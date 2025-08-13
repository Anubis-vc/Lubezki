import os
from PIL import Image
from app.services.gemini_service import GeminiService

gemini_service = GeminiService()

print(gemini_service.analyze_image("/Users/anubis/Desktop/Personal_Projects/film-composition-ai/assets/amelie_still.jpg"))