#!/usr/bin/env python
"""
Run both backend and Streamlit frontend
"""
import subprocess
import sys
import time
import os

print("=" * 60)
print("Starting Backend Server...")
print("=" * 60)

# Start backend
backend_process = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "app.main:app", "--reload", "--port", "8000"],
    cwd="backend"
)

# Wait for backend to start
time.sleep(3)

print("\n" + "=" * 60)
print("Starting Streamlit Frontend...")
print("=" * 60)
print("Open: http://localhost:8501\n")

# Start Streamlit
streamlit_process = subprocess.Popen(
    [sys.executable, "-m", "streamlit", "run", "streamlit_app.py"]
)

try:
    backend_process.wait()
    streamlit_process.wait()
except KeyboardInterrupt:
    print("\nShutting down...")
    backend_process.terminate()
    streamlit_process.terminate()

