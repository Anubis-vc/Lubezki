from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
import logging
from contextlib import asynccontextmanager

from app.api import api_router
from app.core.config import settings
from app.core.database_async import session_manager
from app.core.logging_config import setup_logging


# Set up logging based on environment
if settings.log_level == "DEBUG":
    setup_logging(log_level="DEBUG")
else:
    setup_logging(log_level="INFO")

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Check if database connection exists at startup
    try:
        async with session_manager.session() as session:
            await session.execute(text("SELECT 1"))
        logger.info("Database connection established")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise

    yield

    try:
        await session_manager.close()
        logger.info("Database connections closed")
    except Exception as e:
        logger.error(f"Error closing database connections: {e}")


app = FastAPI(
    title="Lubezki API",
    description="AI-powered film composition analysis using Google Gemini",
    version="1.0.0",
    openapi_url=f"{settings.API_STR}/openapi.json",
    lifespan=lifespan,
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_STR)


@app.get("/")
async def root():
    return {"message": "Lubezki API is running!"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
