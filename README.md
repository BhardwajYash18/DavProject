# Customer Shopping Behaviour Analysis

An end-to-end data analysis project exploring customer shopping patterns using **SQL**, **Python (Pandas)**, and **Power BI**.

---

## Project Overview

This project analyses a synthetic customer shopping dataset to uncover insights about revenue drivers, customer segments, product performance, and subscription behaviour. The full pipeline goes from raw CSV data → cleaned database → SQL analysis → interactive dashboard.

---

## Tools & Technologies

| Tool | Purpose |
|------|---------|
| Python (Pandas) | Data cleaning and feature engineering |
| MySQL | Relational database and analytical queries |
| Microsoft Power BI | Interactive dashboard and visualisation |
| SQLAlchemy | Python-to-MySQL data export |

---

## Dataset

- **Source:** Kaggle — [Customer Shopping Trends Dataset](https://www.kaggle.com/datasets/iamsouravbanerjee/customer-shopping-trends-dataset) by iamsouravbanerjee
- **Records:** 3,900 customers
- **Columns:** 18 original features
- **Note:** This is a synthetic dataset created for educational purposes only.

---

## Project Pipeline

```
Raw CSV  →  Python Pandas (cleaning)  →  MySQL (SQL queries)  →  Power BI (dashboard)
```

### Stage 1 — Data Cleaning (Python Pandas)
- Handled missing values in `review_rating` using **category-level median imputation**
- Standardised all column names (lowercase, underscores)
- Created `age_group` column using `pd.qcut()` (quartile-based binning)
- Encoded `frequency_of_purchases` into numeric days
- Dropped redundant column (`promo_code_used` was identical to `discount_applied`)
- Exported cleaned data directly to MySQL via SQLAlchemy

### Stage 2 — SQL Analysis (MySQL)
10 analytical queries covering:
- Revenue breakdown by gender and age group
- Customer segmentation (New / Returning / Loyal)
- Subscription vs. non-subscription spend comparison
- Top products by review rating and discount rate
- Top 3 products per category using window functions (ROW_NUMBER)
- Shipping type comparison

### Stage 3 — Power BI Dashboard
- 4 KPI cards: Total Customers, Avg. Review Score, Avg. Order Value, Total Revenue
- Donut chart: Subscription status breakdown
- Column charts: Revenue and sales count by category
- Bar charts: Revenue and sales by age group
- 4 slicers: Subscription, Gender, Category, Shipping Type
- Clear All Slicers action button

---

## Key Findings

1. **Subscribers spend more** — subscribed customers have a higher average order value and contribute more total revenue
2. **Clothing dominates** — highest revenue and transaction volume across all categories
3. **Adult and Middle-Aged groups** drive the most total revenue
4. **Repeat buyers subscribe more** — customers with 5+ previous purchases are significantly more likely to subscribe
5. **Discounts aren't always needed** — many discount-using customers still spend above the average order value

---

## Files in This Repository

| File | Description |
|------|-------------|
| `customer_shopping_behavior.ipynb` | Python data cleaning notebook |
| `customer_shopping_behavior_query.sql` | 10 analytical SQL queries |
| `customer_shopping_behavior_project.pbix` | Power BI dashboard file |
| `Customer_Shopping_Behaviour_Report.docx` | Full project report |

---

## Dashboard Preview

> Open the `.pbix` file in Microsoft Power BI Desktop to explore the interactive dashboard.

---

*Data source: Kaggle · Customer Shopping Trends Dataset · Synthetic data · June 2026*
