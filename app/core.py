from typing import List, Dict, Any, Optional

from .schema import SchemaValidator, SchemaValidationError
from .engine import CSVEngine


class LemonDB:
    def __init__(self, name: str, engine: str = "csv", schema: Optional[Dict[str, str]] = None):
        if engine != "csv":
            raise ValueError("Only 'csv' engine is supported in this implementation")
        self.name = name
        self.schema = schema or {}
        self.validator = SchemaValidator(self.schema)
        self.engine = CSVEngine(name, self.schema)

    def save(self, record: List[Any]):
        # allow dict or list
        try:
            self.validator.validate_record(record)
        except SchemaValidationError as e:
            raise
        if isinstance(record, dict):
            # convert dict to list in field order
            row = [record.get(f) for f in self.validator.fields]
        else:
            row = record
        self.engine.save(row)

    def findAll(self) -> List[Dict[str, Any]]:
        return self.engine.find_all()

    def find(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        return self.engine.find(query)

    def deleteOne(self, query: Dict[str, Any]) -> bool:
        return self.engine.delete_one(query)

    def deleteAll(self):
        return self.engine.delete_all()

    def updateOne(self, query: Dict[str, Any], data: Dict[str, Any]) -> bool:
        return self.engine.update_one(query, data)

    def count(self) -> int:
        return self.engine.count()