from pathlib import Path
import pytest
import sqlite3
import pandas as pd
from src.data_loader import DataLoader
from src.preprocessor import Preprocessor
from src.database import DatabaseManager

REPO_DIR = Path(__file__).resolve().parent.parent
RAW_CSV = REPO_DIR / "data" / "raw" / "customer_shopping_behavior.csv"
SCHEMA_SQL = REPO_DIR / "sql" / "schema.sql"
QUERIES_SQL = REPO_DIR / "sql" / "queries.sql"


@pytest.fixture
def populated_db(tmp_path):
    db_file = tmp_path / "test_shopping.db"
    db = DatabaseManager(db_file)
    db.initialize_schema(SCHEMA_SQL)

    raw_df = DataLoader.load_csv(RAW_CSV)
    cleaned_df, _ = Preprocessor.run_full_pipeline(raw_df)
    db.populate_from_dataframe(cleaned_df)
    return db


def test_schema_and_population(populated_db):
    df_cust = populated_db.execute_query("SELECT COUNT(*) AS c FROM customers")
    assert df_cust.iloc[0]["c"] == 3900

    df_orders = populated_db.execute_query("SELECT COUNT(*) AS c FROM orders")
    assert df_orders.iloc[0]["c"] == 3900


def test_foreign_key_constraint(populated_db):
    # Attempting to insert an order with non-existent customer_id should raise IntegrityError
    bad_order_sql = """
    INSERT INTO orders (customer_id, item_purchased, category, purchase_amount, size, color, season, review_rating, shipping_type, discount_applied, payment_method)
    VALUES (999999, 'Coat', 'Clothing', 50.0, 'M', 'Red', 'Winter', 4.0, 'Express', 'No', 'Cash');
    """
    with pytest.raises(sqlite3.IntegrityError):
        with populated_db.get_connection() as conn:
            conn.execute(bad_order_sql)


def test_all_queries_execution(populated_db):
    results = populated_db.execute_script(QUERIES_SQL)
    assert len(results) >= 10
    for desc, res_df in results:
        assert isinstance(res_df, pd.DataFrame)
        assert len(res_df) > 0, f"Query '{desc}' returned empty results"

