@echo off
title Cartoonify Image Project
cd /d "%~dp0"

echo ==========================================
echo       CARTOONIFY IMAGE PROJECT
echo ==========================================
echo.

where py >nul 2>nul
if %errorlevel%==0 (
    set PYTHON=py
) else (
    where python >nul 2>nul
    if %errorlevel% neq 0 (
        echo Python was not found. Install Python 3 from https://www.python.org/downloads/
        echo During installation, select "Add Python to PATH".
        pause
        exit /b 1
    )
    set PYTHON=python
)

if not exist ".venv\Scripts\python.exe" (
    echo Creating project environment...
    %PYTHON% -m venv .venv
    if errorlevel 1 (
        echo Could not create the environment.
        pause
        exit /b 1
    )
)

echo Installing/checking required packages...
".venv\Scripts\python.exe" -m pip install --upgrade pip
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
    echo Package installation failed. Check your internet connection and try again.
    pause
    exit /b 1
)

echo.
echo Starting Cartoonify...
".venv\Scripts\python.exe" app.py
if errorlevel 1 (
    echo The application stopped because of an error.
    pause
)
