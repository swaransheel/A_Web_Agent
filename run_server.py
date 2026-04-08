#!/usr/bin/env python3
"""
Run the FastAPI backend server from the project root.
Works with the reorganized structure where backend/ and venv/ are at root level.
"""
import subprocess
import sys
import os

def main():
    # Set the backend directory
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    
    # Change to backend directory
    os.chdir(backend_dir)
    
    # Run uvicorn server
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'uvicorn', 'app.main:app', '--reload', '--host', '0.0.0.0', '--port', '8000'],
            cwd=backend_dir
        )
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        print("\nServer stopped.")
        sys.exit(0)
    except Exception as e:
        print(f"Error running server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
