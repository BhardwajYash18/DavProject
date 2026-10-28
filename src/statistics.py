import numpy as np
import pandas as pd
from scipy import stats


class DescriptiveStatistics:
    """Computes descriptive metrics, dispersion, frequency tables, and grouped summaries."""

    @staticmethod
    def compute_univariate_summary(series: pd.Series) -> dict:
        """Compute full measures of central tendency, dispersion, and shape for a numeric series."""
        clean_s = series.dropna()
        if len(clean_s) == 0:
            return {}

        mode_res = clean_s.mode()
        mode_val = float(mode_res.iloc[0]) if not mode_res.empty else float("nan")

        q1 = float(clean_s.quantile(0.25))
        q2 = float(clean_s.median())
        q3 = float(clean_s.quantile(0.75))
        iqr = q3 - q1

        variance = float(clean_s.var(ddof=1))
        std_dev = float(clean_s.std(ddof=1))
        mean_val = float(clean_s.mean())

        skewness = float(clean_s.skew())
        kurt = float(clean_s.kurtosis())

        return {
            "count": int(len(clean_s)),
            "mean": mean_val,
            "median": q2,
            "mode": mode_val,
            "variance": variance,
            "std_dev": std_dev,
            "min": float(clean_s.min()),
            "q1": q1,
            "q2": q2,
            "q3": q3,
            "max": float(clean_s.max()),
            "range": float(clean_s.max() - clean_s.min()),
            "iqr": iqr,
            "skewness": skewness,
            "kurtosis": kurt
        }

    @staticmethod
    def compute_all_numeric_summaries(df: pd.DataFrame) -> pd.DataFrame:
        """Compute univariate summaries for all numeric columns in a DataFrame."""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        summaries = {}
        for col in numeric_cols:
            summaries[col] = DescriptiveStatistics.compute_univariate_summary(df[col])
        return pd.DataFrame(summaries)

    @staticmethod
    def grouped_spending_summary(df: pd.DataFrame, group_col: str) -> pd.DataFrame:
        """Compute grouped metrics (count, total revenue, mean spend, std) across a dimension."""
        grouped = df.groupby(group_col)["purchase_amount"].agg(
            customer_count="count",
            total_revenue="sum",
            mean_purchase="mean",
            median_purchase="median",
            std_purchase="std"
        ).reset_index()
        grouped["revenue_share_pct"] = (grouped["total_revenue"] / grouped["total_revenue"].sum()) * 100
        return grouped.sort_values(by="total_revenue", ascending=False)

    @staticmethod
    def cross_tabulate(df: pd.DataFrame, index_col: str, col_col: str, normalize: str | None = None) -> pd.DataFrame:
        """Compute cross-tabulation frequency table between two categorical columns."""
        return pd.crosstab(df[index_col], df[col_col], normalize=normalize, margins=True)


class CorrelationAnalyzer:
    """Computes correlation matrices and bivariate relationships."""

    @staticmethod
    def compute_correlation_matrix(df: pd.DataFrame, method: str = "pearson") -> pd.DataFrame:
        """Calculate correlation matrix for numeric features."""
        numeric_df = df.select_dtypes(include=[np.number])
        return numeric_df.corr(method=method)


class HypothesisTesting:
    """
    Formal statistical hypothesis tests for retail analytics.
    Returns test statistics, p-values, null/alt hypotheses, and academic interpretations.
    """

    @staticmethod
    def test_subscriber_spending_difference(df: pd.DataFrame) -> dict:
        """
        Two-sample independent t-test: Compare purchase amounts of Subscribed vs Non-Subscribed customers.
        H0: Mean purchase amount of subscribers == Mean purchase amount of non-subscribers.
        H1: Mean purchase amount of subscribers != Mean purchase amount of non-subscribers.
        """
        subscribers = df[df["subscription_status"] == "Yes"]["purchase_amount"].dropna()
        non_subscribers = df[df["subscription_status"] == "No"]["purchase_amount"].dropna()

        # Levene's test for equality of variance
        levene_stat, levene_p = stats.levene(subscribers, non_subscribers)
        equal_var = levene_p > 0.05

        t_stat, p_val = stats.ttest_ind(subscribers, non_subscribers, equal_var=equal_var)

        interpretation = (
            "Fail to reject H0: No statistically significant difference in purchase amounts between "
            "subscribers and non-subscribers (p >= 0.05)."
            if p_val >= 0.05 else
            "Reject H0: Statistically significant difference in purchase amounts between subscribers "
            "and non-subscribers (p < 0.05)."
        )

        return {
            "test_name": "Two-sample Independent t-test (Welch's if unequal var)" if not equal_var else "Student's t-test",
            "null_hypothesis": "Mean purchase amount (Subscribers) == Mean purchase amount (Non-subscribers)",
            "alt_hypothesis": "Mean purchase amount (Subscribers) != Mean purchase amount (Non-subscribers)",
            "subscriber_mean": float(subscribers.mean()),
            "non_subscriber_mean": float(non_subscribers.mean()),
            "t_statistic": float(t_stat),
            "p_value": float(p_val),
            "levene_p_value": float(levene_p),
            "significant_at_05": bool(p_val < 0.05),
            "interpretation": interpretation
        }

    @staticmethod
    def test_discount_category_independence(df: pd.DataFrame) -> dict:
        """
        Chi-Square Test of Independence: Test whether discount application is independent of product category.
        H0: Discount application and product category are independent.
        H1: Discount application and product category are dependent.
        """
        contingency_table = pd.crosstab(df["category"], df["discount_applied"])
        chi2, p_val, dof, expected = stats.chi2_contingency(contingency_table)

        interpretation = (
            "Fail to reject H0: Discount application is independent of product category (p >= 0.05)."
            if p_val >= 0.05 else
            "Reject H0: Statistically significant association between product category and discount application (p < 0.05)."
        )

        return {
            "test_name": "Chi-Square Test of Independence",
            "null_hypothesis": "Discount applied and Category are independent",
            "alt_hypothesis": "Discount applied and Category are dependent",
            "chi2_statistic": float(chi2),
            "p_value": float(p_val),
            "degrees_of_freedom": int(dof),
            "contingency_table": contingency_table.to_dict(),
            "significant_at_05": bool(p_val < 0.05),
            "interpretation": interpretation
        }

    @staticmethod
    def test_seasonal_spending_anova(df: pd.DataFrame) -> dict:
        """
        One-Way ANOVA: Test whether mean purchase amounts differ across the 4 seasons.
        H0: Mean purchase amounts are equal across all four seasons.
        H1: At least one season has a different mean purchase amount.
        """
        seasons = df["season"].unique()
        groups = [df[df["season"] == s]["purchase_amount"].dropna() for s in seasons]
        f_stat, p_val = stats.f_oneway(*groups)

        interpretation = (
            "Fail to reject H0: No statistically significant difference in mean purchase amounts across seasons (p >= 0.05)."
            if p_val >= 0.05 else
            "Reject H0: Statistically significant difference in mean purchase amounts across seasons (p < 0.05)."
        )

        return {
            "test_name": "One-Way ANOVA (F-test)",
            "null_hypothesis": "Mean purchase amounts are equal across all seasons",
            "alt_hypothesis": "At least one season has a significantly different mean purchase amount",
            "f_statistic": float(f_stat),
            "p_value": float(p_val),
            "seasons_tested": list(seasons),
            "significant_at_05": bool(p_val < 0.05),
            "interpretation": interpretation
        }

