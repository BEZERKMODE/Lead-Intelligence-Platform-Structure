@echo off
cd /d "%~dp0"
title Lead Intel Platform
echo =====================================================================
echo 🚀 STARTING LEAD INTELLIGENCE PLATFORM (FastAPI Server)
echo =====================================================================
echo.
echo [*] Database: SQLite Auto-Fallback Enabled
echo [*] URL:      http://localhost:5003
echo.
echo [1/2] Scheduling browser launch in 2 seconds...
start /b cmd /c "timeout /t 2 /nobreak >nul 2>&1 && start http://localhost:5003"
echo [2/2] Running Diagnostics...
set PYTHONPATH=%cd%
python test_imports.py > error_log.txt 2>&1
echo.
echo Starting server (logs will appear below)...
echo.
set PYTHONPATH=%cd%
python -m uvicorn backend.app:app --host 0.0.0.0 --port 5003 --reload
echo.
echo =====================================================================
echo [!] Server stopped.
echo =====================================================================
pause
