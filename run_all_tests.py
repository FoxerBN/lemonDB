#!/usr/bin/env python3
"""
Run all tests for LemonDB
"""

import sys
from tests import test_creation, test_count, test_db_test, test_auto_id

def run_all_tests():
    """Run all test modules"""
    print("\n" + "=" * 60)
    print("🍋 RUNNING ALL LEMONDB TESTS")
    print("=" * 60)
    
    tests = [
        ("Database Creation", test_creation.test_db_creation),
        ("Count Function", test_count.test_count),
        ("DB Test Method", test_db_test.test_db_test),
        ("Auto-Increment ID", test_auto_id.test_auto_id),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            print(f"\n\n{'*' * 60}")
            print(f"Running: {name}")
            print('*' * 60)
            test_func()
            passed += 1
        except Exception as e:
            print(f"\n❌ TEST FAILED: {name}")
            print(f"Error: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"Total: {passed + failed}")
    print("=" * 60)
    
    return failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
