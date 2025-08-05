@echo off
title Smart Traffic Control System Launcher
color 0A

echo.
echo ========================================
echo    SMART TRAFFIC CONTROL SYSTEM
echo ========================================
echo.

cd /d "%~dp0"

echo Activating Python environment...
call myenv\Scripts\activate.bat

echo.
echo Starting Traffic Control System...
echo.

python launcher.py

pause
