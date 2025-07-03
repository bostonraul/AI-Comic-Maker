import os
import asyncio
import logging
from typing import List
import replicate
import requests
from PIL import Image
import io
import base64
from dotenv import load_dotenv
from PIL import ImageDraw, ImageFont

load_dotenv()

logger = logging.getLogger(__name__)

class ComicGenerator:
    def __init__(self):
        self.rendering_engine = os.getenv("RENDERING_ENGINE", "REPLICATE")
        self.replicate_api_key = os.getenv("REPLICATE_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.hf_api_key = os.getenv("HF_API_TOKEN")
        
        # Initialize Replicate client if API key is available
        if self.replicate_api_key:
            self.replicate_client = replicate.Client(api_token=self.replicate_api_key)
        else:
            self.replicate_client = None
    
    async def generate_images(self, prompts: List[str], output_dir: str) -> List[str]:
        """
        Generate images from prompts using the configured rendering engine, in parallel
        """
        tasks = [
            self._generate_single_image(prompt, output_dir, i)
            for i, prompt in enumerate(prompts)
        ]
        return await asyncio.gather(*tasks)
    
    async def _generate_single_image(self, prompt: str, output_dir: str, panel_number: int) -> str:
        """
        Generate a single image using the configured rendering engine
        """
        try:
            if self.rendering_engine == "REPLICATE" and self.replicate_client:
                return await self._generate_with_replicate(prompt, output_dir, panel_number)
            elif self.rendering_engine == "OPENAI" and self.openai_api_key:
                return await self._generate_with_openai(prompt, output_dir, panel_number)
            elif self.rendering_engine == "HUGGINGFACE" and self.hf_api_key:
                return await self._generate_with_huggingface(prompt, output_dir, panel_number)
            else:
                logger.warning(f"Rendering engine {self.rendering_engine} not properly configured, using placeholder")
                return self._create_placeholder_image(output_dir, panel_number, prompt)
                
        except Exception as e:
            logger.error(f"Error in _generate_single_image: {str(e)}")
            return self._create_placeholder_image(output_dir, panel_number, prompt)
    
    async def _generate_with_replicate(self, prompt: str, output_dir: str, panel_number: int, dialogue: str = "") -> str:
        """
        Generate image using Replicate API, with comic style and dialogue instructions
        """
        try:
            # Use SDXL model for high-quality comic-style images
            full_prompt = f"comic book style, {prompt}, high quality, detailed illustration, speech bubble with dialogue: '{dialogue}'"
            output = self.replicate_client.run(
                "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
                input={
                    "prompt": full_prompt,
                    "negative_prompt": "watermark, blurry, low quality",
                    "width": 1024,
                    "height": 1024,
                    "num_outputs": 1,
                    "guidance_scale": 7.5,
                    "num_inference_steps": 30
                }
            )
            if output and len(output) > 0:
                image_url = output[0]
                image_path = await self._download_and_save_image(image_url, output_dir, panel_number)
                if dialogue:
                    self.overlay_speech_bubble(image_path, dialogue)
                return image_path
            else:
                raise Exception("No output received from Replicate")
        except Exception as e:
            logger.error(f"Error generating with Replicate: {str(e)}")
            raise
    
    async def _generate_with_openai(self, prompt: str, output_dir: str, panel_number: int) -> str:
        """
        Generate image using OpenAI DALL-E API
        """
        try:
            import openai
            
            client = openai.OpenAI(api_key=self.openai_api_key)
            
            response = client.images.generate(
                model="dall-e-3",
                prompt=f"Comic book style illustration: {prompt}. High quality, detailed, no text or speech bubbles.",
                size="1024x1024",
                quality="standard",
                n=1,
            )
            
            if response.data and len(response.data) > 0:
                image_url = response.data[0].url
                return await self._download_and_save_image(image_url, output_dir, panel_number)
            else:
                raise Exception("No output received from OpenAI")
                
        except Exception as e:
            logger.error(f"Error generating with OpenAI: {str(e)}")
            raise
    
    async def _generate_with_huggingface(self, prompt: str, output_dir: str, panel_number: int) -> str:
        """
        Generate image using Hugging Face Inference API
        """
        try:
            import requests
            
            API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
            headers = {"Authorization": f"Bearer {self.hf_api_key}"}
            
            payload = {
                "inputs": f"comic book style, {prompt}, high quality, detailed illustration",
                "parameters": {
                    "negative_prompt": "speech bubble, caption, subtitle, text, watermark",
                    "width": 1024,
                    "height": 1024,
                    "guidance_scale": 7.5,
                    "num_inference_steps": 30
                }
            }
            
            response = requests.post(API_URL, headers=headers, json=payload)
            
            if response.status_code == 200:
                # Save the image directly from the response
                image_path = os.path.join(output_dir, f"panel_{panel_number:02d}.png")
                with open(image_path, "wb") as f:
                    f.write(response.content)
                return image_path
            else:
                raise Exception(f"Hugging Face API error: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Error generating with Hugging Face: {str(e)}")
            raise
    
    async def _download_and_save_image(self, image_url: str, output_dir: str, panel_number: int) -> str:
        """
        Download image from URL and save to local file
        """
        try:
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            
            image_path = os.path.join(output_dir, f"panel_{panel_number:02d}.png")
            
            with open(image_path, "wb") as f:
                f.write(response.content)
            
            return image_path
            
        except Exception as e:
            logger.error(f"Error downloading image: {str(e)}")
            raise
    
    def _create_placeholder_image(self, output_dir: str, panel_number: int, prompt: str) -> str:
        """
        Create a placeholder image when generation fails
        """
        try:
            # Create a simple placeholder image
            width, height = 1024, 1024
            image = Image.new('RGB', (width, height), color='#f0f0f0')
            
            # Add some text to indicate it's a placeholder
            draw = ImageDraw.Draw(image)
            
            # Try to use a default font, fallback to basic if not available
            try:
                font = ImageFont.truetype("arial.ttf", 40)
            except:
                font = ImageFont.load_default()
            
            # Add panel number
            draw.text((width//2, height//2 - 50), f"Panel {panel_number}", 
                     fill='#333333', anchor="mm", font=font)
            
            # Add truncated prompt
            truncated_prompt = prompt[:50] + "..." if len(prompt) > 50 else prompt
            draw.text((width//2, height//2 + 50), truncated_prompt, 
                     fill='#666666', anchor="mm", font=font)
            
            image_path = os.path.join(output_dir, f"panel_{panel_number:02d}.png")
            image.save(image_path)
            
            return image_path
            
        except Exception as e:
            logger.error(f"Error creating placeholder image: {str(e)}")
            # Return a path even if creation fails
            return os.path.join(output_dir, f"panel_{panel_number:02d}.png")
    
    def overlay_speech_bubble(self, image_path: str, dialogue: str):
        """
        Overlay a simple speech bubble with dialogue on the image using PIL
        """
        try:
            image = Image.open(image_path)
            draw = ImageDraw.Draw(image)
            width, height = image.size
            # Bubble position and size
            bubble_w, bubble_h = int(width * 0.7), int(height * 0.18)
            bubble_x, bubble_y = int(width * 0.15), int(height * 0.05)
            # Draw bubble
            draw.ellipse([bubble_x, bubble_y, bubble_x + bubble_w, bubble_y + bubble_h], fill=(255,255,255,230), outline=(0,0,0), width=3)
            # Draw text
            try:
                font = ImageFont.truetype("arial.ttf", 36)
            except:
                font = ImageFont.load_default()
            text_x = bubble_x + 20
            text_y = bubble_y + bubble_h//3
            draw.text((text_x, text_y), dialogue, fill=(0,0,0), font=font)
            image.save(image_path)
        except Exception as e:
            logger.error(f"Error overlaying speech bubble: {str(e)}") 