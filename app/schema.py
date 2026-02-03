from typing import Dict, List

ALLOWED_TYPES = {"string", "integer", "float", "boolean", "date"}


class SchemaValidationError(Exception):
    pass


class SchemaValidator:
    def __init__(self, schema: Dict[str, str]):
        self.schema = schema or {}
        self.fields = list(self.schema.keys())
        self.types = list(self.schema.values())
        self.validate_schema()

    def validate_schema(self):
        if not isinstance(self.schema, dict):
            raise SchemaValidationError("Schema must be a dict of field->type")
        for k, v in self.schema.items():
            if v not in ALLOWED_TYPES:
                raise SchemaValidationError(f"Unsupported type '{v}' for field '{k}'")

    def validate_record(self, record: List):
        # record may be a dict or list
        if isinstance(record, dict):
            # ensure keys match
            for key in record.keys():
                if key not in self.schema:
                    raise SchemaValidationError(f"Unknown field '{key}' in record")
            return True
        if isinstance(record, list):
            if len(record) != len(self.fields):
                raise SchemaValidationError(
                    f"Record length {len(record)} does not match schema fields {len(self.fields)}"
                )
            return True
        raise SchemaValidationError("Record must be a list or dict")

