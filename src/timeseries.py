from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, root_mean_squared_error


class TimeSeriesAnalyzer:
    """
    Time-series analysis and forecasting for dated retail transaction data.
    Enforces strict chronological sorting and temporal train/test separation.
    """

    def __init__(self, file_path: str | Path, date_col: str = "Date", target_col: str = "Total Amount"):
        self.file_path = Path(file_path)
        self.date_col = date_col
        self.target_col = target_col
        self.df = None
        self.daily_series = None

    def load_and_prepare(self) -> pd.DataFrame:
        """Parse datetime column, sort chronologically, and set index."""
        raw_df = pd.read_csv(self.file_path)
        if self.date_col not in raw_df.columns:
            raise KeyError(f"Date column '{self.date_col}' not found in {list(raw_df.columns)}")

        raw_df[self.date_col] = pd.to_datetime(raw_df[self.date_col])
        raw_df = raw_df.sort_values(by=self.date_col).reset_index(drop=True)
        self.df = raw_df

        # Aggregate to daily total sales
        daily = raw_df.groupby(self.date_col)[self.target_col].agg(["sum", "count", "mean"]).reset_index()
        daily.columns = ["date", "daily_total", "transaction_count", "average_transaction"]
        daily = daily.set_index("date").sort_index()

        # Fill missing calendar dates with 0
        full_idx = pd.date_range(start=daily.index.min(), end=daily.index.max(), freq="D")
        daily = daily.reindex(full_idx, fill_value=0)
        daily.index.name = "date"
        self.daily_series = daily
        return self.daily_series

    def compute_rolling_statistics(self, window_short: int = 7, window_long: int = 30) -> pd.DataFrame:
        """Calculate 7-day and 30-day rolling means and standard deviations."""
        if self.daily_series is None:
            self.load_and_prepare()

        res = self.daily_series.copy()
        res[f"rolling_mean_{window_short}d"] = res["daily_total"].rolling(window=window_short, min_periods=1).mean()
        res[f"rolling_std_{window_short}d"] = res["daily_total"].rolling(window=window_short, min_periods=1).std().fillna(0)

        res[f"rolling_mean_{window_long}d"] = res["daily_total"].rolling(window=window_long, min_periods=1).mean()
        res[f"rolling_std_{window_long}d"] = res["daily_total"].rolling(window=window_long, min_periods=1).std().fillna(0)
        return res

    def resample_sales(self, rule: str = "W") -> pd.DataFrame:
        """Resample daily sales into weekly ('W') or monthly ('ME') aggregations."""
        if self.daily_series is None:
            self.load_and_prepare()

        resampled = self.daily_series.resample(rule).agg({
            "daily_total": "sum",
            "transaction_count": "sum",
            "average_transaction": "mean"
        }).reset_index()
        resampled.rename(columns={"daily_total": "total_sales"}, inplace=True)
        return resampled

    def compute_monthly_seasonality(self) -> pd.DataFrame:
        """Calculate seasonal index by month."""
        if self.daily_series is None:
            self.load_and_prepare()

        monthly = self.resample_sales(rule="ME")
        monthly["month"] = monthly["date"].dt.strftime("%b")
        monthly["month_num"] = monthly["date"].dt.month
        monthly_summary = monthly.groupby(["month_num", "month"])["total_sales"].mean().reset_index()
        overall_mean = monthly_summary["total_sales"].mean()
        monthly_summary["seasonal_index"] = monthly_summary["total_sales"] / overall_mean
        return monthly_summary.sort_values(by="month_num")

    def run_temporal_forecasting(self, test_days: int = 60) -> dict:
        """
        Chronological train/test split forecasting on daily sales.
        Uses historical rolling trend extrapolation without look-ahead bias.
        """
        if self.daily_series is None:
            self.load_and_prepare()

        series = self.daily_series["daily_total"]
        if len(series) <= test_days:
            raise ValueError(f"Series length {len(series)} too short for test period of {test_days} days.")

        train = series.iloc[:-test_days]
        test = series.iloc[-test_days:]

        # Baseline 1: Naive persistence (last observed 30-day mean in train)
        train_mean_30d = float(train.tail(30).mean())
        naive_pred = np.full(len(test), fill_value=train_mean_30d)

        # Baseline 2: Linear Trend on time index
        t_train = np.arange(len(train)).reshape(-1, 1)
        t_test = np.arange(len(train), len(train) + len(test)).reshape(-1, 1)

        # Fit simple trend
        poly_coef = np.polyfit(t_train.ravel(), train.values, deg=1)
        trend_pred = np.polyval(poly_coef, t_test.ravel())

        # Evaluate test metrics
        mae_naive = mean_absolute_error(test, naive_pred)
        rmse_naive = root_mean_squared_error(test, naive_pred)

        mae_trend = mean_absolute_error(test, trend_pred)
        rmse_trend = root_mean_squared_error(test, trend_pred)

        return {
            "train_start": str(train.index.min().date()),
            "train_end": str(train.index.max().date()),
            "test_start": str(test.index.min().date()),
            "test_end": str(test.index.max().date()),
            "train_days": int(len(train)),
            "test_days": int(len(test)),
            "naive_30d_mean": {
                "mae": float(mae_naive),
                "rmse": float(rmse_naive)
            },
            "linear_trend": {
                "slope": float(poly_coef[0]),
                "intercept": float(poly_coef[1]),
                "mae": float(mae_trend),
                "rmse": float(rmse_trend)
            },
            "test_dates": [str(d.date()) for d in test.index],
            "actual_values": test.values.tolist(),
            "predicted_values": trend_pred.tolist()
        }

