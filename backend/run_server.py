#!/usr/bin/env python3
"""
Startup script for the AI Web Search Agent backend.
Usage: python run_server.py
"""

import sys
import os
import subprocess

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Verify .env file exists
if not os.path.exists('.env'):
    print("❌ Error: .env file not found!")
    print("Please copy .env.example to .env and fill in your API keys.")
    sys.exit(1)

# Verify API keys are configured
from app.config import Config

try:
    Config.validate()
    print("✅ Configuration validated")
except ValueError as e:
    print(f"❌ Configuration error: {e}")
    sys.exit(1)

# Start the server
print("\n🚀 Starting AI Web Search Agent Backend...")
print("📍 Server will be available at: http://localhost:8000")
print("📖 API Documentation: http://localhost:8000/docs")
print("⏸️  Press Ctrl+C to stop the server\n")

try:
    subprocess.run([
        sys.executable, "-m", "uvicorn",
        "app.main:app",
        "--reload",
        "--host", "0.0.0.0",
        "--port", "8000"
    ])
except KeyboardInterrupt:
    print("\n\n👋 Shutting down...")
    sys.exit(0)
