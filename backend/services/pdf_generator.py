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
        Create a comic PDF with images and captions
        """
        try:
            logger.info(f"Creating comic PDF with {len(image_paths)} images")
            
            # Create the PDF document
            doc = SimpleDocTemplate(
                output_path,
                pagesize=A4,
                rightMargin=self.margin,
                leftMargin=self.margin,
                topMargin=self.margin,
                bottomMargin=self.margin
            )
            
            # Get styles
            styles = getSampleStyleSheet()
            
            # Create custom styles for comic
            title_style = ParagraphStyle(
                'ComicTitle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=20,
                alignment=TA_CENTER,
                textColor=colors.darkblue
            )
            
            caption_style = ParagraphStyle(
                'ComicCaption',
                parent=styles['Normal'],
                fontSize=10,
                spaceAfter=10,
                alignment=TA_LEFT,
                textColor=colors.black
            )
            
            # Build the story
            story = []
            
            # Add title
            story.append(Paragraph("AI Generated Comic", title_style))
            story.append(Spacer(1, 20))
            
            # Process images and prompts
            for i, (image_path, prompt) in enumerate(zip(image_paths, prompts)):
                if os.path.exists(image_path):
                    try:
                        # Add panel number
                        panel_title = Paragraph(f"Panel {i+1}", styles['Heading2'])
                        story.append(panel_title)
                        story.append(Spacer(1, 10))
                        
                        # Add image
                        img = RLImage(image_path, width=self.image_width, height=self.image_height)
                        story.append(img)
                        story.append(Spacer(1, 10))
                        
                        # Add caption
                        caption = Paragraph(f"<b>Scene:</b> {prompt}", caption_style)
                        story.append(caption)
                        story.append(Spacer(1, 20))
                        
                    except Exception as e:
                        logger.error(f"Error processing image {i+1}: {str(e)}")
                        # Add placeholder text
                        story.append(Paragraph(f"Panel {i+1} - Image could not be loaded", styles['Normal']))
                        story.append(Spacer(1, 20))
                else:
                    logger.warning(f"Image file not found: {image_path}")
                    story.append(Paragraph(f"Panel {i+1} - Image file missing", styles['Normal']))
                    story.append(Spacer(1, 20))
            
            # Build the PDF
            doc.build(story)
            
            logger.info(f"Comic PDF created successfully: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error creating comic PDF: {str(e)}")
            raise
    
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