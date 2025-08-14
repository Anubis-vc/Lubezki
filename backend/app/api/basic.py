from fastapi import APIRouter, HTTPException, UploadFile
import logging
from typing import Any
from PIL import Image
import io
import uuid
from datetime import datetime
# TODO: maybe import asyncio to run the blocking gemini service in a thread

from app.services.gemini_service import GeminiService
from app.data_operations.basic_bucket import get_gallery_urls, upload_file
from app.data_operations.basic_images import create_image
from app.core.config import settings
from app.schemas.image import ImageInTable
from app.data_operations.items import create_item
from app.schemas.item import ItemCreate, BoundingBox
from app.api.deps import SessionDep

router = APIRouter(prefix="/basic")
logger = logging.getLogger(__name__)
gemini_service = GeminiService()


@router.get("/")
async def get_basic_info() -> dict[str, Any]:
    logger.info("Fetching basic gallery for default user")

    try:
        urls = await get_gallery_urls()

        logger.info("Successfully retrieved default gallery for user")
        return {"urls": urls, "total": len(urls)}
    except Exception as e:
        logger.error(f"Error fetching default gallery: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/upload")
async def upload_image(file: UploadFile) -> dict[str, Any]:
    if file.content_type and file.content_type != "image/jpeg":
        raise HTTPException(status_code=400, detail="Invalid file type")

    if file.size and file.size > 25 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large")

    try:
        # key = await upload_file(file)
        # url = await get_single_image_url(key)

        analysis = gemini_service.analyze_image(file.file.read())
        return {"analysis": analysis}
    except Exception as e:
        logger.error(f"Error uploading file: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/upload-for-gallery")
async def upload_for_gallery(file: UploadFile, db: SessionDep) -> dict[str, str]:
    if file.content_type and file.content_type != "image/jpeg":
        raise HTTPException(status_code=400, detail="Invalid file type")

    if file.size and file.size > 25 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large")

    try:
        pil_image = Image.open(io.BytesIO(file.file.read()))
        width, height = pil_image.size  # get original before thumbnailing later
        thumbnail_image = pil_image.resize((500, 500))

        # upload the files to s3
        key = await upload_file(pil_image)
        thumbnail_key = await upload_file(thumbnail_image)

        gemini_response = gemini_service.analyze_image(pil_image)
        image_id = uuid.uuid4()

        # add image to db
        image_data = ImageInTable(
            image_id=image_id,
            user_id=uuid.UUID(settings.DEFAULT_USER_ID),
            original_name=file.filename if file.filename else "unknown",
            bucket=settings.AWS_BASIC_BUCKET_NAME,
            storage_key=key,
            thumbnail_key=thumbnail_key,
            size_bytes=file.size,
            mime_type=file.content_type if file.content_type else "image/*",
            width_px=width,
            height_px=height,
            analysis=gemini_response["analysis"],
            created_at=datetime.now(),
            updated_at=datetime.now(),
            is_analysis_complete=True,
            score=gemini_response["scores"],
            status="complete",
        )
        db_response = await create_image(db, image_data)
        if not db_response:
            raise HTTPException(status_code=500, detail="Failed to create image")

        # add item to db
        for item in gemini_response["objects"]:
            item_data = ItemCreate(
                image_id=image_id,
                name=item["name"],
                bounding_box=BoundingBox(
                    center_x=item["bounding_box"]["x"],
                    center_y=item["bounding_box"]["y"],
                    height=item["bounding_box"]["width"],
                    width=item["bounding_box"]["height"],
                ),
                analysis=item["analysis"],
                created_at=datetime.now(),
            )
            await create_item(db, item_data)

        return {"message": "Image uploaded successfully"}

    except Exception as e:
        logger.error(f"Error uploading file: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


# TODO: Make a script that can do this for every file in the directory and populate gallery
