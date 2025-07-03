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
    ) -> List[dict]:
        """
        Generate 10 illustration prompts and dialogue using ChatGPT based on user input
        """
        try:
            system_prompt = """You are a creative comic book illustrator and storyteller. \
            Your task is to generate exactly 10 detailed illustration prompts for a comic book.\n\n            For each panel, provide:\n            - 'description': a vivid, visual prompt for AI image generation (1-2 sentences)\n            - 'dialogue': a short line of character dialogue or speech bubble (1 sentence, in quotes)\n\n            Return ONLY a JSON array of 10 objects, each with 'description' and 'dialogue'.\n            Example format: [\n              {\"description\": \"A robot detective in a space station...\", \"dialogue\": \"We have a problem!\"},\n              ...\n            ]\n            No other text.\n            """
            user_prompt = f"""Create 10 comic panels for:\n            Genre: {genre}\n            Setting: {setting}\n            Characters: {characters}\n\n            Each panel should progress the story.\n            """
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.8,
                max_tokens=1500
            )
            content = response.choices[0].message.content.strip()
            # Try to parse as JSON
            try:
                prompts = json.loads(content)
                if isinstance(prompts, list) and len(prompts) == 10 and all('description' in p and 'dialogue' in p for p in prompts):
                    logger.info(f"Successfully generated {len(prompts)} prompts with dialogue")
                    return prompts
                else:
                    raise ValueError("Response is not a list of 10 objects with description and dialogue")
            except json.JSONDecodeError:
                raise ValueError("Could not parse ChatGPT response as JSON")
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