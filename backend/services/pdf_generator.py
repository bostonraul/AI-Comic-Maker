import os
import logging
from typing import List
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Image as RLImage, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

logger = logging.getLogger(__name__)

class PDFGenerator:
    def __init__(self):
        self.page_width, self.page_height = A4
        self.margin = 0.5 * inch
        self.image_width = 3 * inch
        self.image_height = 3 * inch
        
    async def create_comic_pdf(
        self, 
        image_paths: List[str], 
        prompts: List[str], 
        output_path: str
    ) -> str:
        """
        Create a comic PDF with images and captions in a 2x2 grid per page
        """
        # Use the simple grid layout for all comics
        return self.create_simple_comic_pdf(image_paths, prompts, output_path)
    
    def create_simple_comic_pdf(
        self, 
        image_paths: List[str], 
        prompts: List[str], 
        output_path: str
    ) -> str:
        """
        Create a simpler comic PDF layout with 2x2 grid
        """
        try:
            logger.info(f"Creating simple comic PDF with {len(image_paths)} images")
            
            # Create canvas
            c = canvas.Canvas(output_path, pagesize=A4)
            width, height = A4
            
            # Calculate layout
            margin = 50
            image_width = (width - 3 * margin) / 2
            image_height = (height - 3 * margin) / 2
            
            # Add title
            c.setFont("Helvetica-Bold", 24)
            c.drawCentredString(width/2, height - margin, "AI Generated Comic")
            
            # Process images in 2x2 grid
            for i, (image_path, prompt) in enumerate(zip(image_paths, prompts)):
                if i >= 4:  # Only first 4 images per page
                    break
                    
                if os.path.exists(image_path):
                    try:
                        # Calculate position (2x2 grid)
                        row = i // 2
                        col = i % 2
                        
                        x = margin + col * (image_width + margin)
                        y = height - margin - 100 - row * (image_height + margin)
                        
                        # Add image
                        c.drawImage(image_path, x, y, width=image_width, height=image_height)
                        
                        # Add panel number
                        c.setFont("Helvetica-Bold", 12)
                        c.drawString(x, y + image_height + 10, f"Panel {i+1}")
                        
                        # Add caption (truncated)
                        c.setFont("Helvetica", 8)
                        truncated_prompt = prompt[:60] + "..." if len(prompt) > 60 else prompt
                        c.drawString(x, y + image_height + 25, truncated_prompt)
                        
                    except Exception as e:
                        logger.error(f"Error processing image {i+1}: {str(e)}")
                        # Draw placeholder
                        c.rect(x, y, image_width, image_height)
                        c.drawString(x + 10, y + image_height/2, f"Panel {i+1} - Error")
            
            c.save()
            logger.info(f"Simple comic PDF created: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error creating simple comic PDF: {str(e)}")
            raise
    
    def create_placeholder_pdf(self, output_path: str, prompts: List[str]) -> str:
        """
        Create a placeholder PDF when image generation fails
        """
        try:
            c = canvas.Canvas(output_path, pagesize=A4)
            width, height = A4
            
            # Add title
            c.setFont("Helvetica-Bold", 24)
            c.drawCentredString(width/2, height - 50, "AI Generated Comic")
            
            # Add subtitle
            c.setFont("Helvetica", 14)
            c.drawCentredString(width/2, height - 80, "Image generation failed - showing prompts only")
            
            # Add prompts
            y_position = height - 120
            for i, prompt in enumerate(prompts):
                if y_position < 50:  # Start new page if needed
                    c.showPage()
                    y_position = height - 50
                
                c.setFont("Helvetica-Bold", 12)
                c.drawString(50, y_position, f"Panel {i+1}:")
                
                c.setFont("Helvetica", 10)
                # Wrap text
                words = prompt.split()
                line = ""
                for word in words:
                    test_line = line + word + " "
                    if c.stringWidth(test_line, "Helvetica", 10) < width - 100:
                        line = test_line
                    else:
                        c.drawString(70, y_position - 15, line)
                        y_position -= 20
                        line = word + " "
                
                if line:
                    c.drawString(70, y_position - 15, line)
                
                y_position -= 30
            
            c.save()
            logger.info(f"Placeholder PDF created: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error creating placeholder PDF: {str(e)}")
            raise 