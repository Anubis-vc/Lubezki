from typing import Dict, Any
from PIL import Image
from google import genai
from google.genai import types
import json

from app.core.config import settings
from app.services.prompt import prompt


class GeminiService:
    def __init__(self):
        if not settings.GEMINI_API_KEY:
            raise ValueError("Gemini API key environment variable is required")

        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model = "gemini-2.0-flash"

    def analyze_image(self, image_path: str) -> Dict[str, Any]:
        """Analyze an image using Google Gemini API: later will use a local model"""
        
        # Resize image for API requirements
        resized_image = self._resize_image(image_path)
        config = types.GenerateContentConfig(response_mime_type="application/json")

        response = self.client.models.generate_content(
            model=self.model,
            contents=[prompt, resized_image],
            config=config
        )

        return json.loads(response.text)


    def _resize_image(
        self, image_path: str, max_size: int = 384
    ) -> Image.Image:
        """Resize image to meet API requirements"""
        
        # TODO: download image first because url too long
        # this resizer will need to get the raw bytes of the image
        image = Image.open(image_path)
        width, height = image.size

        if width > max_size or height > max_size:
            # Maintain aspect ratio
            image.thumbnail((max_size, max_size))

        return image
