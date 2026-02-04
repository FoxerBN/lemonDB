# 🍋 lemonDB Documentation

> A lightweight, file-backed, schema-aware database in Python

---

## 📚 Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Quick Start](#quick-start)
4. [API Reference](#api-reference)
5. [Examples](#examples)
6. [Limitations](#limitations)

---

## Overview

**lemonDB** is a simple CSV-based database with schema validation. Perfect for small projects, prototypes, and learning.

**Key Features:**
- ✅ Schema validation with types (string, integer, float, boolean, date)
- ✅ Constraints: `required` and `unique` fields
- ✅ Simple CRUD operations
- ✅ Custom storage paths
- ✅ Helpful logging with 🍋 icons

**Storage:**
- Data: CSV files (one per collection)
- Metadata: JSON files (schema definitions)
- Default location: `./lemondb_data/`

---

## Architecture

### Component Structure

```
┌─────────────────────────────────────────────────┐
│  LemonDB (core.py)                              │
│  ↓ User-facing API                              │
│  • save(), find(), delete(), update()           │
│  • Orchestrates validation & persistence        │
└──────────────┬──────────────────────────────────┘
               ↓
┌──────────────┴──────────────────────────────────┐
│  SchemaValidator (schema.py)                    │
│  ↓ Validation layer                             │
│  • Type checking                                │
│  • Constraint enforcement (required, unique)    │
└──────────────┬──────────────────────────────────┘
               ↓
┌──────────────┴──────────────────────────────────┐
│  CSVEngine (engine.py)                          │
│  ↓ Persistence layer                            │
│  • File I/O operations                          │
│  • Query matching                               │
│  • Type conversion (CSV ↔ Python)               │
└──────────────┬──────────────────────────────────┘
               ↓
┌──────────────┴──────────────────────────────────┐
│  Utils (utils.py)                               │
│  • Path management                              │
│  • Data serialization                           │
└─────────────────────────────────────────────────┘
```

### Data Flow

**Save Operation:**
```
User → LemonDB.save() → Validate format → Check constraints → CSVEngine.save() → File
```

**Find Operation:**
```
File → CSVEngine.find() → Parse & type → Filter by query → Return results
```

---

## Quick Start

### Basic Usage

```python
from app import LemonDB

# Define schema
schema = {
    "username": "string",
    "email": "string",
    "age": "integer"
}

# Create database
db = LemonDB(name="users", schema=schema)
# 🍋 Schema 'users' was created

# Test connection
db.test()
# 🍋 DB 'users' is created and working!
# 🍋 Current records: 0
# 🍋 Schema fields: username, email, age

# Save records (as tuples/lists matching schema order)
db.save(
    ("Alice", "alice@example.com", 25),
    ("Bob", "bob@example.com", 30)
)
# 🍋 Saved 2 record(s) to 'users'

# Find all
users = db.findAll()
# [{'username': 'Alice', 'email': 'alice@example.com', 'age': 25}, ...]

# Query
alice = db.find({"username": "Alice"})

# Update
db.updateOne({"username": "Alice"}, {"age": 26})
# 🍋 Updated 1 record in 'users'

# Delete
db.deleteOne({"username": "Bob"})
# 🍋 Deleted 1 record from 'users'
```

### Custom Storage Path

```python
db = LemonDB(
    name="products",
    schema={"name": "string", "price": "float"},
    data_dir="/path/to/my/data"
)
# Files will be created at: /path/to/my/data/products.csv
```

### Schema with Constraints

```python
schema = {
    "id": {"type": "integer", "required": True, "unique": True},
    "email": {"type": "string", "required": True, "unique": True},
    "name": {"type": "string", "required": True},
    "active": {"type": "boolean"}
}

db = LemonDB(name="users", schema=schema)

# This will fail (missing required field)
db.save((None, "test@example.com", "Test"))  # ❌ SchemaValidationError

# This will fail (duplicate unique field)
db.save((1, "alice@test.com", "Alice", True))
db.save((2, "alice@test.com", "Alice2", True))  # ❌ SchemaValidationError
```

---

## API Reference

### Constructor

```python
LemonDB(name: str, engine: str = "csv", schema: dict, data_dir: str = None)
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | str | Yes | Collection name |
| `schema` | dict | Yes | Field definitions (see below) |
| `engine` | str | No | Storage engine (only "csv" supported) |
| `data_dir` | str | No | Custom storage path (default: `./lemondb_data/`) |

**Schema Format:**
```python
# Simple: field -> type
schema = {
    "username": "string",
    "age": "integer"
}

# Advanced: field -> options
schema = {
    "id": {"type": "integer", "required": True, "unique": True},
    "email": {"type": "string", "unique": True}
}
```

**Allowed Types:** `string`, `integer`, `float`, `boolean`, `date`

---

### Methods

#### `save(*records, raise_on_error=True) -> int`
Save one or more records.

```python
db.save(("Alice", 25))              # Single record
db.save(("Alice", 25), ("Bob", 30)) # Multiple records
```

**Returns:** Number of records saved  
**Logs:** `🍋 Saved X record(s) to 'name'`

---

#### `findAll() -> list[dict]`
Get all records.

```python
all_users = db.findAll()
# [{'username': 'Alice', 'age': 25}, ...]
```

---

#### `find(query: dict) -> list[dict]`
Query records.

```python
results = db.find({"age": 25})
results = db.find({"username": "Alice", "age": 25})
```

---

#### `deleteOne(query: dict) -> bool`
Delete first matching record.

```python
db.deleteOne({"username": "Alice"})  # Returns True if deleted
```

**Logs:** `🍋 Deleted 1 record` or `🍋 No records matched`

---

#### `deleteAll()`
Delete all records.

```python
db.deleteAll()
```

**Logs:** `🍋 Deleted X record(s) from 'name'`

---

#### `updateOne(query: dict, data: dict) -> bool`
Update first matching record.

```python
db.updateOne({"username": "Alice"}, {"age": 26})
```

**Logs:** `🍋 Updated 1 record` or `🍋 No records matched`

---

#### `count() -> int`
Count records.

```python
total = db.count()
```

---

#### `test()`
Test database status.

```python
db.test()
# 🍋 DB 'users' is created and working!
# 🍋 Current records: 5
# 🍋 Schema fields: username, email, age
```

---

## Examples

### Example 1: Simple Todo List

```python
from app import LemonDB

schema = {
    "id": {"type": "integer", "required": True, "unique": True},
    "task": {"type": "string", "required": True},
    "done": {"type": "boolean"}
}

todos = LemonDB("todos", schema=schema)

# Add tasks
todos.save(
    (1, "Buy groceries", False),
    (2, "Learn Python", False),
    (3, "Exercise", False)
)

# Mark as done
todos.updateOne({"id": 2}, {"done": True})

# Find incomplete
incomplete = todos.find({"done": False})
print(f"You have {len(incomplete)} tasks remaining")

# Complete a task
todos.deleteOne({"id": 1})
```

### Example 2: Multi-Database Setup

```python
# User database
users_db = LemonDB("users", schema={"name": "string", "email": "string"})

# Products in custom location
products_db = LemonDB(
    "products",
    schema={"name": "string", "price": "float", "stock": "integer"},
    data_dir="./inventory_data"
)

# Activity logs
logs_db = LemonDB(
    "logs",
    schema={"timestamp": "string", "action": "string"},
    data_dir="/var/logs/app"
)
```

### Example 3: Error Handling

```python
# Save with error handling
results = db.save(
    ("Alice", "alice@test.com"),
    ("Bob", None),  # Missing required email
    ("Charlie", "charlie@test.com"),
    raise_on_error=False
)
# Output:
# Skipping record ('Bob', None): Field 'email' is required
# 🍋 Saved 2 record(s) to 'users'
```

---

## Limitations

⚠️ **Not suitable for:**
- Large datasets (uses full table scans)
- Concurrent access (no locking mechanism)
- Production systems (toy database for learning/prototyping)

✅ **Good for:**
- Small projects & prototypes
- Configuration storage
- Simple data persistence
- Learning database concepts

---

## File Structure

After creating a database:

```
lemondb_data/
├── users.csv                  # Data records
├── users_metadata.json        # Schema definition
├── products.csv
└── products_metadata.json
```

**users.csv:**
```csv
username,email,age
Alice,alice@example.com,25
Bob,bob@example.com,30
```

**users_metadata.json:**
```json
{
  "schema": {
    "username": "string",
    "email": "string",
    "age": "integer"
  }
}
```

---

## Code Improvements

This version includes several refactorings:

1. **Modular validation** - Separated format checking from constraint validation
2. **DRY principles** - Reusable query matching across find/delete/update
3. **Centralized I/O** - Single method for CSV writes
4. **Logging** - All operations provide feedback with 🍋 icons
5. **Custom paths** - Flexible storage locations

**Total Lines:** 357 (core: 113, engine: 110, schema: 73, utils: 61)

---

## Running Tests


```bash
# Test database creation
python3 -m tests.test_creation

# Test count function
python3 -m tests.test_count

# Test db.test() method
python3 -m tests.test_db_test
```

---

## Running Examples

```bash
# Save operations
python3 -m examples.example_save

# Find/query operations
python3 -m examples.example_find

# Update operations
python3 -m examples.example_update

# Delete operations
python3 -m examples.example_delete

# Complete todo app
python3 -m examples.todo_app
```

---

## Project Structure

```
lemonDB/
├── README.md                    # Project readme
├── docs.md                      # Full documentation (this file)
├── LICENSE                      # MIT License
├── setup.py                     # Package setup
├── requirements.txt             # Dependencies
├── .gitignore                   # Git ignore rules
│
├── app/                         # Main package
│   ├── __init__.py             # Package init
│   ├── core.py                 # LemonDB main class
│   ├── schema.py               # Schema validation
│   ├── engine.py               # CSV storage engine
│   └── utils.py                # Helper utilities
│
├── tests/                       # Test files
│   ├── __init__.py
│   ├── test_creation.py        # Test database creation
│   ├── test_count.py           # Test count function
│   └── test_db_test.py         # Test db.test() method
│
└── examples/                    # Usage examples
    ├── example_save.py         # Save operations demo
    ├── example_find.py         # Query operations demo
    ├── example_update.py       # Update operations demo
    ├── example_delete.py       # Delete operations demo
    └── todo_app.py             # Complete todo application
```

---

**Made with 🍋 by lemonDB**
