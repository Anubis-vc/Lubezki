from pydantic import BaseSettings, validator
from typing import List, Optional
import os

class Settings(BaseSettings):
    API_V1_STR: str = "/api/"
    PROJECT_NAME: str = "Film Composition AI"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # Google Gemini
    GOOGLE_API_KEY: Optional[str] = None
    
    # File upload settings
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: List[str] = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 