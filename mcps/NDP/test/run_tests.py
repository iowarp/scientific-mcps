#!/usr/bin/env python3
"""
Test runner for NDP MCP Server tests.

This script runs all tests from the test directory.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_test(test_file: str, description: str):
    """Run a specific test file."""
    print(f"\n{'='*60}")
    print(f"Running {description}")
    print(f"{'='*60}")
    
    try:
        # Run the test
        result = subprocess.run(
            [sys.executable, test_file],
            cwd=os.path.dirname(os.path.abspath(__file__)),
            capture_output=False,
            text=True
        )
        
        if result.returncode == 0:
            print(f"✅ {description} - PASSED")
            return True
        else:
            print(f"❌ {description} - FAILED (exit code: {result.returncode})")
            return False
            
    except Exception as e:
        print(f"❌ {description} - ERROR: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 NDP MCP Server Test Suite")
    print("=" * 60)
    
    # Get the test directory
    test_dir = Path(__file__).parent
    
    # Define tests to run
    tests = [
        ("test_server.py", "Server Functionality Tests"),
        ("test_stdio.py", "STDIO Communication Tests"),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_file, description in tests:
        test_path = test_dir / test_file
        if test_path.exists():
            if run_test(str(test_path), description):
                passed += 1
        else:
            print(f"❌ Test file not found: {test_file}")
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
