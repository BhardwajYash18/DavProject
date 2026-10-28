# 📊 Customer Shopping Behaviour Analytics (DAV Academic Project)

> An end-to-end Python-based **Data Analytics and Visualization (DAV)** academic project covering data collection, multi-format loading, robust preprocessing, SQLite relational persistence, descriptive statistics, hypothesis testing, exploratory visualization, regression modeling, time-series forecasting, a FastAPI REST service, and an interactive Streamlit dashboard.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![SQLite](https://img.shields.io/badge/Database-SQLite3-lightgrey?logo=sqlite)
![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-red?logo=streamlit)
![FastAPI](https://img.shields.io/badge/API-FastAPI-teal?logo=fastapi)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)
![Tests](https://img.shields.io/badge/Tests-33%20Passed-success)

---

## 📌 Project Overview

This repository transforms the synthetic Customer Shopping Trends dataset into a complete, reproducible **Data Analytics and Visualization (DAV)** laboratory submission. All proprietary dependencies (such as Microsoft Power BI Desktop and local MySQL database servers) have been eliminated and replaced with modern, self-contained Python libraries (`pandas`, `numpy`, `scipy`, `scikit-learn`, `matplotlib`, `seaborn`, `plotly`, `sqlite3`, `fastapi`, and `streamlit`).

---

## 🗺️ DAV Syllabus Coverage Matrix

| DAV Syllabus Topic | Implementation in Repository | Verification Evidence |
|---|---|---|
| **Data Collection & Loading** | `src/data_loader.py` with multi-format parsing for CSV, JSON, XML, and TXT; strict schema validation and custom error handling. | `tests/test_data_loader.py` (5 unit tests passed). |
| **Data Preprocessing** | `src/preprocessor.py` for category-level median imputation, duplicate removal, type casting, IQR-based outlier boundaries, age binning, frequency mapping, Min-Max normalization, and Z-score standardization. | `tests/test_preprocessor.py` (6 unit tests passed). |
| **Data Integration** | Relational normalization splitting flat data into `customers` and `orders` entities linked by primary and foreign keys. | `sql/schema.sql` and `src/database.py`. |
| **Descriptive Statistics** | `src/statistics.py` computing mean, median, mode, sample variance, standard deviation, quartiles, IQR, skewness, kurtosis, grouped revenue summaries, and cross-tabulation. | `tests/test_statistics.py` (4 unit tests passed). |
| **Data Aggregation** | Category-level and demographic spending summaries in Python and SQL (SUM, AVG, COUNT, HAVING). | `sql/queries.sql` and `src/statistics.py`. |
| **Data Visualization** | Publication-ready Matplotlib distributions and boxplots; Seaborn demographic comparisons and correlation heatmaps; Plotly interactive donut and category charts. | `src/visualization.py` and `dashboard/app.py`. |
| **Correlation Analysis** | Pearson correlation matrix excluding surrogate identifier columns (`customer_id`) and annotated Seaborn heatmap. | `src/statistics.py` and `src/visualization.py`. |
| **Regression Analysis** | `src/regression.py` predicting `purchase_amount` with train/test isolation (no leakage), baseline dummy model, Linear and Ridge models, backward-compatible RMSE fallback, evaluation (MAE, RMSE, $R^2$), residual diagnostics, and academic limitations. | `tests/test_regression.py` (3 unit tests passed). |
| **Database Management** | `src/database.py` with Python's `sqlite3`, DDL schema, parameterization, and 11 queries demonstrating joins, subqueries, CTEs, and window functions. | `tests/test_database.py` (3 unit tests passed). |
| **API Communication** | `src/api.py` FastAPI service exposing `/health`, `/stats/summary`, `/stats/categories`, `/customers/filter` with input validation, and `/export/json`. | `tests/test_api.py` (6 unit tests passed). |
| **Data Export** | Automated export of cleaned data and filtered results to CSV and JSON formats. | `data/processed/customer_shopping_cleaned.{csv,json}` and Streamlit download buttons. |
| **Time-Series Analysis** | `src/timeseries.py` using authentic, date-indexed retail transactions; date parsing, daily/weekly/monthly resampling, 7-day and 30-day rolling averages, complete annual cycle monthly seasonality (2023), and chronological forecasting. | `tests/test_timeseries.py` (4 unit tests passed). |
| **Interactive Dashboard** | `dashboard/app.py` multi-tab Streamlit web application with live KPI metrics, dynamic sidebar slicers, interactive charts, and an in-browser SQLite query runner. | Verified on `localhost:8501`. |
| **Reproducibility** | Modular architecture, `requirements.txt`, automated pytest test suite (32 passed), and reproducible Jupyter notebook. | `notebooks/dav_customer_shopping_analysis.ipynb`. |

---

## 🗂️ Repository Architecture

```
customer-shopping-behaviour/
├── data/
│   ├── raw/
│   │   ├── customer_shopping_behavior.csv    # Original verified shopping dataset (3,900 rows)
│   │   ├── sample_data.json                  # Sample multi-format loader test fixture
│   │   ├── sample_data.xml                   # Sample XML test fixture
│   │   └── sample_data.txt                   # Sample delimited text fixture
│   ├── processed/
│   │   ├── customer_shopping_cleaned.csv     # Preprocessed cleaned dataset (CSV)
│   │   └── customer_shopping_cleaned.json    # Preprocessed cleaned dataset (JSON)
│   ├── timeseries/
│   │   └── retail_sales_timeseries.csv       # Public date-indexed retail sales series (1,000 records)
│   └── customer_shopping.db                  # Normalized SQLite relational database
├── src/
│   ├── __init__.py
│   ├── data_loader.py                        # Multi-format data loader (CSV, JSON, XML, TXT)
│   ├── preprocessor.py                       # Imputation, deduplication, IQR, normalization
│   ├── database.py                           # SQLite connection, DDL execution, query runner
│   ├── statistics.py                         # Univariate stats, grouped summaries, hypothesis tests
│   ├── visualization.py                      # Matplotlib, Seaborn, and Plotly graphics
│   ├── regression.py                         # Purchase amount prediction & residual diagnostics
│   ├── timeseries.py                         # Rolling trends, seasonality, and forecasting
│   └── api.py                                # FastAPI REST service endpoints
├── dashboard/
│   └── app.py                                # Streamlit interactive web dashboard
├── sql/
│   ├── schema.sql                            # SQLite normalized schema (customers, orders)
│   └── queries.sql                           # 11 analytical business queries (joins, CTE, window)
├── notebooks/
│   ├── dav_customer_shopping_analysis.ipynb  # End-to-end reproducible DAV practical notebook
│   └── customer_shopping_behavior.ipynb      # Cleaned exploratory notebook
├── tests/
│   ├── __init__.py
│   ├── test_data_loader.py                   # Loader & schema validation tests
│   ├── test_preprocessor.py                  # Cleaning, imputation, and outlier tests
│   ├── test_database.py                      # SQLite DDL and query tests
│   ├── test_statistics.py                    # Univariate and hypothesis test assertions
│   ├── test_regression.py                    # Regression evaluation & no-leakage tests
│   ├── test_timeseries.py                    # Time-series resampling & forecasting tests
│   └── test_api.py                           # FastAPI TestClient endpoint tests
├── requirements.txt                          # Pinned Python package dependencies
├── LICENSE                                   # MIT License
└── README.md                                 # Complete project documentation
```

---

## 🧩 Datasets & Limitations

### 1. Customer Shopping Behaviour Dataset
- **Source:** Kaggle — Customer Shopping Trends Dataset (`iamsouravbanerjee/customer-shopping-trends-dataset`).
- **License:** CC0 Public Domain.
- **Records:** 3,900 rows, 18 original features.
- **Location:** `data/raw/customer_shopping_behavior.csv`.
- **Attributes:** Customer ID, Age, Gender, Item Purchased, Category, Purchase Amount, Location, Size, Color, Season, Review Rating, Subscription Status, Shipping Type, Discount Applied, Previous Purchases, Payment Method, Frequency of Purchases.
- **Critical Limitation:** The shopping dataset **lacks transaction timestamps or dates**. It includes only categorical variables (`Season` and `Frequency of Purchases`). Per academic integrity standards, synthetic dates are **not** fabricated.

### 2. Retail Sales Time-Series Dataset
- **Source:** Public Retail Sales Transaction Data (`retail_sales_dataset.csv`).
- **Temporal Span:** January 1, 2023 to January 1, 2024 (1,000 transactions across 345 observed trading dates).
- **Location:** `data/timeseries/retail_sales_timeseries.csv`.
- **Attributes:** Transaction ID, Date, Customer ID, Gender, Age, Product Category, Quantity, Price per Unit, Total Amount.
- **Methodological Assumptions:**
  - Preserves observed trading dates (345 days) rather than artificially filling 21 unobserved calendar dates with $0 sales, preventing artificial deflation of daily averages and distortion of rolling variance.
  - Monthly seasonality index is evaluated on the complete annual cycle (January–December 2023, 998 transactions) to prevent the single observation on January 1, 2024 from skewing January seasonal metrics.
  - Forecasting uses chronological train/test separation (last 60 observed days as test set) without look-ahead bias.

---

## ⚙️ Installation and Setup

### 1. Clone & Navigate to Repository
```bash
git clone https://github.com/BhardwajYash18/DavProject.git
cd DavProject
```
*(If cloned into an existing folder name, e.g., `customer-shopping-behaviour`, navigate into that folder).*

### 2. Create and Activate a Virtual Environment
```bash
# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🚀 Execution Guide

### 1. Run Data Preprocessing & SQLite Database Setup
```bash
python -c "
from src.data_loader import DataLoader
from src.preprocessor import Preprocessor
from src.database import DatabaseManager

raw_df = DataLoader.load_csv('data/raw/customer_shopping_behavior.csv', validate_schema=True)
cleaned_df, stats = Preprocessor.run_full_pipeline(raw_df, export_dir='data/processed')
db = DatabaseManager('data/customer_shopping.db')
db.initialize_schema('sql/schema.sql')
n_c, n_o = db.populate_from_dataframe(cleaned_df)
print(f'Ready! Cleaned {len(cleaned_df)} rows and inserted {n_c} customers and {n_o} orders.')
"
```

### 2. Launch the Streamlit Interactive Dashboard
```bash
python -m streamlit run dashboard/app.py
```
Open your browser at `http://localhost:8501` to access:
- **KPI Metrics:** Total Revenue, Customer Orders, AOV, Average Rating.
- **Interactive Slicers:** Filter by Category, Gender, Subscription, Season, and Price.
- **Plots:** Plotly donut charts, category revenue bars, and demographic breakdowns.
- **Time-Series Explorer:** 7-day and 30-day moving averages with seasonality metrics.
- **In-Browser SQL Runner:** Execute any of the 11 SQLite analytical queries interactively.
- **Data Export:** Instant CSV and JSON export buttons.

### 3. Start the FastAPI REST API
```bash
python -m uvicorn src.api:app --reload --port 8000
```
- Interactive Swagger UI: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`
- Summary KPIs: `http://localhost:8000/stats/summary`
- Category breakdown: `http://localhost:8000/stats/categories`
- Filtered records: `http://localhost:8000/customers/filter?gender=Female&category=Footwear&limit=10`

### 4. Run the Jupyter Notebook Practical
```bash
python -m jupyter lab notebooks/dav_customer_shopping_analysis.ipynb
```
Follow the narrated practical steps from ingestion to forecasting.

---

## 🧪 Automated Testing

Execute the complete 32-test suite using `pytest`:
```bash
python -m pytest tests/ -v
```

Expected output:
```
======================== 32 passed in ~3.0s ========================
```

---

## 📈 Key Statistical & Analytical Findings

1. **Revenue Drivers:** Clothing accounts for **44.7%** ($104,264) of total revenue, followed by Accessories (**31.8%**), Footwear (**15.5%**), and Outerwear (**7.9%**).
2. **Subscriber Spending Hypothesis Test (Two-Sample t-test):**
   - $H_0$: $\mu_{\text{subscriber}} = \mu_{\text{non-subscriber}}$
   - $t = -0.4368$, $p = 0.6623 \ge 0.05$.
   - **Conclusion:** We fail to reject $H_0$. There is no statistically significant difference in order amounts between subscribers ($59.49) and non-subscribers ($59.87).
3. **Discount vs Category Independence Test ($\chi^2$ Test):**
   - $\chi^2 = 1.2003$, $p = 0.7529 \ge 0.05$.
   - **Conclusion:** Discount application is independent of product category.
4. **Seasonal Spending Variation (One-Way ANOVA):**
   - $F = 3.7461$, $p = 0.0106 < 0.05$.
   - **Conclusion:** Reject $H_0$. Significant seasonal variance in mean purchase amount is observed across seasons.
5. **Regression Predictability & Academic Limitations:**
   - Linear regression predicting `purchase_amount` yields test $MAE \approx 20.77$ and $R^2 \approx -0.01$, matching the baseline dummy mean predictor ($MAE \approx 20.74$).
   - **Interpretation:** In this synthetic dataset, purchase amount is distributed uniformly and independently of customer demographics. This confirms that demographic attributes alone cannot reliably predict basket size without behavioral transaction logs.

---

## 👤 Author & Academic Details

- **Author:** Yash Bhardwaj
- **GitHub:** [BhardwajYash18](https://github.com/BhardwajYash18)
- **Repository:** [DavProject](https://github.com/BhardwajYash18/DavProject.git)
- **Original Dataset Credit:** Sourav Banerjee (Kaggle)
- **Curriculum Alignment:** Data Analytics and Visualization (DAV) Laboratory Submission
- **License:** MIT License
