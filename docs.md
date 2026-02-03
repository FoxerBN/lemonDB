lemonDB - Documentation

Project overview

lemonDB is a tiny, file-backed, schema-aware toy database implemented in Python. It stores records in CSV files under a local data directory (`lemondb_data`) and keeps collection metadata (currently only the schema) as a JSON file per collection.

This repo contains four main modules under `app/`:
- `core` — high-level user-facing API (LemonDB class) that validates against a schema and delegates persistence to an engine.
- `engine` — the storage engine implementation; this project ships a `CSVEngine` that reads/writes CSV files and manages headers.
- `schema` — schema validation utilities (allowed types, record validation).
- `utils` — filesystem helpers, metadata read/write, and conversion helpers (stringify/parse).

This document explains each module, the public API, storage format, examples, edge cases, and suggested next steps.

Quickstart example

1. Define a schema (dict: field -> type):

```python
schema = {
    "username": "string",
    "email": "string",
    "age": "integer",
    "premium": "boolean",
    "signup_date": "date",
}

from app import LemonDB

db = LemonDB(name="users", engine="csv", schema=schema)

user1 = ["Andrea Blinova", "adka95652@gmail.com", 23, True, "2023-08-15"]

db.save(user1)
```

2. The data will be written to `lemondb_data/users.csv` and `lemondb_data/users_metadata.json`.

Module: app.core

Public symbol: LemonDB

Purpose
- Provide a simple, familiar API for saving and querying records while enforcing a schema.
- Delegate low-level persistence details to an engine implementation.

Constructor
- LemonDB(name: str, engine: str = "csv", schema: Optional[Dict[str, str]] = None)
  - name: collection name; used to build data file paths
  - engine: currently only "csv" is supported (ValueError if other)
  - schema: mapping field -> type (allowed types described in `schema` module)
  - Internally: creates a SchemaValidator and a CSVEngine instance.

Methods
- save(record: List[Any] | Dict[str, Any])
  - Accepts either a list aligned with schema field order, or a dict of field->value.
  - Validates record with SchemaValidator.validate_record (raises SchemaValidationError on mismatch).
  - If a dict is provided, converts it to a list following the schema field order before delegating to the engine.

- findAll() -> List[Dict[str, Any]]
  - Returns all records as a list of dicts (field -> typed value) by calling engine.find_all().

- find(query: Dict[str, Any]) -> List[Dict[str, Any]]
  - Returns matching records where all query key/value pairs are equal to record values.

- deleteOne(query: Dict[str, Any]) -> bool
  - Deletes the first record matching the query and returns True if a deletion occurred.

- deleteAll()
  - Removes all records for the collection (recreates CSV header).

- updateOne(query: Dict[str, Any], data: Dict[str, Any]) -> bool
  - Finds the first matching record and applies in-place updates for fields present in data (only known fields). Returns True if at least one row was updated.

- count() -> int
  - Returns the number of stored records (excluding header).

Notes and behavior
- LemonDB performs schema validation before saving.
- Errors raised by SchemaValidator (SchemaValidationError) or engine I/O propagate to callers.

Module: app.engine

Public symbol: CSVEngine

Purpose
- A simple CSV-backed engine that stores one collection per CSV file.
- Manages a companion metadata JSON file that contains the schema and future metadata.

Constructor
- CSVEngine(name: str, schema: Dict[str, str])
  - Builds file paths (CSV and metadata) via utils.csv_path/metadata_path and ensures files/headers exist.

Key internal attributes
- name: collection name
- schema: schema map
- fields: list(schema.keys()) (header order)
- csv_file: path to CSV file
- meta_file: path to metadata JSON

Important methods
- _ensure_files():
  - Writes metadata JSON if missing (writes {"schema": schema}).
  - Creates the CSV file and writes the header row if missing.

- save(record: List[Any])
  - Appends a CSV row. Values are passed through `utils.stringify` to serialize booleans, numbers, and dates.

- _read_all_rows() -> List[List[str]]
  - Reads raw CSV rows (skips header). Returns list of rows as lists of strings.

- _wire_row(row: List[str]) -> Dict[str, Any]
  - Combines a raw CSV row with `fields` and converts each cell to its typed Python value using `utils.parse_value`.
  - If a row is shorter than the header, missing columns are treated as empty strings.

- find_all() -> List[Dict[str, Any]]
  - Returns all records as typed dicts by mapping _wire_row over read rows.

- find(query: Dict[str, Any]) -> List[Dict[str, Any]]
  - Returns records where every key in `query` equals the record's corresponding value.
  - Comparison uses Python equality (==) on parsed Python types.

- count() -> int
  - Returns number of data rows (skips header).

- delete_all()
  - Deletes the CSV file and recreates it with only the header row.

- delete_one(query: Dict[str, Any]) -> bool
  - Iterates rows and deletes the first that matches the query. Writes remaining rows back and returns True if something was deleted. Matching uses typed values after `_wire_row`.

- update_one(query: Dict[str, Any], data: Dict[str, Any]) -> bool
  - Finds the first row matching the query, updates the CSV row's relevant columns by stringifying the new values, and writes everything back. Returns True if update applied.

