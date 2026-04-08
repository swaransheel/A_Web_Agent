@echo off
REM Quick Start Script for AI Web Search Agent Backend
REM Run this from the AI_web_agent (root) folder: run_backend.bat

REM Check if venv exists at root level
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate venv
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if packages installed
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
)

REM Verify setup
echo.
echo Verifying setup...
cd backend
python -c "from app.config import Config; Config.validate(); print('[OK] Configuration verified')" || exit /b 1
cd ..

REM Start server
echo.
echo Starting backend server on http://localhost:8000
echo.
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
