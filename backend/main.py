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
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
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
    prompts: List[str]

class ComicResponse(BaseModel):
    success: bool
    message: str
    zip_url: Optional[str] = None
    pdf_url: Optional[str] = None
    error: Optional[str] = None

@app.get("/")
async def root():
    return {"message": "AI Comic Factory API is running!"}

@app.post("/generate-prompts", response_model=ComicResponse)
async def generate_prompts(request: ComicRequest):
    """Generate 10 illustration prompts using ChatGPT based on user input"""
    try:
        logger.info(f"Generating prompts for genre: {request.genre}, setting: {request.setting}")
        
        prompts = await chatgpt_service.generate_illustration_prompts(
            genre=request.genre,
            setting=request.setting,
            characters=request.characters
        )
        
        return ComicResponse(
            success=True,
            message="Prompts generated successfully",
            prompts=prompts
        )
    except Exception as e:
        logger.error(f"Error generating prompts: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate prompts: {str(e)}")

@app.post("/generate-comic", response_model=ComicResponse)
async def generate_comic(request: GenerateComicRequest, background_tasks: BackgroundTasks):
    """Generate comic images from prompts and return ZIP file"""
    try:
        logger.info(f"Generating comic with {len(request.prompts)} prompts")
        
        if len(request.prompts) != 10:
            raise HTTPException(status_code=400, detail="Exactly 10 prompts are required")
        
        # Create temporary directory for this generation
        temp_dir = tempfile.mkdtemp(prefix="comic_")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Generate images
        image_paths = await comic_generator.generate_images(
            prompts=request.prompts,
            output_dir=temp_dir
        )
        
        # Create ZIP file
        zip_filename = f"comic_{timestamp}.zip"
        zip_path = os.path.join(temp_dir, zip_filename)
        
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for i, image_path in enumerate(image_paths):
                if os.path.exists(image_path):
                    zipf.write(image_path, f"panel_{i+1:02d}.png")
        
        # Create PDF with captions
        pdf_filename = f"comic_{timestamp}.pdf"
        pdf_path = os.path.join(temp_dir, pdf_filename)
        
        await pdf_generator.create_comic_pdf(
            image_paths=image_paths,
            prompts=request.prompts,
            output_path=pdf_path
        )
        
        # Add PDF to ZIP
        with zipfile.ZipFile(zip_path, 'a') as zipf:
            zipf.write(pdf_path, pdf_filename)
        
        # Schedule cleanup
        background_tasks.add_task(cleanup_temp_files, temp_dir, 3600)  # Clean up in 1 hour
        
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
    """Download generated files"""
    # This is a simplified version - in production you'd want proper file storage
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='application/octet-stream'
    )

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