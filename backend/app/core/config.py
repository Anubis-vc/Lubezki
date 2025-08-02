from pydantic_settings import BaseSettings
from typing import List
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    API_STR: str = "/api/"
    PROJECT_NAME: str = "Film Composition AI"

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    # Supabase
    SUPABASE_URL: str | None = None
    SUPABASE_KEY: str | None = None

    # Google Gemini
    GEMINI_API_KEY: str | None = None

    # File upload settings
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: List[str] = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
