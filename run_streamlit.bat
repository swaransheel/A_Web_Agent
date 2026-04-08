@echo off
REM Run AI Web Agent with Streamlit Frontend
echo.
echo ============================================================
echo AI Web Agent - Streamlit Version
echo ============================================================
echo.

cd /d "%~dp0"

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run both servers
python run_all_streamlit.py

pause
