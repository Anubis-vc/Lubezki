from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.api import api_router
from app.core.config import settings
from app.core.database import create_db_and_tables, engine

app = FastAPI(
    title="Lubezki API",
    description="AI-powered film composition analysis using Google Gemini",
    version="1.0.0",
    openapi_url=f"{settings.API_STR}/openapi.json"
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


@app.on_event("startup")
async def startup_event():
    """Initialize database tables on startup"""
    await create_db_and_tables()


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up database connections on shutdown"""
    await engine.dispose()


@app.get("/")
async def root():
    return {"message": "Film Composition AI API is running!"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"} 