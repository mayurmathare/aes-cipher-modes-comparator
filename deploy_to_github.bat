@echo off
title Deploy to GitHub & GitHub Pages
cd /d "%~dp0"

echo ======================================================================
echo          Deploy AES Cipher Simulator to GitHub & GitHub Pages
echo ======================================================================
echo.

echo [1/3] Staging all project files and GitHub Pages workflow...
git add .

echo.
echo [2/3] Creating deployment commit...
git commit -m "Deploy AES Block Cipher Modes Comparison to GitHub Pages"

echo.
echo [3/3] Pushing to GitHub repository (main branch)...
git branch -M main
git push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ======================================================================
    echo [SUCCESS] Code pushed to GitHub successfully!
    echo.
    echo Repository: https://github.com/mayurmathare265/aes-cipher-modes-comparator
    echo.
    echo To activate your live website on GitHub Pages:
    echo 1. Go to: https://github.com/mayurmathare265/aes-cipher-modes-comparator/settings/pages
    echo 2. Under "Build and deployment" -> "Source", select "GitHub Actions"
    echo    (Or choose "Deploy from a branch" -> "main" -> root "/").
    echo.
    echo Your live website will be accessible at:
    echo https://mayurmathare265.github.io/aes-cipher-modes-comparator/
    echo ======================================================================
) else (
    echo.
    echo [NOTE] Push did not complete. If you are prompted in your browser to sign in,
    echo please complete GitHub authentication and run this script again.
)

pause
