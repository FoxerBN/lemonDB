import os
import json
from datetime import datetime

DATA_DIR = "lemondb_data"


def set_data_dir(path: str):
    """Set custom data directory path"""
    global DATA_DIR
    DATA_DIR = path


def get_data_dir() -> str:
    """Get current data directory path"""
    return DATA_DIR


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
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d")
    return str(value)


def parse_value(value: str, dtype: str):
    if value == "":
        return None
    
    parsers = {
        "string": lambda v: v,
        "integer": int,
        "float": float,
        "boolean": lambda v: v.lower() in ("1", "true", "yes", "y"),
        "date": lambda v: datetime.strptime(v, "%Y-%m-%d").date()
    }
    
    try:
        return parsers.get(dtype, str)(value)
    except Exception:
        return value
