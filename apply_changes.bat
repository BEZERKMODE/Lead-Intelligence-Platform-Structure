@echo off
echo Applying changes...
python apply_user_changes.py
if %errorlevel% neq 0 (
    echo Error applying changes.
    pause
    exit /b %errorlevel%
)
echo Changes applied successfully!
echo Committing to git...
git add .
git commit -m "feat: applied user enterprise changes from chat parts 1-5"
echo Commit successful!
echo Starting project...
call run_server.bat
pause
