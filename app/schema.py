from typing import Dict, List, Set, Any

ALLOWED_TYPES = {"string", "integer", "float", "boolean", "date"}


class SchemaValidationError(Exception):
    pass


class SchemaValidator:
    def __init__(self, schema: Dict[str, Any]):
        self.schema_raw = schema or {}
        self._normalize()
        self.validate_schema()

    def _normalize(self):
        self.fields = list(self.schema_raw.keys())
        self.types = {}
        self.constraints = {}
        
        for field, definition in self.schema_raw.items():
            if isinstance(definition, str):
                self.types[field] = definition
                self.constraints[field] = {"required": False, "unique": False}
            elif isinstance(definition, dict):
                self.types[field] = definition.get("type")
                self.constraints[field] = {
                    "required": bool(definition.get("required", False)),
                    "unique": bool(definition.get("unique", False))
                }
            else:
                self.types[field] = None
                self.constraints[field] = {"required": False, "unique": False}

    def validate_schema(self):
        if not isinstance(self.schema_raw, dict) or not self.schema_raw:
            raise SchemaValidationError("Schema must be a non-empty dict of field->type or field->options")
        
        for field, definition in self.schema_raw.items():
            dtype = definition if isinstance(definition, str) else definition.get("type")
            
            if dtype not in ALLOWED_TYPES:
                raise SchemaValidationError(f"Unsupported type '{dtype}' for field '{field}'")
            
            if isinstance(definition, dict):
                if "required" in definition and not isinstance(definition.get("required"), bool):
                    raise SchemaValidationError(f"'required' for field '{field}' must be boolean")
                if "unique" in definition and not isinstance(definition.get("unique"), bool):
                    raise SchemaValidationError(f"'unique' for field '{field}' must be boolean")

    def validate_record_format(self, record: List):
        if not isinstance(record, (list, tuple)):
            raise SchemaValidationError("Record must be a list or tuple aligned with schema fields")
        if len(record) != len(self.fields):
            raise SchemaValidationError(
                f"Record length {len(record)} does not match schema fields {len(self.fields)}"
            )

    def validate_constraints(self, record: List, existing_values: Dict[str, Set], seen_in_batch: Dict[str, Set]):
        for idx, field in enumerate(self.fields):
            value = record[idx]
            constraints = self.constraints.get(field, {})
            
            if constraints.get("required") and (value is None or (isinstance(value, str) and value == "")):
                raise SchemaValidationError(f"Field '{field}' is required but missing in record")
            
            if constraints.get("unique"):
                if value in existing_values.get(field, set()) or value in seen_in_batch.get(field, set()):
                    raise SchemaValidationError(f"Unique constraint violated for field '{field}': {value}")
                seen_in_batch[field].add(value)

    def get_unique_fields(self) -> List[str]:
        return [field for field, constraints in self.constraints.items() if constraints.get("unique")]
