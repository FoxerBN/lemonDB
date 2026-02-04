"""
Test: Database Test Function
Tests db.test() method
"""

from app import LemonDB

def test_db_test():
    """Test the test() method"""
    schema = {
        "username": "string",
        "email": "string",
        "age": "integer"
    }
    
    print("=" * 50)
    print("TEST: db.test() Function")
    print("=" * 50)
    
    db = LemonDB(name="test_db", schema=schema)
    
    # Test empty database
    print("\n--- Testing empty database ---")
    result = db.test()
    assert result == True, "test() should return True"
    
    # Add some data
    db.save(
        ("alice", "alice@test.com", 25),
        ("bob", "bob@test.com", 30)
    )
    
    # Test with data
    print("\n--- Testing database with data ---")
    result = db.test()
    assert result == True, "test() should return True"
    
    print("\n✅ db.test() works correctly!")
    return True


if __name__ == "__main__":
    test_db_test()
