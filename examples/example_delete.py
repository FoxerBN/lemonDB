"""
Example: Delete Operations
Demonstrates how to delete records
"""

from app import LemonDB

print("=" * 60)
print("EXAMPLE: Delete Operations")
print("=" * 60)

# Create database
schema = {
    "id": "integer",
    "task": "string",
    "priority": "string",
    "done": "boolean"
}

db = LemonDB(name="todos", schema=schema)

# Add tasks
db.save(
    (1, "Buy groceries", "high", False),
    (2, "Write report", "high", False),
    (3, "Call dentist", "medium", False),
    (4, "Clean room", "low", False),
    (5, "Read book", "low", False)
)

print("\n--- Initial tasks ---")
print(f"Total tasks: {db.count()}")
for task in db.findAll():
    print(f"  [{task['id']}] {task['task']} - {task['priority']}")

print("\n--- Example 1: Delete one task by ID ---")
db.deleteOne({"id": 3})

print("\n--- Example 2: Delete one task by name ---")
db.deleteOne({"task": "Read book"})

print("\n--- Remaining tasks ---")
print(f"Total tasks: {db.count()}")
for task in db.findAll():
    print(f"  [{task['id']}] {task['task']} - {task['priority']}")

print("\n--- Example 3: Delete all records ---")
response = input("\nDelete all remaining tasks? (yes/no): ")
if response.lower() == "yes":
    db.deleteAll()
    print(f"\nFinal count: {db.count()}")

print("\n✅ Delete examples completed!")
