#!/usr/bin/env python3
"""
Test script to verify AI Comic Factory setup
"""

import os
import sys
import requests
import json
from pathlib import Path

def test_backend_connection():
    """Test if the backend is running and responding"""
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running and responding")
            return True
        else:
            print(f"❌ Backend responded with status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend is not running. Please start it first.")
        return False
    except Exception as e:
        print(f"❌ Error connecting to backend: {e}")
        return False

def test_environment_variables():
    """Test if required environment variables are set"""
    required_vars = ["OPENAI_API_KEY", "REPLICATE_API_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("   Please set them in backend/.env")
        return False
    else:
        print("✅ All required environment variables are set")
        return True

def test_api_endpoints():
    """Test the API endpoints"""
    try:
        # Test generate-prompts endpoint
        test_data = {
            "genre": "Sci-Fi",
            "setting": "Space Station",
            "characters": "Robot detective"
        }
        
        response = requests.post(
            "http://localhost:8000/generate-prompts",
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success") and data.get("prompts"):
                print(f"✅ Generate prompts endpoint working (got {len(data['prompts'])} prompts)")
                return True
            else:
                print("❌ Generate prompts endpoint returned unexpected response")
                return False
        else:
            print(f"❌ Generate prompts endpoint failed with status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing API endpoints: {e}")
        return False

def test_frontend_files():
    """Test if frontend files exist"""
    frontend_files = [
        "frontend/package.json",
        "frontend/app/page.tsx",
        "frontend/app/layout.tsx"
    ]
    
    missing_files = []
    for file_path in frontend_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing frontend files: {', '.join(missing_files)}")
        return False
    else:
        print("✅ All frontend files exist")
        return True

def main():
    """Run all tests"""
    print("🧪 Testing AI Comic Factory Setup")
    print("=" * 40)
    
    tests = [
        ("Environment Variables", test_environment_variables),
        ("Frontend Files", test_frontend_files),
        ("Backend Connection", test_backend_connection),
        ("API Endpoints", test_api_endpoints),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing: {test_name}")
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
    
    print("\n" + "=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your setup is ready to use.")
        print("\nNext steps:")
        print("1. Open http://localhost:3000 in your browser")
        print("2. Fill in the form and start creating comics!")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("\nTroubleshooting:")
        print("1. Make sure the backend is running: python backend/main.py")
        print("2. Check your API keys in backend/.env")
        print("3. Ensure all dependencies are installed")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 