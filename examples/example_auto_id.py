"""
Example: Using Auto-Increment ID
Demonstrates automatic ID generation and findById
"""

from app import LemonDB

print("=" * 60)
print("EXAMPLE: Auto-Increment ID Feature")
print("=" * 60)

# Create database with auto_id enabled (default)
schema = {
    "title": "string",
    "author": "string",
    "year": "integer"
}

books_db = LemonDB(name="books", schema=schema)

print("\n--- Example 1: Save books (IDs added automatically) ---")
# Notice: We DON'T specify IDs - they're added automatically!
books_db.save(
    ("1984", "George Orwell", 1949),
    ("To Kill a Mockingbird", "Harper Lee", 1960),
    ("The Great Gatsby", "F. Scott Fitzgerald", 1925),
    ("Pride and Prejudice", "Jane Austen", 1813)
)

print("\n--- View all books with auto-generated IDs ---")
all_books = books_db.findAll()
for book in all_books:
    print(f"  ID {book['id']}: {book['title']} by {book['author']} ({book['year']})")

print("\n--- Example 2: Find by ID (quick lookup) ---")
book = books_db.findById(2)
if book:
    print(f"\nBook with ID 2: {book['title']} by {book['author']}")

print("\n--- Example 3: Add more books (ID continues) ---")
books_db.save(
    ("The Catcher in the Rye", "J.D. Salinger", 1951),
    ("Harry Potter", "J.K. Rowling", 1997)
)

print(f"\nTotal books now: {books_db.count()}")
latest = books_db.findById(6)
print(f"Latest book (ID 6): {latest['title']}")

print("\n--- Example 4: Update book by ID ---")
books_db.updateOne({"id": 1}, {"year": 1950})  # Fictional update
print("Updated book ID 1")

updated_book = books_db.findById(1)
print(f"Book ID 1 after update: {updated_book}")

print("\n--- Example 5: Delete book by ID ---")
books_db.deleteOne({"id": 3})
print("Deleted book with ID 3")

print("\n--- Final library ---")
print(f"Total books: {books_db.count()}")
for book in books_db.findAll():
    print(f"  [{book['id']}] {book['title']}")

print("\n✅ Auto-ID example completed!")
print("\n💡 Key Points:")
print("  • IDs are added automatically (start from 1)")
print("  • You don't specify IDs when saving")
print("  • Use findById(id) for quick lookups")
print("  • IDs are never reused after deletion")
