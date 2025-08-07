from pydantic_settings import BaseSettings
from pydantic import PostgresDsn
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    API_STR: str = "/api/v1/"
    PROJECT_NAME: str = "Lubezki"

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:8000"]

    # Database
    DB_CXN_STRING: PostgresDsn | None = None

    # Google Gemini
    GEMINI_API_KEY: str | None = None

    # File upload settings
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 20 * 1024 * 1024  # 20MB
    ALLOWED_EXTENSIONS: list[str] = [".jpg", ".jpeg", ".png", ".raw"]


settings = Settings()
