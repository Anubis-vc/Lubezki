from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from contextlib import asynccontextmanager
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.api import api_router
from app.core.config import settings
from app.core.database_async import session_manager
from app.core.logging_config import setup_logging


# Set up logging based on environment

setup_logging(log_level="INFO")

logger = logging.getLogger(__name__)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        if await session_manager.health_check():
            logger.info("Database connection established")
        else:
            logger.error("Database health check failed")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise

    yield

    try:
        await session_manager.close()
        logger.info("Database connection closed")
    except Exception as e:
        logger.error(f"Error closing database connection: {e}")


app = FastAPI(
    title="Lubezki API",
    description="AI-powered film composition analysis using Google Gemini",
    version="1.0.0",
    openapi_url=f"{settings.API_STR}/openapi.json",
    lifespan=lifespan,
)

# Add rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=[
        "Accept",
        "Accept-Language",
        "Content-Language",
        "Content-Type",
        "Authorization",
        "X-Requested-With",
        "Origin",
        "Access-Control-Request-Method",
        "Access-Control-Request-Headers",
    ],
    expose_headers=["Content-Length", "Content-Range"],
    max_age=86400,  # Cache preflight for 24 hours
)

# Include API router
app.include_router(api_router, prefix=settings.API_STR)


@app.get("/")
async def root():
    return {"message": "Lubezki API is running!"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
