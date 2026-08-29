#!/bin/bash

# AI Hiring Prediction System - GitHub Push Script for Mac/Linux

set -e

echo ""
echo "===================================================="
echo "AI Hiring Prediction - GitHub Push Setup"
echo "===================================================="
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "ERROR: Git is not installed"
    echo "Please install Git and try again"
    exit 1
fi

echo "[1/5] Initializing Git repository..."
git init

echo "[2/5] Adding all files..."
git add .

echo "[3/5] Creating initial commit..."
git commit -m "Initial commit: AI Hiring Prediction System - Ready for production"

echo ""
echo "===================================================="
echo "NEXT STEPS:"
echo "===================================================="
echo ""
echo "1. Go to GitHub.com and create a new repository"
echo "   - Repository name: ai-hiring-prediction"
echo "   - DO NOT initialize with README"
echo ""
echo "2. Copy your repository URL"
echo "   (Format: https://github.com/YOUR_USERNAME/ai-hiring-prediction.git)"
echo ""
echo "3. Run these commands with your repository URL:"
echo ""
echo "   git remote add origin YOUR_REPOSITORY_URL"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""

read -p "Enter your GitHub repository URL (or press Enter to skip): " repo_url

if [ -n "$repo_url" ]; then
    echo ""
    echo "[4/5] Adding remote origin..."
    git remote add origin "$repo_url"
    
    echo "[5/5] Pushing to GitHub..."
    git branch -M main
    git push -u origin main
    
    echo ""
    echo "===================================================="
    echo "SUCCESS! Code pushed to GitHub"
    echo "===================================================="
    echo ""
    echo "Next: Deploy on Render"
    echo "See GITHUB_RENDER_DEPLOYMENT.md for instructions"
    echo ""
else
    echo "Skipped GitHub push setup"
    echo "Run manually when ready with your repository URL"
fi
