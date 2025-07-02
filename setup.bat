@echo off
echo ========================================
echo AI Comic Factory - Quick Setup
echo ========================================
echo.

echo This script will help you set up the AI Comic Factory application.
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js 18+ from https://nodejs.org
    pause
    exit /b 1
)

echo Python and Node.js are installed. Proceeding with setup...
echo.

REM Create backend environment file
if not exist "backend\.env" (
    echo Creating backend environment file...
    copy "backend\env.example" "backend\.env"
    echo.
    echo IMPORTANT: Please edit backend\.env and add your API keys:
    echo - OPENAI_API_KEY (required for ChatGPT and DALL-E)
    echo - REPLICATE_API_KEY (required for image generation)
    echo - HF_API_TOKEN (optional, for Hugging Face)
    echo.
)

REM Create frontend .env.local if needed
if not exist "frontend\.env.local" (
    echo Creating frontend environment file...
    echo NEXT_PUBLIC_API_URL=http://localhost:8000 > "frontend\.env.local"
)

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start the application:
echo.
echo 1. Start the backend:
echo    - Run: start-backend.bat
echo    - Or: cd backend && python main.py
echo.
echo 2. Start the frontend (in a new terminal):
echo    - Run: start-frontend.bat
echo    - Or: cd frontend && npm run dev
echo.
echo 3. Open your browser to: http://localhost:3000
echo.
echo Don't forget to add your API keys to backend\.env!
echo.
pause 