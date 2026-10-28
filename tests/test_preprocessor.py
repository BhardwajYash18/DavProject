from pathlib import Path
import pytest
import pandas as pd
import numpy as np
from src.data_loader import DataLoader
from src.preprocessor import Preprocessor

REPO_DIR = Path(__file__).resolve().parent.parent
RAW_CSV = REPO_DIR / "data" / "raw" / "customer_shopping_behavior.csv"


@pytest.fixture
def raw_data():
    return DataLoader.load_csv(RAW_CSV)


def test_standardize_column_names(raw_data):
    p = Preprocessor(raw_data)
    p.standardize_column_names()
    assert "purchase_amount" in p.df.columns
    assert "customer_id" in p.df.columns
    assert "review_rating" in p.df.columns
    assert " " not in "".join(p.df.columns)


def test_handle_missing_values(raw_data):
    # Artificially inject nulls in review_rating
    dirty_df = raw_data.copy()
    p_initial = Preprocessor(dirty_df).standardize_column_names()
    p_initial.df.loc[0:4, "review_rating"] = np.nan

    p_initial.handle_missing_values()
    assert p_initial.df["review_rating"].isnull().sum() == 0


def test_detect_outliers_iqr(raw_data):
    p = Preprocessor(raw_data).standardize_column_names()
    outlier_dict = p.detect_outliers_iqr(["purchase_amount", "age"])
    assert "purchase_amount" in outlier_dict
    assert "iqr" in outlier_dict["purchase_amount"]
    assert outlier_dict["purchase_amount"]["lower_bound"] < outlier_dict["purchase_amount"]["upper_bound"]


def test_engineer_features(raw_data):
    p = Preprocessor(raw_data).standardize_column_names().engineer_features()
    assert "age_group" in p.df.columns
    assert "purchase_frequency_days" in p.df.columns
    assert "promo_code_used" not in p.df.columns  # collinear column dropped


def test_normalization_and_standardization():
    s = pd.Series([10.0, 20.0, 30.0, 40.0, 50.0])
    norm = Preprocessor.normalize_min_max(s)
    assert norm.min() == 0.0
    assert norm.max() == 1.0

    z = Preprocessor.standardize_zscore(s)
    assert np.isclose(z.mean(), 0.0)
    assert np.isclose(z.std(ddof=0), 1.0)


def test_run_full_pipeline(raw_data, tmp_path):
    cleaned, stats = Preprocessor.run_full_pipeline(raw_data, export_dir=tmp_path)
    assert len(cleaned) == len(raw_data)
    assert (tmp_path / "customer_shopping_cleaned.csv").exists()
    assert (tmp_path / "customer_shopping_cleaned.json").exists()
