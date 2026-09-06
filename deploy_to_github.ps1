# deploy_to_github.ps1 - Push code and trigger GitHub Pages deployment
$ErrorActionPreference = "Continue"

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "       Deploy AES Cipher Simulator to GitHub & GitHub Pages           " -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

Write-Host "`n[1/3] Staging all files..." -ForegroundColor Gray
git add .

Write-Host "`n[2/3] Committing changes..." -ForegroundColor Gray
git commit -m "Deploy AES Block Cipher Modes Comparison to GitHub Pages"

Write-Host "`n[3/3] Pushing to GitHub (main branch)..." -ForegroundColor Gray
git branch -M main
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n======================================================================" -ForegroundColor Green
    Write-Host "[SUCCESS] Successfully pushed to GitHub!" -ForegroundColor Green
    Write-Host "Repository: https://github.com/mayurmathare/aes-cipher-modes-comparator" -ForegroundColor Yellow
    Write-Host "`nYour Live Web URL will be:" -ForegroundColor Cyan
    Write-Host "https://mayurmathare.github.io/aes-cipher-modes-comparator/" -ForegroundColor Green
    Write-Host "======================================================================" -ForegroundColor Green
} else {
    Write-Host "`n[NOTE] If authentication is required, please sign in via the browser popup and re-run." -ForegroundColor Yellow
}

Read-Host "`nPress Enter to exit"
