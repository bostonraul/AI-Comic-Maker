---
title: AI Comic Factory
emoji: 👩‍🎨
colorFrom: red
colorTo: yellow
sdk: docker
pinned: true
app_port: 3000
disable_embedding: false
short_description: Create your own AI comic with a single prompt
hf_oauth: true
hf_oauth_expiration_minutes: 43200
hf_oauth_scopes: [inference-api]
---

# AI Comic Factory - Complete Application

A full-stack application that generates AI-powered comics from user input. The app uses ChatGPT to generate 10 illustration prompts based on genre, setting, and characters, then creates comic images using AI image generation APIs, and finally assembles them into a PDF comic.

## 🚀 Features

- **Smart Prompt Generation**: Uses ChatGPT to create 10 unique illustration prompts
- **AI Image Generation**: Supports multiple rendering engines (Replicate, OpenAI DALL-E, Hugging Face)
- **PDF Assembly**: Automatically creates a comic PDF with images and captions
- **ZIP Download**: Provides both individual images and assembled PDF in a ZIP file
- **Modern UI**: Beautiful React frontend with Tailwind CSS
- **FastAPI Backend**: High-performance Python backend with async support

## 🏗️ Architecture

```
User Input (Genre, Setting, Characters)
    ↓
ChatGPT → 10 Illustration Prompts
    ↓
AI Image Generation (Replicate/OpenAI/Hugging Face)
    ↓
PDF Assembly with Captions
    ↓
ZIP File Download
```

## 📁 Project Structure

```
ai-comic-factory/
├── backend/                 # FastAPI backend
│   ├── main.py             # Main FastAPI application
│   ├── services/           # Business logic services
│   │   ├── chatgpt_service.py
│   │   ├── comic_generator.py
│   │   └── pdf_generator.py
│   ├── requirements.txt    # Python dependencies
│   └── env.example        # Environment variables template
├── frontend/               # Next.js frontend
│   ├── app/               # Next.js app directory
│   │   ├── page.tsx       # Main page component
│   │   ├── layout.tsx     # Root layout
│   │   └── globals.css    # Global styles
│   ├── package.json       # Node.js dependencies
│   └── tailwind.config.js # Tailwind configuration
└── README.md              # This file
```

## 🛠️ Installation & Setup

### Option 1: GitHub Codespaces (Recommended) 🚀

**Easiest way to get started - no local setup required!**

1. **Fork this repository** to your GitHub account
2. **Open in Codespaces**: Click the green "Code" button → "Codespaces" → "Create codespace on main"
3. **Add your API keys** to `backend/.env` (see [CODESPACES.md](CODESPACES.md) for detailed instructions)
4. **Start the app**: Use the provided scripts or run manually

**✅ Benefits:**
- No local installation required
- Automatic dependency installation
- Pre-configured development environment
- Free cloud development environment

### Option 2: Local Development

### Prerequisites

- Python 3.8+
- Node.js 18+
- API keys for:
  - OpenAI (for ChatGPT and DALL-E)
  - Replicate (for SDXL)
  - Hugging Face (optional)

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp env.example .env
   # Edit .env with your API keys
   ```

5. **Run the backend:**
   ```bash
   python main.py
   ```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Run the frontend:**
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:3000`

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# API Keys
OPENAI_API_KEY=your_openai_api_key_here
REPLICATE_API_KEY=your_replicate_api_key_here
HF_API_TOKEN=your_huggingface_token_here

# Rendering Engine Configuration
# Options: REPLICATE, OPENAI, HUGGINGFACE
RENDERING_ENGINE=REPLICATE

# Server Configuration
HOST=0.0.0.0
PORT=8000

# Logging
LOG_LEVEL=INFO
```

### API Keys Setup

1. **OpenAI API Key**: Get from [OpenAI Platform](https://platform.openai.com/)
2. **Replicate API Key**: Get from [Replicate](https://replicate.com/)
3. **Hugging Face Token**: Get from [Hugging Face](https://huggingface.co/settings/tokens)

## 🎯 Usage

1. **Open the application** at `http://localhost:3000`

