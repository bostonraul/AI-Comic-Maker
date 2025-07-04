from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import os
import zipfile
import tempfile
import asyncio
import aiofiles
from pathlib import Path
import logging
from datetime import datetime

from services.chatgpt_service import ChatGPTService
from services.comic_generator import ComicGenerator
from services.pdf_generator import PDFGenerator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Comic Factory API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
chatgpt_service = ChatGPTService()
comic_generator = ComicGenerator()
pdf_generator = PDFGenerator()

class ComicRequest(BaseModel):
    genre: str
    setting: str
    characters: str

class GenerateComicRequest(BaseModel):
    prompts: List[dict]  # Each prompt is an object with description and dialogue

class PanelPrompt(BaseModel):
    description: str
    dialogue: str

class ComicResponse(BaseModel):
    success: bool
    message: str
    zip_url: Optional[str] = None
    pdf_url: Optional[str] = None
    error: Optional[str] = None
    prompts: Optional[List[PanelPrompt]] = None

@app.get("/")
async def root():
    return {"message": "AI Comic Factory API is running!"}

@app.post("/generate-prompts", response_model=ComicResponse)
async def generate_prompts(request: ComicRequest):
    """Generate 10 illustration prompts and dialogue using ChatGPT based on user input"""
    try:
        logger.info(f"Generating prompts for genre: {request.genre}, setting: {request.setting}")
        prompts = await chatgpt_service.generate_illustration_prompts(
            genre=request.genre,
            setting=request.setting,
            characters=request.characters
        )
        # prompts is a list of dicts with description and dialogue
        panel_prompts = [PanelPrompt(**p) for p in prompts]
        return {
            "success": True,
            "message": "Prompts generated successfully",
            "prompts": panel_prompts
        }
    except Exception as e:
        logger.error(f"Error generating prompts: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate prompts: {str(e)}")

@app.post("/generate-comic", response_model=ComicResponse)
async def generate_comic(request: GenerateComicRequest, background_tasks: BackgroundTasks):
    """Generate comic images from prompts and return ZIP file (TEMP: only 2 images for dev)"""
    try:
        logger.info(f"Generating comic with {len(request.prompts)} prompts")
        prompts_to_use = request.prompts[:2]
        if len(prompts_to_use) != 2:
            raise HTTPException(status_code=400, detail="Exactly 2 prompts are required for dev mode")
        temp_dir = tempfile.mkdtemp(prefix="comic_")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Extract descriptions and dialogues
        descriptions = [p['description'] for p in prompts_to_use]
        dialogues = [p['dialogue'] for p in prompts_to_use]
        # Generate images with dialogue overlays
        image_paths = []
        for i, (desc, dialogue) in enumerate(zip(descriptions, dialogues)):
            image_path = await comic_generator._generate_with_replicate(desc, temp_dir, i+1, dialogue)
            image_paths.append(image_path)
        zip_filename = f"comic_{timestamp}.zip"
        zip_path = os.path.join(temp_dir, zip_filename)
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for i, image_path in enumerate(image_paths):
                if os.path.exists(image_path):
                    zipf.write(image_path, f"panel_{i+1:02d}.png")
        pdf_filename = f"comic_{timestamp}.pdf"
        pdf_path = os.path.join(temp_dir, pdf_filename)
        await pdf_generator.create_comic_pdf(
            image_paths=image_paths,
            prompts=descriptions,
            output_path=pdf_path
        )
        with zipfile.ZipFile(zip_path, 'a') as zipf:
            zipf.write(pdf_path, pdf_filename)
        await asyncio.sleep(1)
        background_tasks.add_task(cleanup_temp_files, temp_dir, 3600)
        return ComicResponse(
            success=True,
            message="Comic generated successfully",
            zip_url=f"/download/{zip_filename}",
            pdf_url=f"/download/{pdf_filename}"
        )
    except Exception as e:
        logger.error(f"Error generating comic: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate comic: {str(e)}")

@app.get("/download/{filename}")
async def download_file(filename: str):
    temp_dir = tempfile.gettempdir()
    # Search all subdirectories for the file
    for root, dirs, files in os.walk(temp_dir):
        if filename in files:
            file_path = os.path.join(root, filename)
            return FileResponse(
                path=file_path,
                filename=filename,
                media_type='application/octet-stream'
            )
    raise HTTPException(status_code=404, detail="File not found")

async def cleanup_temp_files(temp_dir: str, delay_seconds: int):
    """Clean up temporary files after delay"""
    await asyncio.sleep(delay_seconds)
    try:
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)
        logger.info(f"Cleaned up temporary directory: {temp_dir}")
    except Exception as e:
        logger.error(f"Error cleaning up temp directory: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 