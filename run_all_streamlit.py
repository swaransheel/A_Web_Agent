#!/usr/bin/env python
"""
Run both backend and Streamlit frontend
"""
import subprocess
import os
import sys
import time

def main():
    # Start backend
    print("=" * 60)
    print("Starting Backend Server...")
    print("=" * 60)
    
    backend_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
        cwd="backend",
        env={**os.environ, "PYTHONUNBUFFERED": "1"}
    )
    
    # Wait for backend to start
    time.sleep(2)
    
    # Start Streamlit frontend
    print("\n" + "=" * 60)
    print("Starting Streamlit Frontend...")
    print("=" * 60)
    print("Streamlit will open at: http://localhost:8501")
    print("\n")
    
    streamlit_process = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "streamlit_app.py", "--logger.level=info"],
        env={**os.environ, "API_URL": "http://localhost:8000"}
    )
    
    # Keep both processes running
    try:
        backend_process.wait()
        streamlit_process.wait()
    except KeyboardInterrupt:
        print("\nShutting down...")
        backend_process.terminate()
        streamlit_process.terminate()
        backend_process.wait()
        streamlit_process.wait()
        print("Shutdown complete")

if __name__ == "__main__":
    main()
