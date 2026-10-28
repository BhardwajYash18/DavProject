import pytest
from fastapi.testclient import TestClient
from src.api import app

client = TestClient(app)


def test_api_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"


def test_api_summary_stats():
    res = client.get("/stats/summary")
    assert res.status_code == 200
    data = res.json()
    assert "kpis" in data
    assert data["kpis"]["total_customers"] == 3900
    assert data["kpis"]["total_revenue"] > 0


def test_api_categories():
    res = client.get("/stats/categories")
    assert res.status_code == 200
    cats = res.json()["categories"]
    assert len(cats) == 4


def test_api_filter_valid():
    res = client.get("/customers/filter?gender=Male&limit=10")
    assert res.status_code == 200
    data = res.json()
    assert len(data["records"]) <= 10
    for r in data["records"]:
        assert r["gender"] == "Male"


def test_api_filter_invalid_gender():
    res = client.get("/customers/filter?gender=InvalidGender")
    assert res.status_code == 400
    assert "Gender must be 'Male' or 'Female'" in res.json()["detail"]


def test_api_export_json():
    res = client.get("/export/json?limit=25")
    assert res.status_code == 200
    records = res.json()
    assert len(records) == 25