2. **Fill in the form** with:
   - **Genre**: e.g., "Sci-Fi", "Fantasy", "Mystery"
   - **Setting**: e.g., "Space Station", "Medieval Castle"
   - **Characters**: e.g., "Robot detective", "Wizard apprentice"

3. **Generate Prompts**: Click "Generate 10 Illustration Prompts" to get AI-generated prompts

4. **Generate Comic**: Click "Generate Comic" to create images and PDF

5. **Download**: Get your comic as a ZIP file containing all images and the assembled PDF

## 🔌 API Endpoints

### Backend API

- `POST /generate-prompts` - Generate 10 illustration prompts
- `POST /generate-comic` - Generate comic images and PDF
- `GET /download/{filename}` - Download generated files

### Request Examples

**Generate Prompts:**
```json
{
  "genre": "Sci-Fi",
  "setting": "Space Station",
  "characters": "Robot detective"
}
```

**Generate Comic:**
```json
{
  "prompts": [
    "A robot detective examining evidence in a futuristic space station",
    "The detective discovering a mysterious alien artifact",
    "..."
  ]
}
```

## 🎨 Customization

### Adding New Rendering Engines

To add a new image generation service, modify `backend/services/comic_generator.py`:

1. Add the new engine to the `_generate_single_image` method
2. Create a new method like `_generate_with_newservice`
3. Update the environment variables

### Customizing PDF Layout

Modify `backend/services/pdf_generator.py` to change:
- Page layout and styling
- Image sizes and positioning
- Caption formatting
- Color schemes

### Frontend Styling

The frontend uses Tailwind CSS. Modify:
- `frontend/tailwind.config.js` for theme customization
- `frontend/app/globals.css` for global styles
- Component files for specific styling

## 🚀 Deployment

### Backend Deployment

The backend can be deployed to:
- **Heroku**: Use the provided `requirements.txt`
- **Railway**: Direct deployment from GitHub
- **DigitalOcean App Platform**: Container deployment
- **AWS/GCP**: Container deployment with Docker

### Frontend Deployment

The frontend can be deployed to:
- **Vercel**: Direct deployment from GitHub
- **Netlify**: Build and deploy
- **AWS S3 + CloudFront**: Static hosting

### Docker Deployment

Create a `docker-compose.yml`:

```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - REPLICATE_API_KEY=${REPLICATE_API_KEY}
  
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
```

## 🐛 Troubleshooting

### Common Issues

1. **API Key Errors**: Ensure all API keys are correctly set in `.env`
2. **Image Generation Fails**: Check API quotas and rate limits
3. **PDF Generation Issues**: Ensure all image files exist and are readable
4. **CORS Errors**: Verify the backend CORS configuration matches your frontend URL

### Logs

