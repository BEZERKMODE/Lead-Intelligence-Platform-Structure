@echo off
cd /d "%~dp0"
title Lead Intel Platform
echo =====================================================================
echo 🚀 STARTING LEAD INTELLIGENCE PLATFORM (FastAPI Server)
echo =====================================================================
echo.
echo [*] Database: SQLite Auto-Fallback Enabled
echo [*] URL:      http://localhost:5002
echo.
echo [1/2] Scheduling browser launch in 2 seconds...
start /b cmd /c "timeout /t 2 /nobreak >nul 2>&1 && start http://localhost:5002"
echo [2/2] Starting server (logs will appear below)...
echo.
python backend\app.py
echo.
echo =====================================================================
echo [!] Server stopped.
echo =====================================================================
pause
