"""
Example: Find and Query Operations
Demonstrates how to search for records
"""

from app import LemonDB

print("=" * 60)
print("EXAMPLE: Find Operations")
print("=" * 60)

# Create database with sample data
schema = {
    "id": "integer",
    "name": "string",
    "department": "string",
    "salary": "float",
    "active": "boolean"
}

db = LemonDB(name="employees", schema=schema)

# Add sample employees
db.save(
    (1, "Alice", "Engineering", 75000.0, True),
    (2, "Bob", "Marketing", 65000.0, True),
    (3, "Charlie", "Engineering", 80000.0, True),
    (4, "Diana", "Sales", 70000.0, False),
    (5, "Eve", "Engineering", 72000.0, True)
)

print("\n--- Example 1: Find all records ---")
all_employees = db.findAll()
print(f"Total employees: {len(all_employees)}")

print("\n--- Example 2: Find by department ---")
engineers = db.find({"department": "Engineering"})
print(f"\nEngineers ({len(engineers)}):")
for emp in engineers:
    print(f"  - {emp['name']}: ${emp['salary']:,.2f}")

print("\n--- Example 3: Find by active status ---")
active_employees = db.find({"active": True})
print(f"\nActive employees: {len(active_employees)}")

print("\n--- Example 4: Find specific person ---")
alice = db.find({"name": "Alice"})
if alice:
    print(f"\nFound Alice: {alice[0]}")

print("\n--- Example 5: Find with multiple conditions ---")
active_engineers = db.find({"department": "Engineering", "active": True})
print(f"\nActive engineers: {len(active_engineers)}")
for emp in active_engineers:
    print(f"  - {emp['name']}")

print("\n✅ Find examples completed!")
