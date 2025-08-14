from fastapi import APIRouter, BackgroundTasks, HTTPException, UploadFile, status
import logging
from typing import Any
# TODO: maybe import asyncio to run the blocking gemini service in a thread

from app.services.gemini_service import GeminiService
from app.data_operations.basic_bucket import get_gallery_urls, upload_file, get_single_image_url

router = APIRouter(prefix='/basic')
logger = logging.getLogger(__name__)
gemini_service = GeminiService()


@router.get("/")
async def get_basic_info() -> dict[str, Any]:
    logger.info(f"Fetching basic gallery for default user")

    try:
        urls = await get_gallery_urls()

        logger.info(f"Successfully retrieved default gallery for user")
        return {"urls":urls, "total": len(urls)}
    except Exception as e:
        logger.error(f"Error fetching default gallery: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
    

@router.post("/upload")
async def upload_image(file: UploadFile) -> dict[str, Any]:
    if file.content_type != "image/jpeg":
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    if file.size > 25 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large")
    
    try:
        # key = await upload_file(file)
        # url = await get_single_image_url(key)
        
        analysis = gemini_service.analyze_image(file.file.read())
        return {"analysis": analysis}
    except Exception as e:
        logger.error(f"Error uploading file: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
    