#!/bin/bash

echo "🚀 Setting up AI Comic Factory in Codespaces..."

# Install Python dependencies
echo "📦 Installing Python dependencies..."
cd backend
python -m pip install --upgrade pip
pip install -r requirements.txt
cd ..

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
cd frontend
npm install
cd ..

# Create .env file from template if it doesn't exist
if [ ! -f "backend/.env" ]; then
    echo "📝 Creating .env file from template..."
    cp backend/env.example backend/.env
    echo "⚠️  IMPORTANT: Please add your API keys to backend/.env"
    echo "   - OPENAI_API_KEY"
    echo "   - REPLICATE_API_KEY"
fi

# Create frontend .env.local if it doesn't exist
if [ ! -f "frontend/.env.local" ]; then
    echo "📝 Creating frontend environment file..."
    echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > frontend/.env.local
fi

echo "✅ Setup complete!"
echo ""
echo "🎯 Next steps:"
echo "1. Add your API keys to backend/.env"
echo "2. Start the backend: cd backend && python main.py"
echo "3. Start the frontend: cd frontend && npm run dev"
echo "4. Open http://localhost:3000 in your browser"
echo ""
echo "🔧 Or use the provided scripts:"
echo "   ./start-backend.sh"
echo "   ./start-frontend.sh" 