#!/bin/bash

echo "========================================"
echo "AI Comic Factory - Quick Setup"
echo "========================================"
echo

echo "This script will help you set up the AI Comic Factory application."
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8+ from https://python.org"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js is not installed or not in PATH"
    echo "Please install Node.js 18+ from https://nodejs.org"
    exit 1
fi

echo "Python and Node.js are installed. Proceeding with setup..."
echo

# Create backend environment file
if [ ! -f "backend/.env" ]; then
    echo "Creating backend environment file..."
    cp "backend/env.example" "backend/.env"
    echo
    echo "IMPORTANT: Please edit backend/.env and add your API keys:"
    echo "- OPENAI_API_KEY (required for ChatGPT and DALL-E)"
    echo "- REPLICATE_API_KEY (required for image generation)"
    echo "- HF_API_TOKEN (optional, for Hugging Face)"
    echo
fi

# Create frontend .env.local if needed
if [ ! -f "frontend/.env.local" ]; then
    echo "Creating frontend environment file..."
    echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > "frontend/.env.local"
fi

# Make scripts executable
chmod +x start-backend.sh
chmod +x start-frontend.sh

echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo
echo "To start the application:"
echo
echo "1. Start the backend:"
echo "   - Run: ./start-backend.sh"
echo "   - Or: cd backend && python main.py"
echo
echo "2. Start the frontend (in a new terminal):"
echo "   - Run: ./start-frontend.sh"
echo "   - Or: cd frontend && npm run dev"
echo
echo "3. Open your browser to: http://localhost:3000"
echo
echo "Don't forget to add your API keys to backend/.env!"
echo 