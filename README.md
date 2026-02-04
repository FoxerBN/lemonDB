<div align="center">

# 🍋 LemonDB

### *A lightweight, schema-aware database in Python*

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![CSV](https://img.shields.io/badge/Storage-CSV-orange.svg)]()

*Simple • Fast • Readable • Perfect for Small Projects*

[Features](#-features) •
[Quick Start](#-quick-start) •
[Documentation](docs.md) •
[Examples](#-examples)

</div>

---

## 🌟 Features

- **🎯 Schema Validation** - Define types and constraints (`required`, `unique`)
- **📝 Simple API** - Intuitive CRUD operations
- **📦 CSV Storage** - Human-readable files, no external database
- **🔍 Easy Queries** - Find records with simple dict queries
- **🍋 Helpful Logging** - All operations log with lemon icons
- **📂 Custom Paths** - Store databases anywhere you want
- **⚡ Zero Dependencies** - Uses only Python standard library

---

## 🚀 Quick Start

### Installation

```bash
pip install lemonDB
```

### Basic Example

```python
from app import LemonDB

# 1. Define schema
schema = {
    "username": "string",
    "email": "string",
    "age": "integer"
}

# 2. Create database
db = LemonDB(name="users", schema=schema)
# 🍋 Schema 'users' was created

# 3. Save records (as tuples matching schema order)
db.save(
    ("alice", "alice@example.com", 25),
    ("bob", "bob@example.com", 30)
)
# 🍋 Saved 2 record(s) to 'users'

# 4. Query data
users = db.findAll()
print(users)
# [{'username': 'alice', 'email': 'alice@example.com', 'age': 25}, ...]

# 5. Find specific records
alice = db.find({"username": "alice"})

# 6. Update
db.updateOne({"username": "alice"}, {"age": 26})
# 🍋 Updated 1 record in 'users'

# 7. Delete
db.deleteOne({"username": "bob"})
# 🍋 Deleted 1 record from 'users'
```

---

## 📖 Schema Definition

### Simple Schema

```python
schema = {
    "name": "string",
    "age": "integer",
    "score": "float",
    "active": "boolean",
    "joined": "date"
}
```

**Supported Types:** `string`, `integer`, `float`, `boolean`, `date`

### Advanced Schema with Constraints

```python
schema = {
    "id": {"type": "integer", "required": True, "unique": True},
    "email": {"type": "string", "required": True, "unique": True},
    "name": {"type": "string", "required": True},
    "active": {"type": "boolean"}
}
```

**Constraints:**
- `required: True` - Field cannot be empty or None
- `unique: True` - Field must be unique across all records

---

## 💡 Examples

### Example 1: Todo List

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

# Find incomplete tasks
incomplete = todos.find({"done": False})
print(f"You have {len(incomplete)} tasks left!")
```

### Example 2: Custom Storage Path

```python
# Store in custom location
db = LemonDB(
    name="products",
    schema={"name": "string", "price": "float"},
    data_dir="/path/to/my/data"
)

db.save(("Laptop", 999.99), ("Mouse", 25.50))
# Files created at: /path/to/my/data/products.csv
```

### Example 3: Multiple Databases

```python
# User database
users_db = LemonDB("users", schema={"name": "string", "email": "string"})

# Products database
products_db = LemonDB(
    "products",
    schema={"name": "string", "price": "float", "stock": "integer"},
    data_dir="./inventory"
)

# Activity logs
logs_db = LemonDB(
    "logs",
    schema={"timestamp": "string", "action": "string"},
    data_dir="/var/logs"
)
```

---

## 📚 API Reference

| Method | Description | Example |
|--------|-------------|---------|
| `save(*records)` | Save one or more records | `db.save(("Alice", 25))` |
| `findAll()` | Get all records | `db.findAll()` |
| `find(query)` | Query records | `db.find({"age": 25})` |
| `deleteOne(query)` | Delete first match | `db.deleteOne({"name": "Alice"})` |
| `deleteAll()` | Delete all records | `db.deleteAll()` |
| `updateOne(query, data)` | Update first match | `db.updateOne({"id": 1}, {"age": 26})` |
| `count()` | Count records | `db.count()` |
| `test()` | Test database status | `db.test()` |

**[Full Documentation →](docs.md)**

---

## 📂 Project Structure

```
lemonDB/
├── README.md                    # This file
├── docs.md                      # Full documentation
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
│   ├── test_creation.py        # Test db creation
│   ├── test_count.py           # Test count function
│   └── test_db_test.py         # Test db.test() method
│
└── examples/                    # Usage examples
    ├── example_save.py         # Save operations
    ├── example_find.py         # Query operations
    ├── example_update.py       # Update operations
    ├── example_delete.py       # Delete operations
    └── todo_app.py             # Complete todo app
```

### Running Tests

```bash
# Test database creation
python3 -m tests.test_creation

# Test count function
python3 -m tests.test_count

# Test db.test() method
python3 -m tests.test_db_test
```

### Running Examples

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

```
lemondb_data/
├── users.csv                  # Your data
├── users_metadata.json        # Schema definition
├── products.csv
└── products_metadata.json
```

**Example CSV:**
```csv
username,email,age
alice,alice@example.com,25
bob,bob@example.com,30
```

---

## 🎯 Use Cases

✅ **Perfect for:**
- Small to medium projects (< 10K records)
- Prototypes and MVPs
- Configuration storage
- Learning database concepts
- Simple data persistence

⚠️ **Not suitable for:**
- Large datasets (no indexing)
- Concurrent access (no locking)
- Production systems requiring high performance

---

## 🔧 Advanced Features

### Error Handling

```python
# Skip invalid records instead of raising errors
db.save(
    ("Alice", "alice@test.com"),
    ("Bob", None),  # Missing required field
    ("Charlie", "charlie@test.com"),
    raise_on_error=False
)
# Skipping record ('Bob', None): Field 'email' is required
# 🍋 Saved 2 record(s) to 'users'
```

### Database Testing

```python
db.test()
# 🍋 DB 'users' is created and working!
# 🍋 Current records: 5
# 🍋 Schema fields: username, email, age
```

---

## 📊 Performance

- **Small datasets** (< 1K records): ⚡ Instant
- **Medium datasets** (1K - 10K records): 🏃 Fast
- **Large datasets** (> 10K records): 🐌 Slower (uses full table scans)

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- 🐛 Report bugs
- 💡 Suggest features
- 🔧 Submit pull requests

---

## 📄 License

MIT License - Use freely in your projects!


---

<div align="center">

**[⬆ Back to Top](#-lemondb)**

Made with ❤️ and 🍋

</div>

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