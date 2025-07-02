import os
import json
import logging
from typing import List
import openai
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class ChatGPTService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        self.client = openai.OpenAI(api_key=self.api_key)
    
    async def generate_illustration_prompts(
        self, 
        genre: str, 
        setting: str, 
        characters: str
    ) -> List[str]:
        """
        Generate 10 illustration prompts using ChatGPT based on user input
        """
        try:
            system_prompt = """You are a creative comic book illustrator and storyteller. 
            Your task is to generate exactly 10 detailed illustration prompts for a comic book.
            
            Each prompt should be:
            - Descriptive and vivid
            - Suitable for AI image generation
            - Tell a story progression
            - Include visual details like lighting, composition, character poses
            - Be 1-2 sentences long
            - Focus on visual storytelling
            
            Return ONLY a JSON array of 10 strings, no other text.
            Example format: ["prompt 1", "prompt 2", ..., "prompt 10"]"""
            
            user_prompt = f"""Create 10 illustration prompts for a comic book with:
            Genre: {genre}
            Setting: {setting}
            Characters: {characters}
            
            The prompts should tell a complete story arc from beginning to end.
            Make sure each prompt is visually distinct and progresses the narrative."""
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.8,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content.strip()
            
            # Try to parse as JSON
            try:
                prompts = json.loads(content)
                if isinstance(prompts, list) and len(prompts) == 10:
                    logger.info(f"Successfully generated {len(prompts)} prompts")
                    return prompts
                else:
                    raise ValueError("Response is not a list of 10 prompts")
            except json.JSONDecodeError:
                # If JSON parsing fails, try to extract prompts from text
                prompts = self._extract_prompts_from_text(content)
                if len(prompts) == 10:
                    return prompts
                else:
                    raise ValueError(f"Could not extract exactly 10 prompts from response")
                    
        except Exception as e:
            logger.error(f"Error generating prompts: {str(e)}")
            raise
    
    def _extract_prompts_from_text(self, text: str) -> List[str]:
        """
        Fallback method to extract prompts from text if JSON parsing fails
        """
        lines = text.split('\n')
        prompts = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('```'):
                # Remove numbering if present
                if line[0].isdigit() and '. ' in line:
                    line = line.split('. ', 1)[1]
                prompts.append(line)
        
        # Ensure we have exactly 10 prompts
        if len(prompts) > 10:
            prompts = prompts[:10]
        elif len(prompts) < 10:
            # Pad with generic prompts if we don't have enough
            while len(prompts) < 10:
                prompts.append(f"Comic panel {len(prompts) + 1}")
        
        return prompts 