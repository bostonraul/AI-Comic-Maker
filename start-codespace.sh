#!/bin/bash

echo "🚀 Starting AI Comic Factory in Codespaces..."
echo ""

# Check if .env file exists and has API keys
if [ ! -f "backend/.env" ]; then
    echo "❌ Error: backend/.env file not found!"
    echo "Please create it from the template and add your API keys:"
    echo "cp backend/env.example backend/.env"
    echo "Then edit backend/.env with your OpenAI and Replicate API keys"
    exit 1
fi

# Check if API keys are set
if grep -q "your_openai_api_key_here\|your_replicate_api_key_here" backend/.env; then
    echo "⚠️  Warning: Please add your actual API keys to backend/.env"
    echo "   - OPENAI_API_KEY=sk-your_actual_key"
    echo "   - REPLICATE_API_KEY=r8_your_actual_key"
    echo ""
fi

echo "📦 Installing dependencies..."
cd backend
pip install -r requirements.txt
cd ..

cd frontend
npm install
cd ..

echo ""
echo "🎯 Starting the application..."
echo ""

# Start backend in background
echo "🔧 Starting backend server..."
cd backend
python main.py &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

# Start frontend
echo "🎨 Starting frontend server..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ AI Comic Factory is starting up!"
echo ""
echo "🌐 Access your application:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "🛑 To stop the application, press Ctrl+C"
echo ""

# Wait for user to stop
wait 