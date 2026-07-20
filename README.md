# 📊 Customer Shopping Behaviour Analysis

> End-to-end data analysis project exploring customer shopping patterns using **SQL**, **Python (Pandas)**, and **Power BI**.

![SQL](https://img.shields.io/badge/SQL-MySQL-blue)
![Python](https://img.shields.io/badge/Python-Pandas-yellow)
![BI](https://img.shields.io/badge/Dashboard-Power%20BI-orange)
![Dataset](https://img.shields.io/badge/Dataset-Kaggle-lightgrey)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

---

## 📌 Overview

This project analyses a synthetic customer shopping dataset to uncover insights about revenue drivers, customer segments, product performance, and subscription behaviour. The full pipeline goes from raw CSV data → cleaned database → SQL analysis → interactive dashboard.

- ✅ *Python (Pandas)* — data cleaning and feature engineering
- ✅ *MySQL* — relational database and analytical queries
- ✅ *Microsoft Power BI* — interactive dashboard and visualisation
- ✅ *SQLAlchemy* — Python-to-MySQL data export

---

## 🗂️ What's in this repo

| File | What it contains |
|---|---|
| 📓 `customer_shopping_behavior.ipynb` | Python data cleaning notebook |
| 📄 `customer_shopping_behavior_query.sql` | 10 analytical SQL queries |
| 📊 `customer_shopping_behavior_project.pbix` | Power BI dashboard file |
| 📋 `Customer_Shopping_Behaviour_Report.docx` | Full project report |

---

## 🧩 Dataset

- **Source:** Kaggle — [Customer Shopping Trends Dataset](https://www.kaggle.com/datasets/iamsouravbanerjee/customer-shopping-trends-dataset)
- **Records:** 3,900 customers
- **Columns:** 18 original features
- **Note:** This is a synthetic dataset created for educational purposes only.

---

## 🔄 Project Pipeline

```
Raw CSV  →  Python Pandas (cleaning)  →  MySQL (SQL queries)  →  Power BI (dashboard)
```

| Stage | Tool | What was done |
|---|---|---|
| *Data Collection* | Kaggle | Downloaded raw CSV — 3,900 records, 18 columns |
| *Data Cleaning* | Python (Pandas) | Handled missing values in `review_rating` using category-level median imputation, standardised column names, created `age_group` using `pd.qcut()`, encoded purchase frequency, dropped redundant column |
| *Data Storage* | MySQL | Exported cleaned DataFrame to MySQL via SQLAlchemy |
| *Analysis* | SQL (MySQL) | 10 business queries — aggregation, subqueries, CTEs, window functions, segmentation |
| *Visualisation* | Power BI | Interactive dashboard with KPI cards, slicers, and consistent colour theme |

---

## 🔍 SQL Analysis

10 analytical queries covering:

| # | Business Question | Concepts Used |
|---|---|---|
| Q1 | Revenue breakdown by gender | GROUP BY, SUM |
| Q2 | Discount users who still spent above average | Subquery, WHERE |
| Q3 | Top 5 products by review rating | ORDER BY, LIMIT |
| Q4 | Standard vs. Express shipping spend | WHERE IN, AVG |
| Q5 | Do subscribers spend more? | GROUP BY, COUNT, AVG, SUM |
| Q6 | Products with highest discount rate | CASE WHEN, SUM, COUNT |
| Q7 | Customer segmentation: New / Returning / Loyal | CTE, CASE WHEN |
| Q8 | Top 3 products per category | CTE, ROW_NUMBER(), PARTITION BY |
| Q9 | Repeat buyers and subscription correlation | WHERE, GROUP BY |
| Q10 | Revenue contribution by age group | GROUP BY, ORDER BY |

---

## 📈 Key Findings

1. **Subscribers spend more** — subscribed customers have a higher average order value and contribute more total revenue
2. **Clothing dominates** — highest revenue and transaction volume across all categories
3. **Adult and Middle-Aged groups** drive the most total revenue
4. **Repeat buyers subscribe more** — customers with 5+ previous purchases are significantly more likely to subscribe
5. **Discounts aren't always necessary** — many discount-using customers still spend above the average order value

---

## 🛠️ Tools & Techniques

- *Data Cleaning:* Python, Pandas — `pd.qcut()`, `groupby().transform()`, `SQLAlchemy`
- *Analysis:* MySQL — Aggregations, CTEs, Window Functions, Conditional Aggregation
- *Visualisation:* Microsoft Power BI Desktop — KPI cards, donut chart, column/bar charts, 4 slicers
- *Reporting:* Microsoft Word — Full pipeline documentation and business insights
- *Data Source:* Kaggle — Customer Shopping Trends Dataset (synthetic).

---


## 👤 Author

**Tushar Bhardwaj**
💻 [GitHub](https://github.com/TusharB2301)

---

*Data source: Kaggle · Customer Shopping Trends Dataset · iamsouravbanerjee · Synthetic data · June 2026*
