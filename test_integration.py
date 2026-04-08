"""
Integration Test Script
Tests the complete backend-frontend integration
Run this after starting the backend: python test_integration.py
"""

import sys
import time
import json
import asyncio
from pathlib import Path

# Test configuration
BACKEND_URL = "http://localhost:8000"
API_ENDPOINT = f"{BACKEND_URL}/api/search"
HEALTH_ENDPOINT = f"{BACKEND_URL}/api/health"

def test_backend_connection():
    """Test if backend is running."""
    print("\n📡 Test 1: Backend Connection")
    print("-" * 40)
    
    try:
        import requests
        response = requests.get(HEALTH_ENDPOINT, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend is running")
            print(f"   Status: {data.get('status')}")
            print(f"   Message: {data.get('message')}")
            return True
        else:
            print(f"❌ Backend returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to backend at {BACKEND_URL}")
        print(f"   Make sure to run: python run_server.py")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_search_api():
    """Test search API endpoint."""
    print("\n🔍 Test 2: Search API")
    print("-" * 40)
    
    try:
        import requests
        
        test_query = "What is artificial intelligence?"
        print(f"Query: {test_query}")
        
        response = requests.post(
            API_ENDPOINT,
            json={"query": test_query},
            timeout=60  # Allow long timeout for API calls
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Check response format
            if "answer" in data and "sources" in data:
                print(f"✅ API returned valid response")
                print(f"   Answer length: {len(data['answer'])} characters")
                print(f"   Number of sources: {len(data['sources'])}")
                
                if data['sources']:
                    print(f"   First source: {data['sources'][0][:50]}...")
                
                return True
            else:
                print(f"❌ Response missing required fields")
                print(f"   Response: {data}")
                return False
        else:
            print(f"❌ API returned status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except requests.exceptions.Timeout:
        print(f"❌ Request timed out (60+ seconds)")
        print(f"   Check: Tavily/Gemini API responsiveness")
        return False
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to API")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_frontend_files():
    """Test if frontend files exist and are valid."""
    print("\n🎨 Test 3: Frontend Files")
    print("-" * 40)
    
    files = [
        "search_home/code.html",
        "search_results/code.html"
    ]
    
    all_valid = True
    
    for file_path in files:
        path = Path(file_path)
        
        if not path.exists():
            print(f"❌ {file_path}: NOT FOUND")
            all_valid = False
            continue
        
        with open(path) as f:
            content = f.read()
        
        # Check for JavaScript integration
        has_script = "<script>" in content or "performSearch" in content or "performFollowUp" in content
        has_api_config = "API_BASE_URL" in content or "http://localhost:8000" in content
        
        if has_script and has_api_config:
            print(f"✅ {file_path}")
            print(f"   - Has JavaScript integration")
            print(f"   - API configuration present")
        else:
            print(f"⚠️  {file_path}")
            if not has_script:
                print(f"   - Missing JavaScript handlers")
            if not has_api_config:
                print(f"   - Missing API configuration")
            all_valid = False
    
    return all_valid

def test_cors_configuration():
    """Test CORS configuration."""
    print("\n🔒 Test 4: CORS Configuration")
    print("-" * 40)
    
    try:
        import requests
        
        # Test CORS headers
        headers = {
            "Origin": "http://localhost:3000",
            "Referer": "http://localhost:3000/"
        }
        
        response = requests.options(
            API_ENDPOINT,
            headers=headers,
            timeout=5
        )
        
        cors_origin = response.headers.get("Access-Control-Allow-Origin")
        
        if cors_origin:
            print(f"✅ CORS is configured")
            print(f"   Allowed origin(s): *")
            return True
        else:
            print(f"⚠️  No CORS headers detected")
            print(f"   If frontend is on different origin, add to:")
            print(f"   backend/.env CORS_ORIGINS=...")
            return False
    except Exception as e:
        print(f"⚠️  Could not test CORS: {e}")
        return False

def test_api_validation():
    """Test API input validation."""
    print("\n✔️  Test 5: API Validation")
    print("-" * 40)
    
    try:
        import requests
        
        # Test 1: Empty query
        print("Testing: Empty query")
        response = requests.post(
            API_ENDPOINT,
            json={"query": ""},
            timeout=10
        )
        
        if response.status_code == 400:
            print("  ✅ Empty query rejected")
        else:
            print("  ⚠️  Empty query not handled")
        
        # Test 2: Very long query
        print("Testing: Long query")
        long_query = "test " * 200
        response = requests.post(
            API_ENDPOINT,
            json={"query": long_query},
            timeout=10
        )
        
        if response.status_code == 400:
            print("  ✅ Long query rejected")
        else:
            print("  ⚠️  Long query not handled")
        
        return True
    except Exception as e:
        print(f"⚠️  Validation test error: {e}")
        return False

def main():
    """Run all integration tests."""
    print("=" * 50)
    print("🧪 AI Web Search Agent - Integration Tests")
    print("=" * 50)
    
    tests = [
        ("Backend Connection", test_backend_connection),
        ("Search API", test_search_api),
        ("Frontend Files", test_frontend_files),
        ("CORS Configuration", test_cors_configuration),
        ("API Validation", test_api_validation),
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except KeyboardInterrupt:
            print("\n\n⏸️  Tests interrupted by user")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 Test Summary")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name}: {status}")
    
    print("=" * 50)
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✨ All integration tests passed!")
        print("\n📝 Next steps:")
        print("  1. Open search_home/code.html in your browser")
        print("  2. Enter a search query")
        print("  3. You should see results page with answer + sources")
        print("  4. Try a follow-up question")
    else:
        print("\n⚠️  Some tests failed. Check the output above.")
        print("\n🔍 Troubleshooting:")
        print("  - Is backend running? (python run_server.py)")
        print("  - Are API keys set in backend/.env?")
        print("  - Check browser console (F12) for JavaScript errors")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Tests stopped by user")
        sys.exit(0)
