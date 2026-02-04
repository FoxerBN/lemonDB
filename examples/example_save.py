"""
Example: Save Operations
Demonstrates different ways to save records
"""

from app import LemonDB

print("=" * 60)
print("EXAMPLE: Save Operations")
print("=" * 60)

# Create database
schema = {
    "id": "integer",
    "name": "string",
    "email": "string",
    "active": "boolean"
}

db = LemonDB(name="users", schema=schema)

print("\n--- Example 1: Save single record ---")
db.save((1, "Alice", "alice@example.com", True))

print("\n--- Example 2: Save multiple records at once ---")
db.save(
    (2, "Bob", "bob@example.com", True),
    (3, "Charlie", "charlie@example.com", False),
    (4, "Diana", "diana@example.com", True)
)

print("\n--- Example 3: Save with error handling ---")
# This will skip invalid records
db.save(
    (5, "Eve", "eve@example.com", True),
    (6, None, "invalid@example.com", True),  # Invalid: missing name
    (7, "Frank", "frank@example.com", False),
    raise_on_error=False
)

print("\n--- View all saved records ---")
all_users = db.findAll()
print(f"\nTotal records: {len(all_users)}")
for user in all_users:
    print(f"  - {user['name']}: {user['email']} (active: {user['active']})")

print("\n✅ Save examples completed!")
