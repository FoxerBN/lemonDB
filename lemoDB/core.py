from typing import List, Dict, Any

from .schema import SchemaValidator, SchemaValidationError
from .engine import CSVEngine
LEMON = "🍋"


class LemonDB:
    def __init__(self, name: str, engine: str = "csv", schema: Dict[str, str] = None, data_dir: str = None, auto_id: bool = True):
        if not isinstance(schema, dict) or not schema:
            raise ValueError("A non-empty schema dict is required (field->type)")
        if engine != "csv":
            raise ValueError("Only 'csv' engine is supported in this implementation")
        
        # Set custom data directory if provided
        if data_dir:
            from .utils import set_data_dir
            set_data_dir(data_dir)
        
        self.name = name
        self.auto_id = auto_id
        
        # Add 'id' field to schema if auto_id is enabled
        if self.auto_id and 'id' not in schema:
            self.schema = {"id": {"type": "integer", "required": True, "unique": True}}
            self.schema.update(schema)
        else:
            self.schema = schema
        
        self.validator = SchemaValidator(self.schema)
        self.engine = CSVEngine(name, self.schema)
        print(f"{LEMON} Schema '{name}' was created")

    def _get_next_id(self) -> int:
        """Get next available ID"""
        existing = self.engine.find_all()
        if not existing:
            return 1
        # Convert ID to int if it's string
        ids = []
        for record in existing:
            id_val = record.get('id', 0)
            if isinstance(id_val, str):
                try:
                    ids.append(int(id_val))
                except ValueError:
                    ids.append(0)
            else:
                ids.append(id_val)
        max_id = max(ids) if ids else 0
        return max_id + 1

    def save(self, *records: List[Any], raise_on_error: bool = True) -> int:
        """
        Save one or more records. 
        If auto_id is enabled, automatically adds ID at the beginning of each record.
        Records should NOT include ID when auto_id=True.
        Enforces `required` and `unique` constraints from the schema.
        If `raise_on_error` is False, constraint violations are skipped and saving proceeds.
        Returns number of records saved.
        """
        if not records:
            raise SchemaValidationError("No records provided to save")

        # Process records with auto ID if enabled
        processed_records = []
        if self.auto_id:
            next_id = self._get_next_id()
            for record in records:
                # Prepend ID to record
                record_with_id = [next_id] + list(record)
                processed_records.append(record_with_id)
                next_id += 1
        else:
            processed_records = list(records)

        existing_values = self._load_unique_values()
        seen_in_batch = {field: set() for field in self.validator.get_unique_fields()}

        saved = 0
        for record in processed_records:
            if self._try_save_record(record, existing_values, seen_in_batch, raise_on_error):
                saved += 1
        
        print(f"{LEMON} Saved {saved} record(s) to '{self.name}'")
        return saved

    def _load_unique_values(self):
        existing_rows = self.engine.find_all()
        unique_fields = self.validator.get_unique_fields()
        existing_values = {field: set() for field in unique_fields}
        
        for row in existing_rows:
            for field in unique_fields:
                existing_values[field].add(row.get(field))
        
        return existing_values

    def _try_save_record(self, record, existing_values, seen_in_batch, raise_on_error):
        try:
            if not isinstance(record, (list, tuple)):
                raise SchemaValidationError(
                    "Records must be list or tuple aligned with schema fields; dict/kwargs are not accepted"
                )
            
            self.validator.validate_record_format(record)
            self.validator.validate_constraints(record, existing_values, seen_in_batch)
            
            self.engine.save(list(record))
            return True
        except SchemaValidationError as e:
            if raise_on_error:
                raise
            print(f"Skipping record {record}: {e}")
            return False

    def findAll(self) -> List[Dict[str, Any]]:
        return self.engine.find_all()

    def find(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        return self.engine.find(query)
    
    def findById(self, id: int) -> Dict[str, Any]:
        """Find record by ID (convenience method)"""
        results = self.engine.find({"id": id})
        return results[0] if results else None

    def deleteOne(self, query: Dict[str, Any]) -> bool:
        result = self.engine.delete_one(query)
        if result:
            print(f"{LEMON} Deleted 1 record from '{self.name}'")
        else:
            print(f"{LEMON} No records matched the query in '{self.name}'")
        return result

    def deleteAll(self):
        count = self.count()
        result = self.engine.delete_all()
        print(f"{LEMON} Deleted {count} record(s) from '{self.name}'")
        return result

    def updateOne(self, query: Dict[str, Any], data: Dict[str, Any]) -> bool:
        result = self.engine.update_one(query, data)
        if result:
            print(f"{LEMON} Updated 1 record in '{self.name}'")
        else:
            print(f"{LEMON} No records matched the query in '{self.name}'")
        return result

    def count(self) -> int:
        return self.engine.count()

    def test(self):
        """Test if database is created and working"""
        count = self.count()
        print(f"{LEMON} DB '{self.name}' is created and working!{LEMON}")
        print(f"{LEMON} Current records: {count}{LEMON}")
        print(f"{LEMON} Schema fields: {', '.join(self.validator.fields)}{LEMON}")
        return True