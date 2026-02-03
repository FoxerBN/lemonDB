import os
import json
import csv
from datetime import datetime

DATA_DIR = "lemondb_data"


def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)
    return DATA_DIR


def metadata_path(name: str) -> str:
    ensure_data_dir()
    return os.path.join(DATA_DIR, f"{name}_metadata.json")


def csv_path(name: str) -> str:
    ensure_data_dir()
    return os.path.join(DATA_DIR, f"{name}.csv")


def write_metadata(name: str, metadata: dict):
    path = metadata_path(name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)


def read_metadata(name: str) -> dict:
    path = metadata_path(name)
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def stringify(value):
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, (datetime,)):
        return value.strftime("%Y-%m-%d")
    return str(value)


def parse_value(value: str, dtype: str):
    if value == "":
        return None
    try:
        if dtype == "string":
            return value
        if dtype == "integer":
            return int(value)
        if dtype == "float":
            return float(value)
        if dtype == "boolean":
            lower = value.lower()
            return lower in ("1", "true", "yes", "y")
        if dtype == "date":
            return datetime.strptime(value, "%Y-%m-%d").date()
    except Exception:
        # on parse error return raw string
        return value
    return value

