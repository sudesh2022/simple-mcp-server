#!/usr/bin/env python3
"""
Test script for the MCP HTTP server
Run this to verify all endpoints are working correctly
"""

import requests
import sys
import json

def test_server(base_url="http://localhost:8000"):
    """Test all server endpoints"""
    
    print(f"Testing MCP Server at: {base_url}\n")
    print("=" * 60)
    
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: Server Info
    print("\n1. Testing GET / (Server Info)")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Status: {response.status_code}")
            print(f"   Server: {data.get('name')} v{data.get('version')}")
            tests_passed += 1
        else:
            print(f"   ❌ Status: {response.status_code}")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ Error: {e}")
        tests_failed += 1
    
    # Test 2: Health Check
    print("\n2. Testing GET /health")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Status: {response.status_code}")
            print(f"   Health: {data.get('status')}")
            tests_passed += 1
        else:
            print(f"   ❌ Status: {response.status_code}")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ Error: {e}")
        tests_failed += 1
    
    # Test 3: List Tools
    print("\n3. Testing GET /tools")
    try:
        response = requests.get(f"{base_url}/tools")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Status: {response.status_code}")
            print(f"   Available tools: {len(data.get('tools', []))}")
            tests_passed += 1
        else:
            print(f"   ❌ Status: {response.status_code}")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ Error: {e}")
        tests_failed += 1
    
    # Test 4: Echo Tool
    print("\n4. Testing POST /tools/echo")
    try:
        payload = {"text": "Hello, MCP!"}
        response = requests.post(
            f"{base_url}/tools/echo",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Status: {response.status_code}")
            print(f"   Result: {data.get('result')}")
            tests_passed += 1
        else:
            print(f"   ❌ Status: {response.status_code}")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ Error: {e}")
        tests_failed += 1
    
    # Test 5: Current Time Tool
    print("\n5. Testing GET /tools/time")
    try:
        response = requests.get(f"{base_url}/tools/time")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Status: {response.status_code}")
            print(f"   Time: {data.get('result')}")
            tests_passed += 1
        else:
            print(f"   ❌ Status: {response.status_code}")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ Error: {e}")
        tests_failed += 1
    
    # Test 6: Calculate Tool - Addition
    print("\n6. Testing POST /tools/calculate (addition)")
    try:
        payload = {"operation": "add", "a": 10, "b": 5}
        response = requests.post(
            f"{base_url}/tools/calculate",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Status: {response.status_code}")
            print(f"   Result: {data.get('a')} + {data.get('b')} = {data.get('result')}")
            tests_passed += 1
        else:
            print(f"   ❌ Status: {response.status_code}")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ Error: {e}")
        tests_failed += 1
    
    # Test 7: Calculate Tool - Multiplication
    print("\n7. Testing POST /tools/calculate (multiplication)")
    try:
        payload = {"operation": "multiply", "a": 7, "b": 6}
        response = requests.post(
            f"{base_url}/tools/calculate",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Status: {response.status_code}")
            print(f"   Result: {data.get('a')} × {data.get('b')} = {data.get('result')}")
            tests_passed += 1
        else:
            print(f"   ❌ Status: {response.status_code}")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ Error: {e}")
        tests_failed += 1
    
    # Test 8: Reverse Text Tool
    print("\n8. Testing POST /tools/reverse")
    try:
        payload = {"text": "MCP Server"}
        response = requests.post(
            f"{base_url}/tools/reverse",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Status: {response.status_code}")
            print(f"   Original: {data.get('original')}")
            print(f"   Reversed: {data.get('result')}")
            tests_passed += 1
        else:
            print(f"   ❌ Status: {response.status_code}")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ Error: {e}")
        tests_failed += 1
    
    # Test 9: Error Handling - Division by Zero
    print("\n9. Testing Error Handling (division by zero)")
    try:
        payload = {"operation": "divide", "a": 10, "b": 0}
        response = requests.post(
            f"{base_url}/tools/calculate",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 400:
            print(f"   ✅ Status: {response.status_code} (Expected error)")
            print(f"   Error: {response.json().get('error')}")
            tests_passed += 1
        else:
            print(f"   ❌ Status: {response.status_code} (Expected 400)")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ Error: {e}")
        tests_failed += 1
    
    # Summary
    print("\n" + "=" * 60)
    print(f"\nTest Summary:")
    print(f"  ✅ Passed: {tests_passed}")
    print(f"  ❌ Failed: {tests_failed}")
    print(f"  Total:  {tests_passed + tests_failed}")
    
    if tests_failed == 0:
        print("\n🎉 All tests passed! Server is working correctly.")
        return 0
    else:
        print(f"\n⚠️  {tests_failed} test(s) failed. Please check the server.")
        return 1


if __name__ == "__main__":
    # Get base URL from command line argument or use default
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    
    print("MCP Server Test Suite")
    print(f"Target: {base_url}\n")
    
    try:
        exit_code = test_server(base_url)
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        sys.exit(1)