Check the backend logs for detailed error information:
```bash
# Backend logs
python main.py

# Frontend logs
npm run dev
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Original AI Comic Factory by [@jbilcke-hf](https://github.com/jbilcke-hf)
- Stable Diffusion XL by Stability AI
- ChatGPT by OpenAI
- Next.js and FastAPI communities

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs for error details
3. Open an issue on GitHub
4. Check the original AI Comic Factory documentation

Last release: AI Comic Factory 1.2

The AI Comic Factory will soon have an official website: [aicomicfactory.app](https://aicomicfactory.app)

For more information about my other projects please check [linktr.ee/FLNGR](https://linktr.ee/FLNGR).

## Running the project at home

First, I would like to highlight that everything is open-source (see [here](https://huggingface.co/spaces/jbilcke-hf/ai-comic-factory/tree/main), [here](https://huggingface.co/spaces/jbilcke-hf/VideoChain-API/tree/main), [here](https://huggingface.co/spaces/hysts/SD-XL/tree/main), [here](https://github.com/huggingface/text-generation-inference)).

However the project isn't a monolithic Space that can be duplicated and ran immediately:
it requires various components to run for the frontend, backend, LLM, SDXL etc.

If you try to duplicate the project, open the `.env` you will see it requires some variables.

Provider config:
- `LLM_ENGINE`: can be one of `INFERENCE_API`, `INFERENCE_ENDPOINT`, `OPENAI`, `GROQ`, `ANTHROPIC`
- `RENDERING_ENGINE`: can be one of: "INFERENCE_API", "INFERENCE_ENDPOINT", "REPLICATE", "VIDEOCHAIN", "OPENAI" for now, unless you code your custom solution

Auth config:
- `AUTH_HF_API_TOKEN`:  if you decide to use Hugging Face for the LLM engine (inference api model or a custom inference endpoint)
- `AUTH_OPENAI_API_KEY`: to use OpenAI for the LLM engine
- `AUTH_GROQ_API_KEY`: to use Groq for the LLM engine
- `AUTH_ANTHROPIC_API_KEY`: to use Anthropic (Claude) for the LLM engine
- `AUTH_VIDEOCHAIN_API_TOKEN`: secret token to access the VideoChain API server
- `AUTH_REPLICATE_API_TOKEN`: in case you want to use Replicate.com

Rendering config:
- `RENDERING_HF_INFERENCE_ENDPOINT_URL`: necessary if you decide to use a custom inference endpoint
- `RENDERING_REPLICATE_API_MODEL_VERSION`: url to the VideoChain API server
- `RENDERING_HF_INFERENCE_ENDPOINT_URL`: optional, default to nothing
- `RENDERING_HF_INFERENCE_API_BASE_MODEL`: optional, defaults to "stabilityai/stable-diffusion-xl-base-1.0"
- `RENDERING_HF_INFERENCE_API_REFINER_MODEL`: optional, defaults to "stabilityai/stable-diffusion-xl-refiner-1.0"
- `RENDERING_REPLICATE_API_MODEL`: optional, defaults to "stabilityai/sdxl"
- `RENDERING_REPLICATE_API_MODEL_VERSION`: optional, in case you want to change the version

Language model config (depending on the LLM engine you decide to use):
- `LLM_HF_INFERENCE_ENDPOINT_URL`: "<use your own>"
- `LLM_HF_INFERENCE_API_MODEL`: "HuggingFaceH4/zephyr-7b-beta"
- `LLM_OPENAI_API_BASE_URL`: "https://api.openai.com/v1"
- `LLM_OPENAI_API_MODEL`: "gpt-4-turbo"
- `LLM_GROQ_API_MODEL`: "mixtral-8x7b-32768"
- `LLM_ANTHROPIC_API_MODEL`: "claude-3-opus-20240229"

In addition, there are some community sharing variables that you can just ignore.
Those variables are not required to run the AI Comic Factory on your own website or computer
(they are meant to create a connection with the Hugging Face community,
and thus only make sense for official Hugging Face apps):
- `NEXT_PUBLIC_ENABLE_COMMUNITY_SHARING`: you don't need this
- `COMMUNITY_API_URL`: you don't need this
- `COMMUNITY_API_TOKEN`: you don't need this
- `COMMUNITY_API_ID`: you don't need this

Please read the `.env` default config file for more informations.
To customise a variable locally, you should create a `.env.local`
(do not commit this file as it will contain your secrets).

-> If you intend to run it with local, cloud-hosted and/or proprietary models **you are going to need to code 👨‍💻**.

## The LLM API (Large Language Model)

Currently the AI Comic Factory uses [zephyr-7b-beta](https://huggingface.co/HuggingFaceH4/zephyr-7b-beta) through an [Inference Endpoint](https://huggingface.co/docs/inference-endpoints/index).

You have multiple options:

### Option 1: Use an Inference API model

This is a new option added recently, where you can use one of the models from the Hugging Face Hub. By default we suggest to use [zephyr-7b-beta](https://huggingface.co/HuggingFaceH4/zephyr-7b-beta) as it will provide better results than the 7b model.

To activate it, create a `.env.local` configuration file:

```bash
LLM_ENGINE="INFERENCE_API"

