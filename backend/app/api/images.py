from fastapi import APIRouter, HTTPException, status
import uuid
from datetime import datetime
from fastapi import UploadFile

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

router = APIRouter(prefix="/image")
# gemini_service = GeminiService()

# TODO: make sure user is authenticated and authorized for all these  operations


########## GET REQUESTS ##########
@router.get("/{image_id}/", response_model=ImageResponse)
async def get_download_url(image_id: int, db: SessionDep):
    """Get a presigned URL to view the image and get its metadata"""

    db_image = await get_image_by_id(db, image_id)
    image_info = await get_image_by_id(db, image_id)
    if not db_image or not image_info:
        raise HTTPException(status_code=404, detail="Image not found")

    download_url = await get_single_image_url(db_image.storage_path)

    if not download_url:
        raise HTTPException(status_code=500, detail="Failed to generate download URL")

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


@router.get("/gallery/{user_id}/", response_model=ImageListResponse)
async def get_gallery(db: SessionDep, user_id: uuid.UUID, cursor: datetime | None):
    """Get a users gallery of images with pagination"""

    images, total, cursor = await get_images_for_user(db, user_id, cursor)
    urls = []
    if total > 0:
        urls = await get_image_urls_bulk(images)
    return {"images": images, "urls": urls, "total": total, "cursor": cursor}


########## POST REQUESTS ##########
# TODO: make sure that the client is sending the height and width
@router.post(
    "/", response_model=ImageCreateURLResponse, status_code=status.HTTP_201_CREATED
)
async def create_image_record(
    db: SessionDep, user_id: uuid.UUID, file: UploadFile, width: int, height: int
):
    """Create a database record after successful S3 upload"""

    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    if not file.size or file.size > settings.MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size is invalid")

    presigned_url, key = await get_upload_url(
        file.filename if file.filename else "unknown"
    )
    if not presigned_url or not key:
        raise HTTPException(status_code=500, detail="Failed to generate upload URL")

    data = ImageCreate(
        user_id=user_id,
        created_at=datetime.now(),
        original_name=file.filename,
        bucket=settings.AWS_BUCKET_NAME,
        storage_path=key,
        size_bytes=file.size,
        mime_type=file.content_type,
        width_px=width,
        height_px=height,
        updated_at=datetime.now(),
        is_analysis_complete=False,
        score=None,
        analysis=None,
        status="uploading",
    )

    if await create_image(db, data):
        return {
            "presigned_url": presigned_url,
            "message": "image record created, pending upload",
        }
    else:
        raise HTTPException(status_code=500, detail="Failed to create image record")


########## PATCH REQUESTS ##########
# TODO: add listener for s3 events to update the image record with status
@router.patch("/update/analysis/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_image_analysis(
    db: SessionDep, image_id: int, analysis: ImageAnalysisUpdate
):
    """Update the analysis of an image"""

    if await update_image_analysis_db(db, image_id, analysis):
        return
    else:
        raise HTTPException(status_code=500, detail="Failed to update image analysis")


@router.patch("/update/upload/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_image_upload(db: SessionDep, image_id: int, upload: ImageUploadUpdate):
    """Update the upload status of an image"""

    if await update_image_upload_db(db, image_id, upload):
        return
    else:
        raise HTTPException(status_code=500, detail="Failed to update image upload")


########## DELETE REQUESTS ##########
@router.delete("/{image_id}", response_model=ImageDeleteResponse)
async def delete_image_endpoint(image_id: int, db: SessionDep):
    """Delete an image from both database and S3"""

    db_image = await get_image_by_id(db, image_id)
    if not db_image:
        raise HTTPException(status_code=404, detail="Image not found")

    try:
        s3_deleted = await delete_image_s3(db_image.storage_path)
        db_deleted = await delete_image_db(db, image_id)

        if not db_deleted:
            raise HTTPException(
                status_code=500, detail="Failed to delete from database"
            )

        return {
            "message": "Image deleted successfully",
            "s3_deleted": s3_deleted,
            "db_deleted": db_deleted,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Delete failed: {str(e)}")
