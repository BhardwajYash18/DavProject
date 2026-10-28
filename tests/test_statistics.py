from pathlib import Path
import pytest
import pandas as pd
import numpy as np
from src.data_loader import DataLoader
from src.preprocessor import Preprocessor
from src.statistics import DescriptiveStatistics, CorrelationAnalyzer, HypothesisTesting

REPO_DIR = Path(__file__).resolve().parent.parent
RAW_CSV = REPO_DIR / "data" / "raw" / "customer_shopping_behavior.csv"


@pytest.fixture
def cleaned_data():
    raw_df = DataLoader.load_csv(RAW_CSV)
    cleaned, _ = Preprocessor.run_full_pipeline(raw_df)
    return cleaned


def test_univariate_summary():
    s = pd.Series([10.0, 20.0, 20.0, 30.0, 40.0, 50.0])
    res = DescriptiveStatistics.compute_univariate_summary(s)
    assert res["count"] == 6
    assert np.isclose(res["mean"], 28.333333, atol=1e-4)
    assert res["median"] == 25.0
    assert res["mode"] == 20.0
    assert res["min"] == 10.0
    assert res["max"] == 50.0
    assert res["range"] == 40.0


def test_univariate_summary_edge_cases():
    # Empty series
    assert DescriptiveStatistics.compute_univariate_summary(pd.Series([])) == {}
    # Single value series
    single_res = DescriptiveStatistics.compute_univariate_summary(pd.Series([42.0]))
    assert single_res["count"] == 1
    assert single_res["mean"] == 42.0
    assert single_res["variance"] == 0.0


def test_grouped_spending_summary(cleaned_data):
    grp = DescriptiveStatistics.grouped_spending_summary(cleaned_data, "category")
    assert len(grp) == 4
    assert "total_revenue" in grp.columns
    assert "mean_purchase" in grp.columns
    assert np.isclose(grp["revenue_share_pct"].sum(), 100.0)


def test_correlation_matrix_excludes_identifiers(cleaned_data):
    corr = CorrelationAnalyzer.compute_correlation_matrix(cleaned_data, exclude_identifiers=True)
    assert "purchase_amount" in corr.columns
    assert "customer_id" not in corr.columns, "Identifier 'customer_id' must be excluded from correlation"
    assert np.isclose(corr.loc["purchase_amount", "purchase_amount"], 1.0)


def test_hypothesis_tests(cleaned_data):
    # T-test
    ttest = HypothesisTesting.test_subscriber_spending_difference(cleaned_data)
    assert "t_statistic" in ttest
    assert "p_value" in ttest
    assert 0.0 <= ttest["p_value"] <= 1.0

    # Chi-square test
    chi2 = HypothesisTesting.test_discount_category_independence(cleaned_data)
    assert "chi2_statistic" in chi2
    assert "p_value" in chi2
    assert 0.0 <= chi2["p_value"] <= 1.0

    # ANOVA test
    anova = HypothesisTesting.test_seasonal_spending_anova(cleaned_data)
    assert "f_statistic" in anova
    assert "p_value" in anova
    assert 0.0 <= anova["p_value"] <= 1.0
