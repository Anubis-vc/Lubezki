import logging
from fastapi import APIRouter, HTTPException, status, Form
import uuid
from datetime import datetime

from app.api.deps import SessionDep
from app.schemas.image import (
    ImageResponse,
    ImageListResponse,
    ImageCreateURLResponse,
    ImageAnalysisUpdate,
    ImageUploadUpdate,
    ImageDeleteResponse,
    ImageCreate,
)

# from app.services.gemini_service import GeminiService
from app.data_operations import (
    get_upload_url,
    create_image,
    get_image_by_id,
    get_images_for_user,
    update_image_analysis_db,
    update_image_upload_db,
    delete_image_db,
    delete_image_s3,
    get_single_image_url,
    get_image_urls_bulk,
)
from app.core.config import settings

router = APIRouter(prefix="/images")
logger = logging.getLogger(__name__)
# gemini_service = GeminiService()

# TODO: make sure user is authenticated and authorized for all these  operations


########## GET REQUESTS ##########
@router.get("/{image_id}", response_model=ImageResponse)
async def get_download_url(image_id: int, db: SessionDep):
    """Get a presigned URL to view the image and get its metadata"""
    logger.info(f"Fetching download URL for image {image_id}")

    try:
        db_image = await get_image_by_id(db, image_id)
        image_info = await get_image_by_id(db, image_id)
        if not db_image or not image_info:
            logger.warning(f"Image {image_id} not found")
            raise HTTPException(status_code=404, detail="Image not found")

        download_url = await get_single_image_url(db_image.storage_path)

        if not download_url:
            logger.error(f"Failed to generate download URL for image {image_id}")
            raise HTTPException(
                status_code=500, detail="Failed to generate download URL"
            )

        logger.info(f"Successfully generated download URL for image {image_id}")
        return {
            "original_name": image_info.original_name,
            "size_bytes": image_info.size_bytes,
            "mime_type": image_info.mime_type,
            "width_px": image_info.width_px,
            "height_px": image_info.height_px,
            "is_analysis_complete": image_info.is_analysis_complete,
            "score": image_info.score,
            "analysis": image_info.analysis,
            "download_url": download_url,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Unexpected error fetching download URL for image {image_id}: {e}",
            exc_info=True,
        )
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/gallery/{user_id}", response_model=ImageListResponse)
async def get_gallery(
    user_id: uuid.UUID, db: SessionDep, cursor: datetime | None = None
):
    """Get a users gallery of images with pagination"""
    logger.info(f"Fetching gallery for user {user_id}, cursor: {cursor}")

    try:
        images, total, cursor = await get_images_for_user(db, user_id, cursor)
        urls = []
        if total > 0:
            urls = await get_image_urls_bulk(images)

        logger.info(
            f"Successfully retrieved gallery for user {user_id}: {total} images"
        )
        return {"images": images, "urls": urls, "total": total, "cursor": cursor}
    except Exception as e:
        logger.error(f"Error fetching gallery for user {user_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


########## POST REQUESTS ##########
# TODO: edit this to not take in the image, we'll send it to s3 directly
# TODO: check the file type with magic bytes on the backend
# TODO: better to bring from body instead of form since we're not sending a file
@router.post(
    "/", response_model=ImageCreateURLResponse, status_code=status.HTTP_201_CREATED
)
async def create_image_record(
    db: SessionDep,
    user_id: uuid.UUID = Form(...),
    filename: str = Form(...),
    file_type: str = Form(...),
    file_size: int = Form(...),
    width: int = Form(...),
    height: int = Form(...),
):
    """Create a database record after successful S3 upload"""
    logger.info(f"Creating image record for user {user_id}, file: {filename}")

    try:
        presigned_url, key = await get_upload_url(filename)

        data = ImageCreate(
            user_id=user_id,
            created_at=datetime.now(),
            original_name=filename,
            bucket=settings.AWS_BUCKET_NAME,
            storage_path=key,
            size_bytes=file_size,
            mime_type=file_type,
            width_px=width,
            height_px=height,
            updated_at=datetime.now(),
            is_analysis_complete=False,
            score=None,
            analysis=None,
            status="uploading",
        )

        if await create_image(db, data):
            logger.info(
                f"Successfully created image record for user {user_id}, key: {key}"
            )
            return {
                "presigned_url": presigned_url,
                "message": "image record created, pending upload",
            }
        else:
            logger.error(f"Failed to create image record for user {user_id}")
            raise HTTPException(status_code=500, detail="Failed to create image record")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Unexpected error creating image record for user {user_id}: {e}",
            exc_info=True,
        )
        raise HTTPException(status_code=500, detail="Internal server error")


########## PATCH REQUESTS ##########
# TODO: add listener for s3 events to update the image record with status
@router.patch("/update/analysis/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_image_analysis(
    image_id: int, analysis: ImageAnalysisUpdate, db: SessionDep
):
    """Update the analysis of an image"""
    logger.info(f"Updating analysis for image {image_id}")

    try:
        if await update_image_analysis_db(db, image_id, analysis):
            logger.info(f"Successfully updated analysis for image {image_id}")
            return
        else:
            logger.error(f"Failed to update analysis for image {image_id}")
            raise HTTPException(
                status_code=500, detail="Failed to update image analysis"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Unexpected error updating analysis for image {image_id}: {e}",
            exc_info=True,
        )
        raise HTTPException(status_code=500, detail="Internal server error")


@router.patch("/update/upload/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_image_upload(image_id: int, upload: ImageUploadUpdate, db: SessionDep):
    """Update the upload status of an image"""
    logger.info(f"Updating upload status for image {image_id} to {upload.status}")

    try:
        if await update_image_upload_db(db, image_id, upload):
            logger.info(f"Successfully updated upload status for image {image_id}")
            return
        else:
            logger.error(f"Failed to update upload status for image {image_id}")
            raise HTTPException(status_code=500, detail="Failed to update image upload")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Unexpected error updating upload status for image {image_id}: {e}",
            exc_info=True,
        )
        raise HTTPException(status_code=500, detail="Internal server error")


########## DELETE REQUESTS ##########
@router.delete("/{image_id}", response_model=ImageDeleteResponse)
async def delete_image_endpoint(image_id: int, db: SessionDep):
    """Delete an image from both database and S3"""
    logger.info(f"Deleting image {image_id}")

    try:
        db_image = await get_image_by_id(db, image_id)
        if not db_image:
            logger.warning(f"Image {image_id} not found for deletion")
            raise HTTPException(status_code=404, detail="Image not found")

        s3_deleted = await delete_image_s3(db_image.storage_path)
        db_deleted = await delete_image_db(db, image_id)

        if not db_deleted:
            logger.error(f"Failed to delete image {image_id} from database")
            raise HTTPException(
                status_code=500, detail="Failed to delete from database"
            )

        logger.info(
            f"Successfully deleted image {image_id}, S3: {s3_deleted}, DB: {db_deleted}"
        )
        return {
            "message": "Image deleted successfully",
            "s3_deleted": s3_deleted,
            "db_deleted": db_deleted,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error deleting image {image_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Delete failed: {str(e)}")
