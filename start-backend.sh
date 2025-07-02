#!/bin/bash

echo "Starting AI Comic Factory Backend..."
echo

cd backend

echo "Creating virtual environment if it doesn't exist..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created."
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo
echo "Starting FastAPI server..."
echo "Backend will be available at: http://localhost:8000"
echo
python main.py 