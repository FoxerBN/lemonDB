"""
Test: Database Creation and Initialization
Tests if database is created properly with schema
"""

from app import LemonDB

def test_db_creation():
    """Test if database can be created"""
    schema = {
        "username": "string",
        "email": "string"
    }
    
    print("=" * 50)
    print("TEST: Database Creation")
    print("=" * 50)
    
    # Create database
    db = LemonDB(name="test_users", schema=schema)
    
    # Test if it works
    db.test()
    
    print("\n✅ Database created successfully!")
    return True


if __name__ == "__main__":
    test_db_creation()
