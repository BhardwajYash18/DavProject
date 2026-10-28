from pathlib import Path
import streamlit as pd_st
import streamlit as st
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Customer Shopping Analytics | DAV Dashboard",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Relative Paths
BASE_DIR = Path(__file__).resolve().parent.parent
CLEANED_DATA_PATH = BASE_DIR / "data" / "processed" / "customer_shopping_cleaned.csv"
DB_PATH = BASE_DIR / "data" / "customer_shopping.db"
QUERIES_PATH = BASE_DIR / "sql" / "queries.sql"
TIMESERIES_PATH = BASE_DIR / "data" / "timeseries" / "retail_sales_timeseries.csv"

# Import core modules
from src.data_loader import DataLoader
from src.visualization import Visualizer
from src.statistics import DescriptiveStatistics, CorrelationAnalyzer
from src.database import DatabaseManager
from src.timeseries import TimeSeriesAnalyzer


@st.cache_data
def load_shopping_data() -> pd.DataFrame:
    if not CLEANED_DATA_PATH.exists():
        st.error(f"Cleaned dataset not found at {CLEANED_DATA_PATH}. Please run preprocessing first.")
        st.stop()
    return DataLoader.load_csv(CLEANED_DATA_PATH)


@st.cache_data
def load_timeseries_data() -> pd.DataFrame:
    if not TIMESERIES_PATH.exists():
        return None
    analyzer = TimeSeriesAnalyzer(TIMESERIES_PATH)
    return analyzer.compute_rolling_statistics()


# Load datasets
df_all = load_shopping_data()

# Sidebar: Filters
st.sidebar.title("🔍 Data Filters")
st.sidebar.caption("Filter cross-sectional customer records:")

# Category filter
categories = ["All"] + sorted(df_all["category"].dropna().unique().tolist())
selected_category = st.sidebar.selectbox("Product Category", categories)

# Gender filter
genders = ["All"] + sorted(df_all["gender"].dropna().unique().tolist())
selected_gender = st.sidebar.selectbox("Customer Gender", genders)

# Subscription filter
subs = ["All"] + sorted(df_all["subscription_status"].dropna().unique().tolist())
selected_sub = st.sidebar.selectbox("Subscription Status", subs)

# Season filter
all_seasons = sorted(df_all["season"].dropna().unique().tolist())
selected_seasons = st.sidebar.multiselect("Season", all_seasons, default=all_seasons)

# Purchase Amount range slider
min_amt = float(df_all["purchase_amount"].min())
max_amt = float(df_all["purchase_amount"].max())
price_range = st.sidebar.slider("Purchase Amount Range ($)", min_amt, max_amt, (min_amt, max_amt))

# Apply filtering
filtered_df = df_all.copy()
if selected_category != "All":
    filtered_df = filtered_df[filtered_df["category"] == selected_category]
if selected_gender != "All":
    filtered_df = filtered_df[filtered_df["gender"] == selected_gender]
if selected_sub != "All":
    filtered_df = filtered_df[filtered_df["subscription_status"] == selected_sub]
if selected_seasons:
    filtered_df = filtered_df[filtered_df["season"].isin(selected_seasons)]
filtered_df = filtered_df[
    (filtered_df["purchase_amount"] >= price_range[0]) &
    (filtered_df["purchase_amount"] <= price_range[1])
]

# Header
st.title("📊 Customer Shopping Behaviour Analytics")
st.markdown("A Python-native **Data Analytics and Visualization (DAV)** dashboard replacing legacy Power BI.")

# KPI Metric Cards (Calculated directly from filtered data)
col1, col2, col3, col4 = st.columns(4)

total_revenue = filtered_df["purchase_amount"].sum()
customer_count = filtered_df["customer_id"].nunique()
aov = filtered_df["purchase_amount"].mean() if customer_count > 0 else 0.0
avg_rating = filtered_df["review_rating"].mean() if customer_count > 0 else 0.0

col1.metric("Total Revenue", f"${total_revenue:,.2f}")
col2.metric("Customer Orders", f"{customer_count:,}")
col3.metric("Average Order Value (AOV)", f"${aov:.2f}")
col4.metric("Average Review Rating", f"{avg_rating:.2f} ⭐")

st.divider()

# Navigation Tabs
tab_overview, tab_demographics, tab_timeseries, tab_sql, tab_export = st.tabs([
    "📈 Overview & Categories",
    "👥 Demographics & Segments",
    "⏳ Time-Series Trends",
    "🗄️ SQLite SQL Analytics",
    "💾 Data Explorer & Export"
])

