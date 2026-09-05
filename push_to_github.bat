@echo off
title Upload Project to GitHub
cd /d "%~dp0"

echo ======================================================================
echo             Upload Project to GitHub Repository
echo ======================================================================
echo.

set /p REPO_URL="Enter your GitHub Repository URL (e.g. https://github.com/YourUsername/repo-name.git): "

if "%REPO_URL%"=="" (
    echo [ERROR] No repository URL was entered.
    pause
    exit /b 1
)

echo.
echo [1/4] Initializing Git repository...
git init

echo.
echo [2/4] Staging all files...
git add .

echo.
echo [3/4] Creating initial commit...
git commit -m "Initial commit: AES Block Cipher Modes Comparison Web App"

echo.
echo [4/4] Setting main branch and pushing to remote...
git branch -M main
git remote remove origin 2>nul
git remote add origin %REPO_URL%
git push -u origin main

echo.
if %ERRORLEVEL% EQU 0 (
    echo ======================================================================
    echo [SUCCESS] Successfully uploaded to GitHub!
    echo ======================================================================
) else (
    echo [NOTE] If this is your first time connecting Git to GitHub on this PC,
    echo Windows will prompt you to log into your GitHub account in a popup.
)

pause
