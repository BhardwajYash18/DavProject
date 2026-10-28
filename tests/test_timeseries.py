from pathlib import Path
import pytest
import pandas as pd
from src.timeseries import TimeSeriesAnalyzer

REPO_DIR = Path(__file__).resolve().parent.parent
TS_CSV = REPO_DIR / "data" / "timeseries" / "retail_sales_timeseries.csv"


def test_timeseries_load_and_rolling():
    analyzer = TimeSeriesAnalyzer(TS_CSV)
    # Default: observed trading days preserved without artificial zero sales
    rolling_df = analyzer.compute_rolling_statistics(window_short=7, window_long=30)

    assert isinstance(rolling_df, pd.DataFrame)
    assert "daily_total" in rolling_df.columns
    assert "rolling_mean_7d" in rolling_df.columns
    assert "rolling_mean_30d" in rolling_df.columns
    assert len(rolling_df) == 345  # 345 observed transaction days


def test_timeseries_fill_unobserved():
    analyzer = TimeSeriesAnalyzer(TS_CSV)
    calendar_df = analyzer.load_and_prepare(fill_unobserved_days=True)
    assert len(calendar_df) == 366  # Full calendar span Jan 1, 2023 to Jan 1, 2024
    assert (calendar_df["daily_total"] == 0).sum() == 21  # 21 unobserved days filled with 0


def test_resampling_and_seasonality():
    analyzer = TimeSeriesAnalyzer(TS_CSV)
    monthly = analyzer.resample_sales(rule="ME")
    assert len(monthly) >= 12
    assert "total_sales" in monthly.columns

    season = analyzer.compute_monthly_seasonality(full_year_only=True)
    assert "seasonal_index" in season.columns
    assert len(season) == 12  # Complete 12-month annual cycle for 2023


def test_forecasting():
    analyzer = TimeSeriesAnalyzer(TS_CSV)
    fc = analyzer.run_temporal_forecasting(test_days=30)
    assert fc["test_days"] == 30
    assert fc["linear_trend"]["mae"] > 0
    assert fc["linear_trend"]["rmse"] > 0
    assert len(fc["predicted_values"]) == 30
