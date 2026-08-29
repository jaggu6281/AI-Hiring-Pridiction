@echo off
REM AI Hiring Prediction System - GitHub Push Script for Windows

echo.
echo ====================================================
echo AI Hiring Prediction - GitHub Push Setup
echo ====================================================
echo.

REM Check if git is installed
where git >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Git is not installed or not in PATH
    echo Please install Git from: https://git-scm.com/download/win
    echo Then run this script again
    pause
    exit /b 1
)

echo [1/5] Initializing Git repository...
git init
if %ERRORLEVEL% NEQ 0 echo ERROR: Failed to initialize repository & pause & exit /b 1

echo [2/5] Adding all files...
git add .
if %ERRORLEVEL% NEQ 0 echo ERROR: Failed to add files & pause & exit /b 1

echo [3/5] Creating initial commit...
git commit -m "Initial commit: AI Hiring Prediction System - Ready for production"
if %ERRORLEVEL% NEQ 0 echo ERROR: Failed to create commit & pause & exit /b 1

echo.
echo ====================================================
echo NEXT STEPS:
echo ====================================================
echo.
echo 1. Go to GitHub.com and create a new repository
echo    - Repository name: ai-hiring-prediction
echo    - DO NOT initialize with README
echo.
echo 2. Copy your repository URL
echo    (Format: https://github.com/YOUR_USERNAME/ai-hiring-prediction.git)
echo.
echo 3. Run this command with your repository URL:
echo.
echo    git remote add origin YOUR_REPOSITORY_URL
echo    git branch -M main
echo    git push -u origin main
echo.
echo 4. Or run the interactive setup:
echo.
set /p repo_url="Enter your GitHub repository URL (or press Enter to skip): "

if not "%repo_url%"=="" (
    echo.
    echo [4/5] Adding remote origin...
    git remote add origin %repo_url%
    if %ERRORLEVEL% NEQ 0 echo ERROR: Failed to add remote & pause & exit /b 1
    
    echo [5/5] Pushing to GitHub...
    git branch -M main
    git push -u origin main
    if %ERRORLEVEL% NEQ 0 (
        echo ERROR: Failed to push to GitHub
        echo Please check your repository URL and try again
        pause
        exit /b 1
    )
    
    echo.
    echo ====================================================
    echo SUCCESS! Code pushed to GitHub
    echo ====================================================
    echo.
    echo Next: Deploy on Render
    echo See GITHUB_RENDER_DEPLOYMENT.md for instructions
    echo.
    pause
) else (
    echo Skipped GitHub push setup
    echo Run manually when ready with your repository URL
    pause
)
