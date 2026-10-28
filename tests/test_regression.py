from pathlib import Path
import pytest
import pandas as pd
from src.data_loader import DataLoader
from src.preprocessor import Preprocessor
from src.regression import RegressionPipeline

REPO_DIR = Path(__file__).resolve().parent.parent
RAW_CSV = REPO_DIR / "data" / "raw" / "customer_shopping_behavior.csv"


@pytest.fixture
def cleaned_data():
    raw_df = DataLoader.load_csv(RAW_CSV)
    cleaned, _ = Preprocessor.run_full_pipeline(raw_df)
    return cleaned


def test_regression_pipeline_execution(cleaned_data):
    pipe = RegressionPipeline(cleaned_data, test_size=0.2, random_state=42)
    res = pipe.train(model_type="linear")

    assert "baseline" in res
    assert "test_metrics" in res
    assert res["test_metrics"]["mae"] > 0
    assert res["test_metrics"]["rmse"] > 0
    assert isinstance(res["coefficients"], pd.DataFrame)
    assert len(res["coefficients"]) > 0


def test_ridge_regression(cleaned_data):
    pipe = RegressionPipeline(cleaned_data, test_size=0.2, random_state=42)
    res = pipe.train(model_type="ridge", alpha=1.0)
    assert res["model_type"] == "ridge"
    assert res["test_metrics"]["mae"] > 0

