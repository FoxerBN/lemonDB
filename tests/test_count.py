"""
Test: Database Count Function
Tests db.count() method
"""

from app import LemonDB

def test_count():
    """Test count functionality"""
    schema = {
        "name": "string"
    }
    
    print("=" * 50)
    print("TEST: Count Function")
    print("=" * 50)
    
    # auto_id is enabled by default, so only pass name
    db = LemonDB(name="test_count", schema=schema)
    
    # Initial count
    initial = db.count()
    print(f"\nInitial count: {initial}")
    assert initial == 0, "Expected 0 records initially"
    
    # Add records (only name, ID is added automatically)
    db.save(("Alice",), ("Bob",), ("Charlie",))
    
    # Count after adding
    after = db.count()
    print(f"Count after adding 3 records: {after}")
    assert after == 3, "Expected 3 records"
    
    # Delete one by ID
    db.deleteOne({"id": 2})
    
    # Count after delete
    final = db.count()
    print(f"Count after deleting 1 record: {final}")
    assert final == 2, "Expected 2 records"
    
    print("\n✅ All count tests passed!")
    return True


if __name__ == "__main__":
    test_count()
