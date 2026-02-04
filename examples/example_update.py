"""
Example: Update Operations
Demonstrates how to update records
"""

from app import LemonDB

print("=" * 60)
print("EXAMPLE: Update Operations")
print("=" * 60)

# Create database
schema = {
    "id": "integer",
    "product": "string",
    "price": "float",
    "stock": "integer"
}

db = LemonDB(name="inventory", schema=schema)

# Add initial products
db.save(
    (1, "Laptop", 999.99, 10),
    (2, "Mouse", 25.50, 50),
    (3, "Keyboard", 75.00, 30)
)

print("\n--- Initial inventory ---")
for item in db.findAll():
    print(f"  {item['product']}: ${item['price']} (stock: {item['stock']})")

print("\n--- Example 1: Update price ---")
db.updateOne({"id": 1}, {"price": 899.99})
print("Updated Laptop price to $899.99")

print("\n--- Example 2: Update stock ---")
db.updateOne({"product": "Mouse"}, {"stock": 45})
print("Updated Mouse stock to 45")

print("\n--- Example 3: Update multiple fields ---")
db.updateOne({"id": 3}, {"price": 79.99, "stock": 25})
print("Updated Keyboard price and stock")

print("\n--- Final inventory ---")
for item in db.findAll():
    print(f"  {item['product']}: ${item['price']} (stock: {item['stock']})")

print("\n✅ Update examples completed!")