HF_API_TOKEN="Your Hugging Face token"

# "HuggingFaceH4/zephyr-7b-beta" is used by default, but you can change this
# note: You should use a model able to generate JSON responses,
# so it is storngly suggested to use at least the 34b model
HF_INFERENCE_API_MODEL="HuggingFaceH4/zephyr-7b-beta"
```

### Option 2: Use an Inference Endpoint URL

If you would like to run the AI Comic Factory on a private LLM running on the Hugging Face Inference Endpoint service, create a `.env.local` configuration file:

```bash
LLM_ENGINE="INFERENCE_ENDPOINT"

HF_API_TOKEN="Your Hugging Face token"

HF_INFERENCE_ENDPOINT_URL="path to your inference endpoint url"
```

To run this kind of LLM locally, you can use [TGI](https://github.com/huggingface/text-generation-inference) (Please read [this post](https://github.com/huggingface/text-generation-inference/issues/726) for more information about the licensing).

### Option 3: Use an OpenAI API Key

This is a new option added recently, where you can use OpenAI API with an OpenAI API Key.

To activate it, create a `.env.local` configuration file:

```bash
LLM_ENGINE="OPENAI"

# default openai api base url is: https://api.openai.com/v1
LLM_OPENAI_API_BASE_URL="A custom OpenAI API Base URL if you have some special privileges"

LLM_OPENAI_API_MODEL="gpt-4-turbo"

AUTH_OPENAI_API_KEY="Yourown OpenAI API Key"
```
### Option 4: (new, experimental) use Groq

```bash
LLM_ENGINE="GROQ"

LLM_GROQ_API_MODEL="mixtral-8x7b-32768"

AUTH_GROQ_API_KEY="Your own GROQ API Key"
```
### Option 5: (new, experimental) use Anthropic (Claude)

```bash
LLM_ENGINE="ANTHROPIC"

LLM_ANTHROPIC_API_MODEL="claude-3-opus-20240229"

AUTH_ANTHROPIC_API_KEY="Your own ANTHROPIC API Key"
```

### Option 6: Fork and modify the code to use a different LLM system

Another option could be to disable the LLM completely and replace it with another LLM protocol and/or provider (eg. Claude, Replicate), or a human-generated story instead (by returning mock or static data).

### Notes

It is possible that I modify the AI Comic Factory to make it easier in the future (eg. add support for Claude or Replicate)

## The Rendering API

This API is used to generate the panel images. This is an API I created for my various projects at Hugging Face.

I haven't written documentation for it yet, but basically it is "just a wrapper ™" around other existing APIs:

- The [hysts/SD-XL](https://huggingface.co/spaces/hysts/SD-XL?duplicate=true) Space by [@hysts](https://huggingface.co/hysts)
- And other APIs for making videos, adding audio etc.. but you won't need them for the AI Comic Factory

### Option 1: Deploy VideoChain yourself

You will have to [clone](https://huggingface.co/spaces/jbilcke-hf/VideoChain-API?duplicate=true) the [source-code](https://huggingface.co/spaces/jbilcke-hf/VideoChain-API/tree/main)

Unfortunately, I haven't had the time to write the documentation for VideoChain yet.
(When I do I will update this document to point to the VideoChain's README)


### Option 2: Use Replicate

To use Replicate, create a `.env.local` configuration file:

```bash
RENDERING_ENGINE="REPLICATE"

RENDERING_REPLICATE_API_MODEL="stabilityai/sdxl"

RENDERING_REPLICATE_API_MODEL_VERSION="da77bc59ee60423279fd632efb4795ab731d9e3ca9705ef3341091fb989b7eaf"

AUTH_REPLICATE_API_TOKEN="Your Replicate token"
```

### Option 3: Use another SDXL API

If you fork the project you will be able to modify the code to use the Stable Diffusion technology of your choice (local, open-source, proprietary, your custom HF Space etc).

It would even be something else, such as Dall-E.
