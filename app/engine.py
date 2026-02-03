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
            dtype = self.schema.get(fname, "string")
            val = row[i] if i < len(row) else ""
            out[fname] = parse_value(val, dtype)
        return out

    def find_all(self) -> List[Dict[str, Any]]:
        rows = self._read_all_rows()
        return [self._wire_row(r) for r in rows]

    def find(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        all_rows = self.find_all()

        def matches(item):
            for k, v in query.items():
                if item.get(k) != v:
                    return False
            return True

        return [r for r in all_rows if matches(r)]

    def count(self) -> int:
        return len(self._read_all_rows())

    def delete_all(self):
        # remove csv file and recreate header
        if os.path.exists(self.csv_file):
            os.remove(self.csv_file)
        with open(self.csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(self.fields)

    def delete_one(self, query: Dict[str, Any]) -> bool:
        rows = self._read_all_rows()
        remaining = []
        deleted = False
        for row in rows:
            obj = self._wire_row(row)
            if not deleted and all(obj.get(k) == v for k, v in query.items()):
                deleted = True
                continue
            remaining.append(row)
        # write back
        with open(self.csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(self.fields)
            writer.writerows(remaining)
        return deleted

    def update_one(self, query: Dict[str, Any], data: Dict[str, Any]) -> bool:
        rows = self._read_all_rows()
        updated = False
        new_rows = []
        for row in rows:
            obj = self._wire_row(row)
            if not updated and all(obj.get(k) == v for k, v in query.items()):
                # apply updates
                for key, val in data.items():
                    if key in self.fields:
                        idx = self.fields.index(key)
                        row[idx] = stringify(val)
                updated = True
            new_rows.append(row)
        with open(self.csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(self.fields)
            writer.writerows(new_rows)
        return updated
