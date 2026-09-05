# run.ps1 - PowerShell launcher for AES Block Cipher Modes Comparator
$ErrorActionPreference = "Continue"

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "      AES Block Cipher Modes Comparison (Cryptography Practical)      " -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

# Locate Python or Py launcher
$pyCommand = $null
if (Get-Command "py" -ErrorAction SilentlyContinue) {
    $pyCommand = "py"
} elseif (Get-Command "python" -ErrorAction SilentlyContinue) {
    $pyCommand = "python"
}

if (-not $pyCommand) {
    Write-Host "[ERROR] Python was not found in your system PATH." -ForegroundColor Red
    Write-Host "Please install Python from https://www.python.org/ (ensure 'Add Python to PATH' is checked)." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[1/3] Using Python: $pyCommand" -ForegroundColor Gray
& $pyCommand --version

Write-Host "`n[2/3] Installing/Verifying Flask and PyCryptodome..." -ForegroundColor Gray
& $pyCommand -m pip install -r requirements.txt

Write-Host "`n[3/3] Starting web server..." -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Yellow
Write-Host "Web app running at: http://127.0.0.1:5000" -ForegroundColor Yellow
Write-Host "======================================================================" -ForegroundColor Yellow

# Optionally open browser automatically
try {
    Start-Process "http://127.0.0.1:5000"
} catch {}

& $pyCommand app.py
Read-Host "Press Enter to exit"
