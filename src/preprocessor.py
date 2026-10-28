from pathlib import Path
import numpy as np
import pandas as pd


class Preprocessor:
    """End-to-end data preprocessing pipeline for customer shopping analysis."""

    FREQUENCY_MAPPING = {
        "Fortnightly": 14,
        "Weekly": 7,
        "Monthly": 30,
        "Quarterly": 90,
        "Bi-Weekly": 14,
        "Annually": 365,
        "Every 3 Months": 90
    }

    AGE_GROUP_LABELS = ["Young-adult", "Adult", "Middle-aged", "Senior"]

    def __init__(self, df: pd.DataFrame):
        # Work on an isolated copy to preserve raw dataset immutability
        self.df = df.copy()
        self.outlier_summary: dict = {}
        self.cleaning_stats: dict = {}

    def standardize_column_names(self) -> "Preprocessor":
        """Clean and normalize column headers to snake_case."""
        cols = self.df.columns.str.lower()
        cols = cols.str.replace(" ", "_")
        cols = cols.str.replace("(", "", regex=False)
        cols = cols.str.replace(")", "", regex=False)
        self.df.columns = cols
        if "purchase_amount_usd" in self.df.columns:
            self.df.rename(columns={"purchase_amount_usd": "purchase_amount"}, inplace=True)
        return self

    def handle_duplicates(self) -> "Preprocessor":
        """Identify and remove exact duplicate records."""
        initial_count = len(self.df)
        self.df.drop_duplicates(inplace=True)
        duplicates_removed = initial_count - len(self.df)
        self.cleaning_stats["duplicates_removed"] = duplicates_removed
        return self

    def handle_missing_values(self) -> "Preprocessor":
        """
        Impute missing numerical ratings using category-level medians.
        Category medians prevent global rating bias across distinct product groups.
        """
        missing_before = int(self.df["review_rating"].isnull().sum())
        if missing_before > 0:
            self.df["review_rating"] = self.df.groupby("category")["review_rating"].transform(
                lambda x: x.fillna(x.median())
            )
            # Fallback to global median if an entire category is null
            if self.df["review_rating"].isnull().any():
                self.df["review_rating"].fillna(self.df["review_rating"].median(), inplace=True)
        self.cleaning_stats["missing_ratings_imputed"] = missing_before
        return self

    def validate_data_types_and_ranges(self) -> "Preprocessor":
        """Enforce strict types and validate realistic domains."""
        self.df["customer_id"] = self.df["customer_id"].astype(int)
        self.df["age"] = pd.to_numeric(self.df["age"], errors="coerce")
        self.df["purchase_amount"] = pd.to_numeric(self.df["purchase_amount"], errors="coerce")
        self.df["previous_purchases"] = pd.to_numeric(self.df["previous_purchases"], errors="coerce")
        self.df["review_rating"] = pd.to_numeric(self.df["review_rating"], errors="coerce")

        # Range filtering: age between 10 and 120, positive purchases
        valid_mask = (
            (self.df["age"] >= 10) & (self.df["age"] <= 120) &
            (self.df["purchase_amount"] > 0) &
            (self.df["previous_purchases"] >= 0) &
            (self.df["review_rating"] >= 1.0) & (self.df["review_rating"] <= 5.0)
        )
        invalid_count = int((~valid_mask).sum())
        if invalid_count > 0:
            self.df = self.df[valid_mask].copy()
        self.cleaning_stats["invalid_records_filtered"] = invalid_count
        return self

    def engineer_features(self) -> "Preprocessor":
        """Create analytical bins, frequency metrics, and prune collinear variables."""
        # 1. Age group discretization via 4 quantiles
        self.df["age_group"] = pd.qcut(self.df["age"], q=4, labels=self.AGE_GROUP_LABELS)

        # 2. Map purchase frequency into days
        self.df["purchase_frequency_days"] = self.df["frequency_of_purchases"].map(self.FREQUENCY_MAPPING)

        # 3. Check and drop collinear promo_code_used if redundant with discount_applied
        if "promo_code_used" in self.df.columns and "discount_applied" in self.df.columns:
            if (self.df["promo_code_used"] == self.df["discount_applied"]).all():
                self.df.drop(columns=["promo_code_used"], inplace=True)
                self.cleaning_stats["collinear_promo_code_dropped"] = True
            else:
                self.cleaning_stats["collinear_promo_code_dropped"] = False
        return self

    def detect_outliers_iqr(self, columns: list[str] | None = None) -> dict:
        """Calculate IQR-based outlier boundaries without silently discarding valid records."""
        if columns is None:
            columns = ["purchase_amount", "age", "previous_purchases"]
        summary = {}
        for col in columns:
            if col in self.df.columns:
                q1 = self.df[col].quantile(0.25)
                q3 = self.df[col].quantile(0.75)
                iqr = q3 - q1
                lower = q1 - 1.5 * iqr
                upper = q3 + 1.5 * iqr
                outliers = self.df[(self.df[col] < lower) | (self.df[col] > upper)]
                summary[col] = {
                    "q1": float(q1),
                    "q3": float(q3),
                    "iqr": float(iqr),
                    "lower_bound": float(lower),
                    "upper_bound": float(upper),
                    "outlier_count": int(len(outliers))
                }
        self.outlier_summary = summary
        return summary

    def get_processed_data(self) -> pd.DataFrame:
        """Return the preprocessed DataFrame."""
        return self.df.copy()

    def export_data(self, output_dir: str | Path) -> tuple[Path, Path]:
        """Export cleaned dataset to both CSV and JSON formats."""
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)
        csv_path = out_path / "customer_shopping_cleaned.csv"
        json_path = out_path / "customer_shopping_cleaned.json"

        # Export CSV
        self.df.to_csv(csv_path, index=False)
        # Export JSON (records orientation)
        self.df.to_json(json_path, orient="records", indent=2)
        return csv_path, json_path

    @staticmethod
    def normalize_min_max(series: pd.Series) -> pd.Series:
        """Min-Max normalization scaling values into [0, 1]."""
        s_min, s_max = series.min(), series.max()
        if s_max == s_min:
            return pd.Series(0.0, index=series.index)
        return (series - s_min) / (s_max - s_min)

    @staticmethod
    def standardize_zscore(series: pd.Series) -> pd.Series:
        """Z-score standardization (zero mean, unit variance)."""
        std = series.std(ddof=0)
        if std == 0:
            return pd.Series(0.0, index=series.index)
        return (series - series.mean()) / std

    @classmethod
    def run_full_pipeline(cls, raw_df: pd.DataFrame, export_dir: str | Path | None = None) -> tuple[pd.DataFrame, dict]:
        """Convenience method to execute the complete preprocessing pipeline."""
        pipeline = cls(raw_df)
        pipeline.standardize_column_names()
        pipeline.handle_duplicates()
        pipeline.handle_missing_values()
        pipeline.validate_data_types_and_ranges()
        pipeline.engineer_features()
        pipeline.detect_outliers_iqr()

        cleaned_df = pipeline.get_processed_data()
        if export_dir:
            pipeline.export_data(export_dir)
        return cleaned_df, pipeline.cleaning_stats