Storage format
- Data directory: `lemondb_data/` (created when needed by utils.ensure_data_dir()).
- CSV file: `<name>.csv` with header row of fields.
- Metadata file: `<name>_metadata.json`, currently contains {"schema": {..}}.

Concurrency and limitations
- CSVEngine rewrites the whole CSV file for delete_one and update_one. There is no locking; concurrent access may corrupt files.
- No transactionality or atomic multi-row operations.
- Search is full-table scan (reads entire CSV into memory). Not suitable for large datasets.

Module: app.schema

Public symbols: SchemaValidator, SchemaValidationError

Purpose
- Validate schema definitions and incoming records against the schema.
- Provide a list of allowed primitive types and basic validation.

Allowed types
- "string", "integer", "float", "boolean", "date"

SchemaValidator class
- Constructor: SchemaValidator(schema: Dict[str, str])
  - Stores schema, builds `fields` and `types` lists, and calls `validate_schema()`.

- validate_schema()
  - Ensures the provided schema is a dict and that every declared type is one of allowed types.
  - Raises SchemaValidationError on invalid schema.

- validate_record(record: List | Dict)
  - Accepts either a dict or list record:
    - If dict: ensures every key in the dict exists in the schema (extra keys are rejected).
    - If list: ensures the list length equals the number of schema fields.
  - Raises SchemaValidationError for invalid records; returns True if OK.

Notes
- validate_record does not type-check values (e.g., that a value declared as integer is actually an int). The engine's parsing is responsible for converting stored strings back to typed values on read.

Module: app.utils

Purpose
- Small helpers for filesystem paths, metadata I/O, and converting between Python types and string representation for CSV storage.

Public functions
- ensure_data_dir() -> str
  - Ensures `lemondb_data` directory exists; returns the directory path.

- metadata_path(name: str) -> str
  - Returns path to metadata JSON for `name` and ensures data directory exists.

- csv_path(name: str) -> str
  - Returns path to CSV file for `name` and ensures data directory exists.

- write_metadata(name: str, metadata: dict)
  - Writes JSON metadata pretty-printed (indent=2) to metadata file.

- read_metadata(name: str) -> dict
  - Reads metadata JSON and returns the dict or {} if file is missing.

- stringify(value) -> str
  - Serializes values to strings for CSV storage:
    - None -> ""
    - bool -> "true"/"false"
    - int/float -> decimal string
    - datetime/date -> formatted as YYYY-MM-DD
    - otherwise -> str(value)

- parse_value(value: str, dtype: str) -> Any
  - Parses a CSV cell string back into a Python value according to dtype:
    - "" -> None
    - string -> returned as-is
    - integer -> int()
    - float -> float()
    - boolean -> True for ("1","true","yes","y") (case-insensitive), otherwise False
    - date -> parsed via datetime.strptime(...).date()
  - If parsing raises any exception, the raw string is returned as a fallback.

Examples and file contents

Given the quickstart above, files created look like:

lemondb_data/users_metadata.json
{
  "schema": {
    "username": "string",
    "email": "string",
    "age": "integer",
    "premium": "boolean",
    "signup_date": "date"
  }
}

lemondb_data/users.csv
username,email,age,premium,signup_date
Andrea Blinova,adka95652@gmail.com,23,true,2023-08-15

Edge cases and behavior summary

- Empty values: an empty field is stored as an empty string and parsed back as None.
- Type coercion: parse_value attempts conversion and returns the raw string if conversion fails (so malformed integers remain strings on read).
- Dict save: passing a dict to LemonDB.save will only save keys that exist in the schema and will preserve field order defined by the schema when converting to a CSV row.
- Extra keys in dict save: validate_record rejects records that contain unknown keys (SchemaValidationError).
- Partial rows: if the CSV contains shorter rows than the header, missing columns are treated as empty and parsed to None.
- Boolean parsing: many common truthy strings map to True; anything else maps to False when dtype is "boolean".

Limitations

- Single-engine (CSV) implementation. The code is designed so future engines could be added, but only "csv" is allowed in `LemonDB` currently.
- No concurrency controls or atomic file writes; not safe for concurrent writers.
- Full table scans for queries and updates; not appropriate for large datasets.
- No schema migrations or evolution handling.

Next steps and suggested improvements

- Add file locking or atomic replace-write (write to temp & rename) to reduce race conditions.
- Add a context manager or transaction abstraction for atomic multi-step operations.
- Introduce indexes and incremental reading for large datasets.
- Add schema type enforcement on write to reject or coerce bad values earlier.
- Provide an append-only WAL or journaling to improve durability.

How to run tests / try the project

- The repository provides `test/run_test.py` demonstrating basic usage. To run it:

```bash
python test/run_test.py
```

- Or import and use from Python:

```python
from app import LemonDB
# ...follow quickstart above
```

Requirements coverage

- Docs explain `core` (LemonDB), `engine` (CSVEngine), `schema` (SchemaValidator), and `utils` (I/O and parsing) — Done.

If you want, I can also:
- Generate a shorter Quickstart README or add inline examples to each module file.
- Add unit tests that assert current behavior (save/find/update/delete) so docs and code remain synchronized.


