import csv
import os
from typing import List, Dict, Any

from .utils import csv_path, metadata_path, read_metadata, write_metadata, stringify, parse_value


class CSVEngine:
    def __init__(self, name: str, schema: Dict[str, str]):
        self.name = name
        self.schema = schema
        self.fields = list(schema.keys())
        self.csv_file = csv_path(name)
        self.meta_file = metadata_path(name)
        self._ensure_files()

    def _ensure_files(self):
        # ensure metadata exists
        meta = read_metadata(self.name)
        if not meta:
            write_metadata(self.name, {"schema": self.schema})
        # ensure csv header
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(self.fields)

    def save(self, record: List[Any]):
        # record is list aligned with fields
        with open(self.csv_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            row = [stringify(v) for v in record]
            writer.writerow(row)

    def _read_all_rows(self) -> List[List[str]]:
        rows = []
        if not os.path.exists(self.csv_file):
            return rows
        with open(self.csv_file, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                if i == 0:
                    continue
                rows.append(row)
        return rows

    def _wire_row(self, row: List[str]) -> Dict[str, Any]:
        out = {}
        for i, fname in enumerate(self.fields):
            schema_def = self.schema.get(fname, "string")
            # Handle both simple string type and dict with type key
            if isinstance(schema_def, dict):
                dtype = schema_def.get("type", "string")
            else:
                dtype = schema_def
            val = row[i] if i < len(row) else ""
            out[fname] = parse_value(val, dtype)
        return out

    def find_all(self) -> List[Dict[str, Any]]:
        rows = self._read_all_rows()
        return [self._wire_row(r) for r in rows]

    def find(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [row for row in self.find_all() if self._matches_query(row, query)]

    def _matches_query(self, row: Dict[str, Any], query: Dict[str, Any]) -> bool:
        return all(row.get(key) == value for key, value in query.items())

    def count(self) -> int:
        return len(self._read_all_rows())

    def delete_all(self):
        if os.path.exists(self.csv_file):
            os.remove(self.csv_file)
        self._write_rows([])

    def delete_one(self, query: Dict[str, Any]) -> bool:
        rows = self._read_all_rows()
        remaining = []
        deleted = False
        
        for row in rows:
            obj = self._wire_row(row)
            if not deleted and self._matches_query(obj, query):
                deleted = True
                continue
            remaining.append(row)
        
        self._write_rows(remaining)
        return deleted

    def update_one(self, query: Dict[str, Any], data: Dict[str, Any]) -> bool:
        rows = self._read_all_rows()
        updated = False
        new_rows = []
        
        for row in rows:
            obj = self._wire_row(row)
            if not updated and self._matches_query(obj, query):
                for key, val in data.items():
                    if key in self.fields:
                        idx = self.fields.index(key)
                        row[idx] = stringify(val)
                updated = True
            new_rows.append(row)
        
        self._write_rows(new_rows)
        return updated

    def _write_rows(self, rows: List[List[str]]):
        with open(self.csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(self.fields)
            writer.writerows(rows)
