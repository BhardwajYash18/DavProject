from pathlib import Path
import sqlite3
import pandas as pd


class DatabaseManager:
    """Manages SQLite database creation, data population, and query execution."""

    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def get_connection(self) -> sqlite3.Connection:
        """Create and return a connection with foreign key constraints enabled."""
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.row_factory = sqlite3.Row
        return conn

    def initialize_schema(self, schema_file: str | Path) -> None:
        """Execute DDL script to create database tables and views."""
        schema_path = Path(schema_file)
        if not schema_path.exists():
            raise FileNotFoundError(f"Schema file not found: {schema_path}")

        with open(schema_path, "r", encoding="utf-8") as f:
            ddl_script = f.read()

        with self.get_connection() as conn:
            conn.executescript(ddl_script)

    def populate_from_dataframe(self, cleaned_df: pd.DataFrame) -> tuple[int, int]:
        """
        Normalize and insert cleaned data into 'customers' and 'orders' tables.
        Returns the number of customer and order records inserted.
        """
        # 1. Prepare Customers records (unique customer demographics)
        customer_cols = [
            "customer_id", "age", "gender", "location", "age_group",
            "subscription_status", "previous_purchases", "frequency_of_purchases",
            "purchase_frequency_days"
        ]
        customers_df = cleaned_df[customer_cols].drop_duplicates(subset=["customer_id"])

        # 2. Prepare Orders records
        order_cols = [
            "customer_id", "item_purchased", "category", "purchase_amount",
            "size", "color", "season", "review_rating", "shipping_type",
            "discount_applied", "payment_method"
        ]
        orders_df = cleaned_df[order_cols].copy()

        with self.get_connection() as conn:
            # Insert customers
            customers_df.to_sql("customers", conn, if_exists="append", index=False)
            # Insert orders
            orders_df.to_sql("orders", conn, if_exists="append", index=False)

        return len(customers_df), len(orders_df)

    def execute_query(self, query: str, params: tuple | dict | None = None) -> pd.DataFrame:
        """Execute a parameterized SQL query and return results as a DataFrame."""
        with self.get_connection() as conn:
            if params:
                return pd.read_sql_query(query, conn, params=params)
            return pd.read_sql_query(query, conn)

    def execute_script(self, script_path: str | Path) -> list[tuple[str, pd.DataFrame]]:
        """
        Execute SQL analytical script containing multiple semicolon-separated statements.
        Returns pairs of (query_header/comment, result_dataframe).
        """
        path = Path(script_path)
        with open(path, "r", encoding="utf-8") as f:
            raw_text = f.read()

        results = []
        raw_queries = raw_text.split(";")
        for block in raw_queries:
            block = block.strip()
            if not block:
                continue
            # Extract leading comment as description
            lines = block.splitlines()
            desc = "SQL Query"
            for line in lines:
                if line.startswith("--"):
                    desc = line.lstrip("- ").strip()
                    break
            df = self.execute_query(block)
            results.append((desc, df))
        return results

