# GitHub Login & Push Script - Tuition Station
Write-Host "=== GitHub Setup for Tuition Station ===" -ForegroundColor Cyan

# Add gh to PATH
$env:Path += ";C:\Program Files\GitHub CLI"

# Check if already logged in
$status = gh auth status 2>&1
if ($status -match "Logged in") {
    Write-Host "Already logged in to GitHub!" -ForegroundColor Green
} else {
    Write-Host "Step 1: Login to GitHub" -ForegroundColor Yellow
    Write-Host "A browser will open. Log in and authorize." -ForegroundColor Yellow
    gh auth login -h github.com --web
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Login failed!" -ForegroundColor Red
        exit 1
    }
}

Write-Host "Step 2: Creating GitHub repository 'Tuition_Station'..." -ForegroundColor Yellow
gh repo create eliascsebaust19/Tuition_Station --public --source=. --remote=origin --push

if ($LASTEXITCODE -eq 0) {
    Write-Host "==============================" -ForegroundColor Cyan
    Write-Host "SUCCESS! Repository created and code pushed!" -ForegroundColor Green
    Write-Host "URL: https://github.com/eliascsebaust19/Tuition_Station" -ForegroundColor Green
    Write-Host "==============================" -ForegroundColor Cyan
} else {
    Write-Host "Failed to create repo. Trying to push to existing repo..." -ForegroundColor Yellow
    git remote add origin https://github.com/eliascsebaust19/Tuition_Station.git 2>$null
    git push -u origin master
}

pause
