@echo off
title GitHub Setup - Tuition Station
cd /d "%~dp0.."
echo ====================================
echo     GitHub Setup - Tuition Station
echo ====================================
echo.

echo Step 1: Login to GitHub
echo.
"C:\Program Files\GitHub CLI\gh.exe" auth login -h github.com --web
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Login failed. Please try again.
    pause
    exit /b 1
)

echo.
echo Step 2: Creating GitHub repository...
"C:\Program Files\GitHub CLI\gh.exe" repo create eliascsebaust19/Tuition_Station --public --source=. --remote=origin --push

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ====================================
    echo    SUCCESS! Code pushed to GitHub!
    echo    https://github.com/eliascsebaust19/Tuition_Station
    echo ====================================
) else (
    echo.
    echo Trying to push to existing repo...
    git remote add origin https://github.com/eliascsebaust19/Tuition_Station.git 2>nul
    git push -u origin master
)

echo.
pause
