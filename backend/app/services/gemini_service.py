from typing import Dict, Any
from PIL import Image
from google import genai
from google.genai import types
import json
import io
from app.core.config import settings
from app.services.prompt import prompt


class GeminiService:
    def __init__(self):
        if not settings.GEMINI_API_KEY:
            raise ValueError("Gemini API key environment variable is required")

        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model = "gemini-2.0-flash"


    def analyze_image(self, image: bytes | Image.Image) -> Dict[str, Any]:
        """Analyze an image using Google Gemini API: later will use a local model"""

        # Resize image for API requirements
        resized_image = self._resize_image(image)
        config = types.GenerateContentConfig(response_mime_type="application/json")

        response = self.client.models.generate_content(
            model=self.model, contents=[prompt, resized_image], config=config
        )

        return json.loads(response.text)

    def _resize_image(self, image: bytes | Image.Image, max_size: int = 384) -> Image.Image:
        """Resize image to meet API requirements"""

        pil_image: Image.Image
        if isinstance(image, bytes):
            pil_image = Image.open(io.BytesIO(image))
        else:
            pil_image = image

        width, height = pil_image.size

        if width > max_size or height > max_size:
            pil_image.thumbnail((max_size, max_size))  # maintain aspect ratio

        return pil_image
