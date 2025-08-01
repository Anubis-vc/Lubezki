import os
from typing import Dict, Any, Optional
from google import genai
from PIL import Image
import io
from app.core.config import settings

class GeminiService:
    def __init__(self):
        if not settings.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY environment variable is required")
        
        self.client = genai.Client(api_key=settings.GOOGLE_API_KEY)
    
    def analyze_image(self, image_path: str, prompt: str = None) -> Dict[str, Any]:
        """
        Analyze an image using Google Gemini API
        """
        if not prompt:
            prompt = """
            Analyze this film composition and provide detailed feedback on:
            1. Cinematography techniques used
            2. Lighting setup and mood
            3. Framing and composition
            4. Color palette and visual style
            5. Overall visual storytelling effectiveness
            
            Please provide a structured response with specific observations and suggestions for improvement.
            Rate the overall composition on a scale of 1-10.
            """
        
        try:
            # Resize image for API requirements
            resized_image = self._resize_image_for_api(image_path)
            
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[
                    prompt,
                    resized_image,
                ],
            )
            
            return {
                "success": True,
                "response_text": response.text,
                "model_used": "gemini-2.0-flash",
                "prompt_used": prompt
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "model_used": "gemini-2.0-flash",
                "prompt_used": prompt
            }
    
    def _resize_image_for_api(self, image_path: str, max_size: int = 384) -> Image.Image:
        """ Resize image to meet API requirements """
        image = Image.open(image_path)
        width, height = image.size
        
        if width > max_size or height > max_size:
            # Maintain aspect ratio
            image.thumbnail((max_size, max_size))
        
        return image 