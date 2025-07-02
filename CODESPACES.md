# 🚀 AI Comic Factory - GitHub Codespaces Setup

This guide will help you set up and run the AI Comic Factory application in GitHub Codespaces.

## 📋 Prerequisites

- GitHub account
- OpenAI API key
- Replicate API key

## 🎯 Quick Start

### 1. **Fork/Clone the Repository**
```bash
# If you haven't already, fork this repository to your GitHub account
# Then clone it or use the "Code" button to open in Codespaces
```

### 2. **Open in Codespaces**
1. Go to your repository on GitHub
2. Click the green "Code" button
3. Select "Codespaces" tab
4. Click "Create codespace on main"

### 3. **Set Up Environment Variables**
Once Codespaces opens, you'll need to add your API keys:

1. **Open the backend/.env file** in the editor
2. **Replace the placeholder values** with your actual API keys:

```env
# API Keys
OPENAI_API_KEY=sk-your_actual_openai_key_here
REPLICATE_API_KEY=r8_your_actual_replicate_key_here
HF_API_TOKEN=your_huggingface_token_here

# Rendering Engine Configuration
RENDERING_ENGINE=REPLICATE

# Server Configuration
HOST=0.0.0.0
PORT=8000

# Logging
LOG_LEVEL=INFO
```

### 4. **Start the Application**

#### **Option A: Use the provided scripts**
```bash
# Start backend (in one terminal)
./start-backend.sh

# Start frontend (in another terminal)
./start-frontend.sh
```

#### **Option B: Manual start**
```bash
# Terminal 1 - Start backend
cd backend
python main.py

# Terminal 2 - Start frontend
cd frontend
npm run dev
```

### 5. **Access the Application**
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🔧 Codespaces Features

### **Automatic Setup**
The `.devcontainer` configuration automatically:
- ✅ Installs Python 3.11
- ✅ Installs Node.js 18
- ✅ Installs all dependencies
- ✅ Sets up VS Code extensions
- ✅ Forwards ports 3000 and 8000

### **Port Forwarding**
- **Port 3000**: Frontend (Next.js)
- **Port 8000**: Backend (FastAPI)

### **VS Code Extensions**
- Python support
- TypeScript support
- Tailwind CSS IntelliSense
- Prettier formatting

## 🎨 Using the Application

1. **Fill in the form** with:
   - **Genre**: e.g., "Sci-Fi", "Fantasy", "Mystery"
   - **Setting**: e.g., "Space Station", "Medieval Castle"
   - **Characters**: e.g., "Robot detective", "Wizard apprentice"

2. **Generate Prompts**: Click "Generate 10 Illustration Prompts"

3. **Generate Comic**: Click "Generate Comic" to create images and PDF

4. **Download**: Get your comic as a ZIP file

## 🔑 Getting API Keys

### **OpenAI API Key**
1. Go to https://platform.openai.com/api-keys
2. Sign up/login
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)

### **Replicate API Key**
1. Go to https://replicate.com/account/api-tokens
2. Sign up/login
3. Click "Create API token"
4. Copy the token (starts with `r8_`)

## 🐛 Troubleshooting

### **Common Issues**

1. **"API key not found"**
   - Make sure you've added your API keys to `backend/.env`
   - Check that the keys are correct and active

2. **"Port already in use"**
   - Stop any running processes
   - Use different ports if needed

3. **"Dependencies not found"**
   - Run the setup script: `bash .devcontainer/setup.sh`
   - Or manually install: `pip install -r backend/requirements.txt`

### **Testing the Setup**
```bash
# Test if everything is working
python test-setup.py
```

## 💰 Cost Estimation

### **Per Comic (10 images):**
- **OpenAI ChatGPT**: ~$0.01-0.02
- **Replicate SDXL**: ~$0.20-0.50
- **Total**: ~$0.21-0.52 per comic

## 🚀 Deployment Options

### **Local Development**
- Use the provided scripts
- Access via localhost

### **Production Deployment**
- Deploy backend to Railway/Heroku
- Deploy frontend to Vercel/Netlify
- Set environment variables in deployment platform

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section
2. Review the logs in the terminal
3. Open an issue on GitHub
4. Check the original AI Comic Factory documentation

## 🎉 Success!

Once everything is set up, you'll have a fully functional AI Comic Factory running in the cloud! Create amazing comics with just a few clicks. 