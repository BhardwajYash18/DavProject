from pathlib import Path
import json
import xml.etree.ElementTree as ET
import pandas as pd


class DataLoaderError(Exception):
    """Custom exception raised when data loading or validation fails."""
    pass


class DataLoader:
    """Reusable multi-format data loader with schema validation for CSV, JSON, XML, and TXT files."""

    REQUIRED_SHOPPING_COLUMNS = [
        "Customer ID",
        "Age",
        "Gender",
        "Item Purchased",
        "Category",
        "Purchase Amount (USD)",
        "Location",
        "Size",
        "Color",
        "Season",
        "Review Rating",
        "Subscription Status",
        "Shipping Type",
        "Discount Applied",
        "Promo Code Used",
        "Previous Purchases",
        "Payment Method",
        "Frequency of Purchases"
    ]

    @staticmethod
    def _validate_path(file_path: Path) -> Path:
        path = Path(file_path)
        if not path.exists():
            raise DataLoaderError(f"File not found: {path.resolve()}")
        if not path.is_file():
            raise DataLoaderError(f"Path is not a file: {path.resolve()}")
        return path

    @classmethod
    def load_csv(cls, file_path: str | Path, validate_schema: bool = False) -> pd.DataFrame:
        """Load tabular data from CSV."""
        path = cls._validate_path(file_path)
        try:
            df = pd.read_csv(path)
        except Exception as e:
            raise DataLoaderError(f"Failed to parse CSV file '{path.name}': {e}") from e

        if validate_schema:
            cls.validate_shopping_schema(df)
        return df

    @classmethod
    def load_json(cls, file_path: str | Path) -> pd.DataFrame:
        """Load tabular records or nested objects from JSON."""
        path = cls._validate_path(file_path)
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                return pd.DataFrame(data)
            elif isinstance(data, dict):
                return pd.DataFrame([data])
            else:
                raise DataLoaderError(f"Unsupported JSON root type: {type(data)}")
        except json.JSONDecodeError as e:
            raise DataLoaderError(f"Invalid JSON in '{path.name}': {e}") from e
        except Exception as e:
            raise DataLoaderError(f"Failed to parse JSON file '{path.name}': {e}") from e

    @classmethod
    def load_xml(cls, file_path: str | Path) -> pd.DataFrame:
        """Load customer or tabular records from an XML tree structure."""
        path = cls._validate_path(file_path)
        try:
            tree = ET.parse(path)
            root = tree.getroot()
            rows = []
            for child in root:
                row = {sub.tag: sub.text for sub in child}
                if row:
                    rows.append(row)
            if not rows:
                raise DataLoaderError(f"No records found under XML root '{root.tag}' in '{path.name}'.")
            return pd.DataFrame(rows)
        except ET.ParseError as e:
            raise DataLoaderError(f"Invalid XML syntax in '{path.name}': {e}") from e
        except Exception as e:
            raise DataLoaderError(f"Failed to parse XML file '{path.name}': {e}") from e

    @classmethod
    def load_txt(cls, file_path: str | Path, delimiter: str | None = None) -> pd.DataFrame:
        """Load delimited tabular data from TXT (tab, comma, or pipe-separated)."""
        path = cls._validate_path(file_path)
        try:
            if delimiter:
                return pd.read_csv(path, sep=delimiter)
            # Auto-detect delimiter by inspecting header line
            with open(path, "r", encoding="utf-8") as f:
                header = f.readline()
            if "\t" in header:
                detected = "\t"
            elif "|" in header:
                detected = "|"
            elif "," in header:
                detected = ","
            else:
                detected = r"\s+"
            return pd.read_csv(path, sep=detected)
        except Exception as e:
            raise DataLoaderError(f"Failed to parse TXT file '{path.name}': {e}") from e

    @classmethod
    def validate_shopping_schema(cls, df: pd.DataFrame) -> bool:
        """Validate presence of expected shopping dataset columns."""
        missing = [col for col in cls.REQUIRED_SHOPPING_COLUMNS if col not in df.columns]
        if missing:
            raise DataLoaderError(f"Schema validation failed. Missing required columns: {missing}")
        return True
