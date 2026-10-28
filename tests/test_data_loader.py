from pathlib import Path
import pytest
import pandas as pd
from src.data_loader import DataLoader, DataLoaderError

REPO_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = REPO_DIR / "data" / "raw"


def test_load_csv_valid():
    csv_file = RAW_DIR / "customer_shopping_behavior.csv"
    df = DataLoader.load_csv(csv_file, validate_schema=True)
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (3900, 18)
    assert "Customer ID" in df.columns
    assert "Purchase Amount (USD)" in df.columns


def test_load_csv_not_found():
    with pytest.raises(DataLoaderError, match="File not found"):
        DataLoader.load_csv("non_existent_file.csv")


def test_load_json_valid():
    json_file = RAW_DIR / "sample_data.json"
    df = DataLoader.load_json(json_file)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 10
    assert "Customer ID" in df.columns


def test_load_xml_valid():
    xml_file = RAW_DIR / "sample_data.xml"
    df = DataLoader.load_xml(xml_file)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 10
    assert "Customer_ID" in df.columns


def test_load_txt_valid():
    txt_file = RAW_DIR / "sample_data.txt"
    df = DataLoader.load_txt(txt_file)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 10
    assert "Customer ID" in df.columns


def test_validate_schema_failure():
    bad_df = pd.DataFrame({"Customer ID": [1, 2], "Age": [20, 30]})
    with pytest.raises(DataLoaderError, match="Schema validation failed"):
        DataLoader.validate_shopping_schema(bad_df)
