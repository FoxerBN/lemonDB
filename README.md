# lemoDB

A lightweight, schema-aware, CSV-based database for Python.

## Installation

```bash
pip install lemoDB
```

## Quick Start

```python
from lemoDB import LemonDB

# Define schema
schema = {
    "username": "string",
    "email": "string",
    "age": "integer"
}

# Create database
db = LemonDB(name="users", schema=schema)

# Save records
db.save(
    ("alice", "alice@example.com", 25),
    ("bob", "bob@example.com", 30)
)

# Query data
users = db.findAll()
alice = db.find({"username": "alice"})

# Update
db.updateOne({"username": "alice"}, {"age": 26})

# Delete
db.deleteOne({"username": "bob"})
```

## Features

- Schema validation with type checking
- Auto-increment IDs
- Simple CRUD operations
- CSV-based storage
- Zero external dependencies
