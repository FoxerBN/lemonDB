# LemonDB 🍋

A lightweight, CSV-based database library for Python. Simple, minimal, and easy to use.

## Features

- **CSV-Based Storage**: No external database required
- **Simple API**: Intuitive methods like `save()`, `deleteOne()`, `deleteAll()`, `find()`, etc.
- **Schema Definition**: Define your data structure upfront
- **Easy Installation**: Install via `pip install lemonDB`
- **Minimal Dependencies**: Keep it lightweight and fast

## Installation

```bash
pip install lemonDB
```

## Quick Start

### 1. Define Your Schema

Create a schema that describes your data structure:

```python
from lemondb import LemonDB

# Define your schema (simple dictionary format)
schema = {
    "name": "string",
    "email": "string",
    "age": "integer",
    "active": "boolean"
}
```

### 2. Initialize Your Database

```python
# Create a LemonDB instance
db = LemonDB(name="myapp", engine="csv", schema=schema)
```

### 3. Save Data

```python
# Create a record matching your schema
user1 = ["Anna", "anna@example.com", 25, True]

# Save it
db.save(user1)
```

### 4. Query Data

```python
# Find records
results = db.find({"name": "Anna"})

# Find all
all_users = db.findAll()

# Delete one record
db.deleteOne({"name": "Anna"})

# Delete all records
db.deleteAll()

# Update records
db.updateOne({"name": "Anna"}, {"age": 26})

# Get count
count = db.count()
```

## Schema Format

Supported data types:

```python
schema = {
    "fieldName": "string",      # Text data
    "age": "integer",            # Whole numbers
    "salary": "float",           # Decimal numbers
    "active": "boolean",         # True/False
    "joined": "date"             # YYYY-MM-DD format
}
```

## Folder Structure

```
lemonDB/
├── README.md
├── setup.py
├── LICENSE
├── requirements.txt
├── lemondb/
│   ├── __init__.py
│   ├── core.py                  # Main LemonDB class
│   ├── schema.py                # Schema validation
│   ├── engine.py                # CSV engine
│   └── utils.py                 # Helper functions
├── tests/
│   ├── __init__.py
│   ├── test_save.py
│   ├── test_query.py
│   └── test_delete.py
└── examples/
    ├── basic_usage.py
    ├── user_database.py
    └── todo_app.py
```

## Example Usage

### Create a User Database

```python
from lemondb import LemonDB

# Define schema
user_schema = {
    "username": "string",
    "email": "string",
    "age": "integer",
    "premium": "boolean"
}

# Initialize
db = LemonDB(name="users", engine="csv", schema=user_schema)

# Add users
user1 = ["anna_teku", "anna@example.com", 25, True]
user2 = ["john_doe", "john@example.com", 30, False]

db.save(user1)
db.save(user2)

# Query
all_users = db.findAll()
premium_users = db.find({"premium": True})

# Delete
db.deleteOne({"username": "john_doe"})
```

## API Reference

### Core Methods

- **`save(record)`** - Insert a new record
- **`findAll()`** - Retrieve all records
- **`find(query)`** - Find records matching query
- **`deleteOne(query)`** - Delete first matching record
- **`deleteAll()`** - Delete all records
- **`updateOne(query, data)`** - Update first matching record
- **`updateAll(query, data)`** - Update all matching records
- **`count()`** - Get total record count

## Data Storage

Your data is stored as CSV files in a `lemondb_data/` directory:

```
lemondb_data/
├── myapp.csv          # Your database file
└── myapp_metadata.json # Schema and metadata
```

## Why LemonDB?

✨ **Minimal Setup** - No database server needed  
✨ **Human Readable** - CSV files you can open and read  
✨ **Perfect for Small Projects** - Prototypes, scripts, small apps  
✨ **Lightweight** - Minimal dependencies  

## Limitations

- Best suited for small datasets (< 50K records)
- Single file operations (not optimized for concurrent access)
- No complex joins or transactions

## Contributing

Contributions welcome! Feel free to submit issues and pull requests.

## License

MIT License - feel free to use in your projects!

---

**Happy coding! 🍋**