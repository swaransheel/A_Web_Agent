#!/usr/bin/env python3
"""
Backend Health Check and Test Script
Verifies that everything is configured correctly before running
"""

import os
import sys
import subprocess
from pathlib import Path

def check_config():
    """Check if configuration is valid."""
    print("🔍 Checking Configuration...")
    
    # Check .env file
    env_file = Path("backend/.env")
    if not env_file.exists():
        print("❌ .env file not found")
        return False
    
    # Read .env
    env_vars = {}
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                env_vars[key.strip()] = value.strip().strip('"').strip("'")
    
    # Check required keys
    required = ["GEMINI_API_KEY", "TAVILY_API_KEY"]
    missing = []
    
    for key in required:
        if key not in env_vars or not env_vars[key] or env_vars[key] == "your_key_here":
            missing.append(key)
            print(f"  ❌ {key}: NOT SET")
        else:
            # Show truncated key
            value = env_vars[key]
            truncated = value[:10] + "..." if len(value) > 10 else value
            print(f"  ✅ {key}: {truncated}")
    
    if missing:
        print(f"\n❌ Missing or invalid: {', '.join(missing)}")
        print("   Please add your API keys to backend/.env")
        return False
    
    print("✅ Configuration valid!\n")
    return True

def check_dependencies():
    """Check if required Python packages are installed."""
    print("📦 Checking Dependencies...")
    
    required = [
        "fastapi",
        "uvicorn",
        "pydantic",
        "httpx",
        "google.generativeai"
    ]
    
    try:
        import importlib
        missing = []
        
        for package in required:
            try:
                module_name = package.replace("-", "_").split(".")[0]
                importlib.import_module(module_name)
                print(f"  ✅ {package}")
            except ImportError:
                missing.append(package)
                print(f"  ❌ {package}")
        
        if missing:
            print(f"\n⚠️  Missing packages: {', '.join(missing)}")
            print("   Run: pip install -r requirements.txt")
            return False
        
        print("✅ All dependencies installed!\n")
        return True
    except Exception as e:
        print(f"❌ Error checking dependencies: {e}")
        return False

def check_frontend():
    """Check if frontend files exist."""
    print("🎨 Checking Frontend Files...")
    
    files = [
        "search_home/code.html",
        "search_results/code.html"
    ]
    
    all_exist = True
    for file in files:
        if Path(file).exists():
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file}")
            all_exist = False
    
    if not all_exist:
        print("\n❌ Some frontend files are missing")
        return False
    
    print("✅ Frontend files ready!\n")
    return True

def main():
    """Run all checks."""
    print("=" * 50)
    print("🚀 AI Web Search Agent - Setup Verification")
    print("=" * 50 + "\n")
    
    checks = [
        ("Configuration", check_config),
        ("Dependencies", check_dependencies),
        ("Frontend", check_frontend),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Error during {name} check: {e}\n")
            results.append((name, False))
    
    # Summary
    print("=" * 50)
    print("📋 Summary")
    print("=" * 50)
    
    all_passed = True
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name}: {status}")
        if not result:
            all_passed = False
    
    print("=" * 50)
    
    if all_passed:
        print("\n✨ All checks passed! Ready to run:\n")
        print("  1. Start backend:    python run_server.py")
        print("  2. Open frontend:    search_home/code.html in browser")
        print("  3. API docs:         http://localhost:8000/docs")
        print("\n🎉 Everything is configured and ready!")
    else:
        print("\n⚠️  Please fix the issues above before running")
        sys.exit(1)

if __name__ == "__main__":
    main()
