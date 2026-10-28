from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np


class Visualizer:
    """Publication-ready static (Matplotlib/Seaborn) and interactive (Plotly) visualizations."""

    # Set consistent style
    sns.set_theme(style="whitegrid", palette="muted")
    plt.rcParams["font.sans-serif"] = "DejaVu Sans"
    plt.rcParams["figure.dpi"] = 150

    # ------------------ Matplotlib & Seaborn Visualizations ------------------ #

    @staticmethod
    def plot_purchase_distribution(df: pd.DataFrame, save_path: str | Path | None = None) -> plt.Figure:
        """Plot histogram and KDE distribution of customer purchase amounts."""
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.histplot(df["purchase_amount"], kde=True, color="#2b5c8f", bins=25, ax=ax)
        mean_val = df["purchase_amount"].mean()
        median_val = df["purchase_amount"].median()
        ax.axvline(mean_val, color="red", linestyle="--", label=f"Mean: ${mean_val:.2f}")
        ax.axvline(median_val, color="green", linestyle=":", label=f"Median: ${median_val:.2f}")
        ax.set_title("Customer Purchase Amount Distribution (USD)", fontsize=13, weight="bold")
        ax.set_xlabel("Purchase Amount ($)")
        ax.set_ylabel("Customer Count")
        ax.legend()
        plt.tight_layout()
        if save_path:
            fig.savefig(save_path, bbox_inches="tight")
        return fig

    @staticmethod
    def plot_category_boxplots(df: pd.DataFrame, save_path: str | Path | None = None) -> plt.Figure:
        """Boxplot of purchase amount distribution across product categories."""
        fig, ax = plt.subplots(figsize=(9, 5))
        sns.boxplot(data=df, x="category", y="purchase_amount", palette="Set2", ax=ax)
        ax.set_title("Purchase Amount Distribution by Product Category", fontsize=13, weight="bold")
        ax.set_xlabel("Product Category")
        ax.set_ylabel("Purchase Amount ($)")
        plt.tight_layout()
        if save_path:
            fig.savefig(save_path, bbox_inches="tight")
        return fig

    @staticmethod
    def plot_correlation_heatmap(df: pd.DataFrame, save_path: str | Path | None = None) -> plt.Figure:
        """Annotated Seaborn correlation heatmap for numerical attributes."""
        num_cols = ["age", "purchase_amount", "review_rating", "previous_purchases", "purchase_frequency_days"]
        corr_matrix = df[[c for c in num_cols if c in df.columns]].corr()

        fig, ax = plt.subplots(figsize=(7, 6))
        sns.heatmap(corr_matrix, annot=True, fmt=".3f", cmap="coolwarm", vmin=-1, vmax=1, cbar=True, ax=ax, square=True)
        ax.set_title("Correlation Heatmap of Customer Attributes", fontsize=13, weight="bold")
        plt.tight_layout()
        if save_path:
            fig.savefig(save_path, bbox_inches="tight")
        return fig

    @staticmethod
    def plot_demographic_spending(df: pd.DataFrame, save_path: str | Path | None = None) -> plt.Figure:
        """Bar plot comparing average spending by age group and gender."""
        fig, ax = plt.subplots(figsize=(9, 5))
        sns.barplot(data=df, x="age_group", y="purchase_amount", hue="gender", palette="deep", errorbar="se", ax=ax)
        ax.set_title("Average Purchase Amount by Age Group and Gender", fontsize=13, weight="bold")
        ax.set_xlabel("Age Group")
        ax.set_ylabel("Average Purchase Amount ($)")
        ax.legend(title="Gender")
        plt.tight_layout()
        if save_path:
            fig.savefig(save_path, bbox_inches="tight")
        return fig

    @staticmethod
    def plot_regression_residuals(y_actual: np.ndarray, y_pred: np.ndarray, save_path: str | Path | None = None) -> plt.Figure:
        """Residual plot for regression diagnostics."""
        residuals = y_actual - y_pred
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.scatterplot(x=y_pred, y=residuals, alpha=0.6, color="#4c72b0", ax=ax)
        ax.axhline(0, color="red", linestyle="--", linewidth=1.5)
        ax.set_title("Regression Residuals vs Predicted Purchase Amount", fontsize=13, weight="bold")
        ax.set_xlabel("Predicted Purchase Amount ($)")
        ax.set_ylabel("Residuals ($)")
        plt.tight_layout()
        if save_path:
            fig.savefig(save_path, bbox_inches="tight")
        return fig

    # ------------------ Plotly Interactive Visualizations ------------------ #

    @staticmethod
    def plotly_subscription_donut(df: pd.DataFrame) -> go.Figure:
        """Interactive donut chart displaying subscriber distribution."""
        counts = df["subscription_status"].value_counts().reset_index()
        counts.columns = ["subscription_status", "count"]
        fig = px.pie(
            counts,
            names="subscription_status",
            values="count",
            hole=0.45,
            color="subscription_status",
            color_discrete_map={"Yes": "#2ca02c", "No": "#1f77b4"},
            title="Customer Subscription Status Proportion"
        )
        fig.update_traces(textposition="inside", textinfo="percent+label")
        fig.update_layout(showlegend=True, margin=dict(t=40, b=10, l=10, r=10))
        return fig

    @staticmethod
    def plotly_revenue_by_category(df: pd.DataFrame) -> go.Figure:
        """Interactive bar chart displaying revenue and order count by category."""
        summary = df.groupby("category").agg(
            total_revenue=("purchase_amount", "sum"),
            order_count=("purchase_amount", "count")
        ).reset_index().sort_values(by="total_revenue", ascending=False)

        fig = px.bar(
            summary,
            x="category",
            y="total_revenue",
            color="category",
            text="total_revenue",
            hover_data=["order_count"],
            title="Total Revenue by Product Category ($)",
            labels={"total_revenue": "Total Revenue ($)", "category": "Product Category"}
        )
        fig.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
        fig.update_layout(margin=dict(t=40, b=20, l=20, r=20), showlegend=False)
        return fig

    @staticmethod
    def plotly_customer_scatter(df: pd.DataFrame) -> go.Figure:
        """Interactive scatter plot of Purchase Amount vs Age, faceted/colored by Subscription."""
        fig = px.scatter(
            df,
            x="age",
            y="purchase_amount",
            color="subscription_status",
            hover_data=["category", "item_purchased", "review_rating"],
            title="Purchase Amount vs Customer Age",
            labels={"age": "Customer Age", "purchase_amount": "Purchase Amount ($)"},
            opacity=0.7
        )
        fig.update_layout(margin=dict(t=40, b=20, l=20, r=20))
        return fig

    @staticmethod
    def plotly_timeseries_trends(daily_df: pd.DataFrame) -> go.Figure:
        """Interactive time-series line chart with rolling averages."""
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=daily_df.index, y=daily_df["daily_total"],
            mode="lines", name="Daily Sales", opacity=0.35, line=dict(color="#a6c8e0")
        ))
        if "rolling_mean_7d" in daily_df.columns:
            fig.add_trace(go.Scatter(
                x=daily_df.index, y=daily_df["rolling_mean_7d"],
                mode="lines", name="7-Day Moving Avg", line=dict(color="#1f77b4", width=2)
            ))
        if "rolling_mean_30d" in daily_df.columns:
            fig.add_trace(go.Scatter(
                x=daily_df.index, y=daily_df["rolling_mean_30d"],
                mode="lines", name="30-Day Moving Avg", line=dict(color="#ff7f0e", width=2.5)
            ))
        fig.update_layout(
            title="Retail Daily Sales Trends and Rolling Averages",
            xaxis_title="Date",
            yaxis_title="Total Sales ($)",
            hovermode="x unified",
            margin=dict(t=40, b=20, l=20, r=20)
        )
        return fig

