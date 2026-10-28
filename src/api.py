from pathlib import Path
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
import pandas as pd
from src.data_loader import DataLoader
from src.statistics import DescriptiveStatistics

app = FastAPI(
    title="Customer Shopping Analytics API",
    description="DAV Academic REST API serving shopping insights, metrics, and filtered customer records.",
    version="1.0.0"
)

# Base path relative to repository root
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "processed" / "customer_shopping_cleaned.csv"


def get_data() -> pd.DataFrame:
    """Load cleaned dataset from disk or raise HTTP 500."""
    if not DATA_PATH.exists():
        raise HTTPException(status_code=500, detail="Processed dataset not found. Please run preprocessing first.")
    return DataLoader.load_csv(DATA_PATH)


@app.get("/")
def read_root():
    """Root metadata endpoint."""
    return {
        "project": "Customer Shopping Analytics (DAV Project)",
        "version": "1.0.0",
        "status": "online",
        "documentation": "/docs"
    }


@app.get("/health")
def health_check():
    """Service health status."""
    return {"status": "healthy", "dataset_available": DATA_PATH.exists()}


@app.get("/stats/summary")
def get_dataset_summary():
    """Retrieve global KPIs and descriptive statistics."""
    df = get_data()
    total_rev = float(df["purchase_amount"].sum())
    cust_count = int(df["customer_id"].nunique())
    aov = float(df["purchase_amount"].mean())
    avg_rating = float(df["review_rating"].mean())

    univariate = DescriptiveStatistics.compute_univariate_summary(df["purchase_amount"])

    return {
        "kpis": {
            "total_revenue": total_rev,
            "total_customers": cust_count,
            "average_order_value": round(aov, 2),
            "average_review_rating": round(avg_rating, 2)
        },
        "purchase_amount_distribution": univariate
    }


@app.get("/stats/categories")
def get_category_metrics():
    """Retrieve revenue, volume, and mean spend breakdown by product category."""
    df = get_data()
    summary = DescriptiveStatistics.grouped_spending_summary(df, "category")
    return {"categories": summary.to_dict(orient="records")}


@app.get("/customers/filter")
def filter_customers(
    gender: str | None = Query(None, description="Filter by gender (Male / Female)"),
    category: str | None = Query(None, description="Filter by product category"),
    subscription: str | None = Query(None, description="Filter by subscription status (Yes / No)"),
    min_amount: float | None = Query(None, ge=0, description="Minimum purchase amount in USD"),
    max_amount: float | None = Query(None, ge=0, description="Maximum purchase amount in USD"),
    limit: int = Query(50, ge=1, le=500, description="Max records to return")
):
    """Query and filter customer transaction records with parameter validation."""
    df = get_data()

    if gender:
        if gender not in ["Male", "Female"]:
            raise HTTPException(status_code=400, detail="Gender must be 'Male' or 'Female'.")
        df = df[df["gender"].str.lower() == gender.lower()]

    if category:
        df = df[df["category"].str.lower() == category.lower()]

    if subscription:
        if subscription not in ["Yes", "No"]:
            raise HTTPException(status_code=400, detail="Subscription must be 'Yes' or 'No'.")
        df = df[df["subscription_status"].str.lower() == subscription.lower()]

    if min_amount is not None:
        df = df[df["purchase_amount"] >= min_amount]

    if max_amount is not None:
        df = df[df["purchase_amount"] <= max_amount]

    records = df.head(limit).to_dict(orient="records")
    return {
        "total_matched": len(df),
        "limit": limit,
        "records": records
    }


@app.get("/export/json")
def export_dataset_json(limit: int = Query(100, ge=1, le=3900)):
    """Export cleaned customer records as JSON."""
    df = get_data()
    return JSONResponse(content=df.head(limit).to_dict(orient="records"))

