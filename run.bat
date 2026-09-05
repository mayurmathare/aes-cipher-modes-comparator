@echo off
title AES Block Cipher Modes Comparison - Web Simulator
cd /d "%~dp0"

echo ======================================================================
echo       AES Block Cipher Modes Comparison (Cryptography Practical)
echo ======================================================================
echo.

:: Detect Python command
set PY_EXEC=
where py >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    set PY_EXEC=py
) else (
    where python >nul 2>nul
    if %ERRORLEVEL% EQU 0 (
        set PY_EXEC=python
    )
)

if "%PY_EXEC%"=="" (
    echo [ERROR] Python was not detected on your system.
    echo Please install Python 3 from https://www.python.org/
    echo NOTE: Make sure to check the box "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo [1/3] Detected Python command: %PY_EXEC%
%PY_EXEC% --version

echo.
echo [2/3] Installing / Verifying required libraries (Flask, PyCryptodome)...
%PY_EXEC% -m pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [WARNING] Pip install encountered an issue. Trying with user flag...
    %PY_EXEC% -m pip install --user -r requirements.txt
)

echo.
echo [3/3] Running verification tests...
%PY_EXEC% test_crypto.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [WARNING] Tests encountered an issue, but attempting to start web server...
)

echo.
echo ======================================================================
echo Starting AES Block Cipher Modes Comparison Web Application...
echo Open your browser and go to:
echo.
echo       http://127.0.0.1:5000
echo.
echo Keep this window open while using the application.
echo Press Ctrl+C in this window to stop the server.
echo ======================================================================
echo.

%PY_EXEC% app.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] The application stopped unexpectedly.
    pause
)
pause
