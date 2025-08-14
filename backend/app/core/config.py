from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    API_STR: str = "/api/v1"
    PROJECT_NAME: str = "Lubezki"

    # TODO: make this good
    # CORS
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8000",
    ]

    # Database
    DB_CXN_STRING: str = "missing"

    # Google Gemini
    GEMINI_API_KEY: str | None = None

    # File upload settings
    MAX_FILE_SIZE: int = 20 * 1024 * 1024  # 20MB
    ALLOWED_EXTENSIONS: list[str] = [".jpg", ".jpeg", ".png", ".raw"]

    env: str = "dev"
    echo_sql: bool = False
    log_level: str = "DEBUG"  # TODO: change to INFO in production

    AWS_BUCKET_NAME: str = "dev"
    AWS_BASIC_BUCKET_NAME: str = "public-lubezki-images"

    PUBLIC_AUTH_KEY: str = "missing"
    
    DEFAULT_USER_ID: str = "70321201-896d-4ff5-b5c1-61296c3775ba"

    def model_post_init(self, __context):
        self.echo_sql = self.env == "dev"


settings = Settings()
