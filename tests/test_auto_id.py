"""
Test: Auto-Increment ID Feature
Tests automatic ID generation
"""

from app import LemonDB

def test_auto_id():
    """Test automatic ID generation"""
    schema = {
        "name": "string",
        "email": "string"
    }
    
    print("=" * 50)
    print("TEST: Auto-Increment ID")
    print("=" * 50)
    
    # Create database with auto_id enabled (default)
    db = LemonDB(name="test_auto_id", schema=schema)
    
    print("\n--- Test 1: Save records WITHOUT specifying ID ---")
    # Records don't include ID - it's added automatically
    db.save(
        ("Alice", "alice@test.com"),
        ("Bob", "bob@test.com"),
        ("Charlie", "charlie@test.com")
    )
    
    # Check if IDs were added
    all_records = db.findAll()
    print("\nRecords with auto-generated IDs:")
    for record in all_records:
        print(f"  ID: {record['id']}, Name: {record['name']}, Email: {record['email']}")
    
    # Verify IDs
    assert all_records[0]['id'] == 1, "First ID should be 1"
    assert all_records[1]['id'] == 2, "Second ID should be 2"
    assert all_records[2]['id'] == 3, "Third ID should be 3"
    print("✅ IDs generated correctly: 1, 2, 3")
    
    print("\n--- Test 2: Find by ID ---")
    # Find using the new findById method
    alice = db.findById(1)
    print(f"\nFound by ID 1: {alice}")
    assert alice['name'] == "Alice", "Should find Alice by ID 1"
    
    bob = db.findById(2)
    assert bob['name'] == "Bob", "Should find Bob by ID 2"
    print("✅ findById() works correctly")
    
    print("\n--- Test 3: Add more records (ID continues) ---")
    db.save(("Diana", "diana@test.com"))
    
    diana = db.findById(4)
    print(f"\nNew record: {diana}")
    assert diana['id'] == 4, "Next ID should be 4"
    assert diana['name'] == "Diana", "Should be Diana"
    print("✅ ID continues from 4")
    
    print("\n--- Test 4: Delete and add (ID doesn't reuse) ---")
    db.deleteOne({"id": 2})
    print("Deleted record with ID 2")
    
    db.save(("Eve", "eve@test.com"))
    eve = db.findById(5)
    print(f"New record after delete: {eve}")
    assert eve['id'] == 5, "New ID should be 5, not reusing 2"
    print("✅ IDs don't get reused")
    
    print("\n--- Test 5: Verify final state ---")
    final = db.findAll()
    print(f"\nFinal records: {db.count()}")
    for record in final:
        print(f"  ID: {record['id']}, Name: {record['name']}")
    
    print("\n✅ All auto-ID tests passed!")
    return True


if __name__ == "__main__":
    test_auto_id()