# ----------------- TAB 1: OVERVIEW & CATEGORIES ----------------- #
with tab_overview:
    st.subheader("Category Revenue & Customer Subscription Overview")
    t1_col1, t1_col2 = st.columns([1.6, 1.4])

    with t1_col1:
        if not filtered_df.empty:
            cat_fig = Visualizer.plotly_revenue_by_category(filtered_df)
            st.plotly_chart(cat_fig, use_container_width=True)
        else:
            st.info("No data available for selected filters.")

    with t1_col2:
        if not filtered_df.empty:
            donut_fig = Visualizer.plotly_subscription_donut(filtered_df)
            st.plotly_chart(donut_fig, use_container_width=True)
        else:
            st.info("No data available for selected filters.")

    st.subheader("Purchase Amount Distribution & Category Spread")
    dist_col1, dist_col2 = st.columns(2)
    with dist_col1:
        fig_dist = Visualizer.plot_purchase_distribution(filtered_df)
        st.pyplot(fig_dist)
    with dist_col2:
        fig_box = Visualizer.plot_category_boxplots(filtered_df)
        st.pyplot(fig_box)

# ----------------- TAB 2: DEMOGRAPHICS & SEGMENTS ----------------- #
with tab_demographics:
    st.subheader("Demographic Spending Breakdown & Feature Correlation")
    demo_col1, demo_col2 = st.columns(2)

    with demo_col1:
        fig_demo = Visualizer.plot_demographic_spending(filtered_df)
        st.pyplot(fig_demo)

    with demo_col2:
        fig_corr = Visualizer.plot_correlation_heatmap(filtered_df)
        st.pyplot(fig_corr)

    st.subheader("Interactive Customer Spending vs Age Explorer")
    if not filtered_df.empty:
        scatter_fig = Visualizer.plotly_customer_scatter(filtered_df)
        st.plotly_chart(scatter_fig, use_container_width=True)

# ----------------- TAB 3: TIME-SERIES TRENDS ----------------- #
with tab_timeseries:
    st.subheader("Retail Sales Time-Series Analysis (Dated Dataset)")
    st.caption("Temporal analytics performed on verified, date-indexed retail transactions (2023-01 to 2024-01).")

    daily_ts = load_timeseries_data()
    if daily_ts is not None:
        ts_fig = Visualizer.plotly_timeseries_trends(daily_ts)
        st.plotly_chart(ts_fig, use_container_width=True)

        st.subheader("Monthly Seasonality Index (Complete Annual Cycle: 2023)")
        analyzer = TimeSeriesAnalyzer(TIMESERIES_PATH)
        season_df = analyzer.compute_monthly_seasonality(full_year_only=True)
        st.dataframe(season_df, use_container_width=True)
    else:
        st.warning("Time-series dataset not found.")

# ----------------- TAB 4: SQL ANALYTICS ----------------- #
with tab_sql:
    st.subheader("Interactive SQLite Query Runner")
    st.caption("Execute predefined analytical SQL queries on the normalized SQLite database schema.")

    if DB_PATH.exists() and QUERIES_PATH.exists():
        db = DatabaseManager(DB_PATH)
        with open(QUERIES_PATH, "r", encoding="utf-8") as f:
            full_sql = f.read()

        raw_blocks = [b.strip() for b in full_sql.split(";") if b.strip()]
        query_options = {}
        for block in raw_blocks:
            first_line = block.splitlines()[0].lstrip("- ").strip()
            query_options[first_line] = block

        chosen_title = st.selectbox("Select SQL Business Query:", list(query_options.keys()))
        selected_sql = query_options[chosen_title]

        st.code(selected_sql, language="sql")
        if st.button("▶ Run SQL Query"):
            try:
                res_df = db.execute_query(selected_sql)
                st.success(f"Query returned {len(res_df)} rows and {len(res_df.columns)} columns.")
                st.dataframe(res_df, use_container_width=True)
            except Exception as e:
                st.error(f"SQL execution error: {e}")
    else:
        st.warning("SQLite database or queries.sql not found.")

# ----------------- TAB 5: DATA EXPLORER & EXPORT ----------------- #
with tab_export:
    st.subheader("Cleaned Dataset Explorer")
    st.write(f"Showing **{len(filtered_df)}** of **{len(df_all)}** total customer records.")
    st.dataframe(filtered_df.head(100), use_container_width=True)

    st.subheader("Data Export")
    exp_col1, exp_col2 = st.columns(2)

    with exp_col1:
        csv_data = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Filtered Data as CSV",
            data=csv_data,
            file_name="customer_shopping_filtered.csv",
            mime="text/csv"
        )

    with exp_col2:
        json_data = filtered_df.to_json(orient="records", indent=2).encode("utf-8")
        st.download_button(
            label="📥 Download Filtered Data as JSON",
            data=json_data,
            file_name="customer_shopping_filtered.json",
            mime="application/json"
        )

