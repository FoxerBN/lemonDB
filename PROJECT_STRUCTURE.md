# 🍋 LemonDB - Project Structure

## Directory Layout

```
lemonDB/
├── README.md                    # Project overview & quick start
├── docs.md                      # Complete documentation
├── LICENSE                      # MIT License
├── setup.py                     # Package configuration
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore rules
├── run_all_tests.py            # Run all tests at once
│
├── app/                         # Core package
│   ├── __init__.py             # Package initialization
│   ├── core.py                 # Main LemonDB class (113 lines)
│   ├── schema.py               # Schema validation (73 lines)
│   ├── engine.py               # CSV storage engine (110 lines)
│   └── utils.py                # Utility functions (61 lines)
│
├── tests/                       # Unit tests
│   ├── __init__.py
│   ├── test_creation.py        # Test: Database creation
│   ├── test_count.py           # Test: Count function
│   └── test_db_test.py         # Test: db.test() method
│
└── examples/                    # Usage examples
    ├── example_save.py         # Demo: Save operations
    ├── example_find.py         # Demo: Query/find operations
    ├── example_update.py       # Demo: Update operations
    ├── example_delete.py       # Demo: Delete operations
    └── todo_app.py             # Demo: Complete todo app
```

## Module Descriptions

### `app/core.py`
Main API interface - LemonDB class with CRUD operations
- `save()` - Save records with validation
- `find()` / `findAll()` - Query operations
- `deleteOne()` / `deleteAll()` - Delete operations
- `updateOne()` - Update records
- `count()` - Count records
- `test()` - Database status check

### `app/schema.py`
Schema validation and constraint enforcement
- Type validation (string, integer, float, boolean, date)
- Constraint checking (required, unique)
- Record format validation

### `app/engine.py`
CSV-based storage engine
- File I/O operations
- Query matching
- Type conversion (Python ↔ CSV)

### `app/utils.py`
Helper utilities
- Path management
- Data serialization
- Metadata handling

## Running Commands

### Run All Tests
```bash
python3 run_all_tests.py
```

### Run Individual Tests
```bash
python3 -m tests.test_creation
python3 -m tests.test_count
python3 -m tests.test_db_test
```

### Run Examples
```bash
python3 -m examples.example_save
python3 -m examples.example_find
python3 -m examples.example_update
python3 -m examples.example_delete
python3 -m examples.todo_app
```

## Data Storage

Default location: `./lemondb_data/`

```
lemondb_data/
├── users.csv                  # Data records
├── users_metadata.json        # Schema definition
├── products.csv
└── products_metadata.json
```

## Code Statistics

- **Total lines:** 357
- **Core:** 113 lines
- **Engine:** 110 lines
- **Schema:** 73 lines
- **Utils:** 61 lines

## Testing Coverage

✅ Database creation
✅ Count function
✅ Test method (db.test())
✅ Save operations
✅ Find operations
✅ Update operations
✅ Delete operations

---

**Made with 🍋 by lemonDB**
