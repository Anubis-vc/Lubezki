from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.image import Image, ImageCreate, ImageUpdate, ImageResponse, ImageListResponse
from fastapi import UploadFile
import os
import shutil
from pathlib import Path


# TODO: upload file to bucket
async def save_uploaded_file(file: UploadFile, upload_dir: str = "uploads") -> tuple[str, str]:
    print("need to implement, find bucket info first")


# Database operations
async def create_image(db: AsyncSession, image_data: ImageCreate) -> Image:
    """Create a new image record"""
    db_image = Image(**image_data.model_dump())
    db.add(db_image)
    await db.commit()
    await db.refresh(db_image)
    return db_image


async def get_image_by_id(db: AsyncSession, image_id: str) -> Optional[Image]:
    """Get image by ID"""
    result = await db.execute(select(Image).where(Image.id == image_id))
    return result.scalar_one_or_none()


async def get_images(
    db: AsyncSession, 
    user_id: Optional[int] = None,
    limit: int = 100, 
    offset: int = 0
) -> tuple[List[Image], int]:
    """Get images with optional filtering and pagination"""
    # Build query
    query = select(Image)
    if user_id is not None:
        query = query.where(Image.user_id == user_id)
    
    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # Get paginated results
    query = query.order_by(Image.uploaded_at.desc()).offset(offset).limit(limit)
    result = await db.execute(query)
    images = result.scalars().all()
    
    return list(images), total


async def update_image_analysis(
    db: AsyncSession, 
    image_id: str, 
    gemini_response: str, 
    analysis_summary: str, 
    composition_score: int
) -> Optional[Image]:
    """Update image with analysis results"""
    # Get the image first
    image = await get_image_by_id(db, image_id)
    if not image:
        return None
    
    # Update fields
    image.gemini_response = gemini_response
    image.analysis_summary = analysis_summary
    image.composition_score = composition_score
    image.is_analysis_complete = True
    
    await db.commit()
    await db.refresh(image)
    return image


async def update_image(
    db: AsyncSession, 
    image_id: str, 
    image_update: ImageUpdate
) -> Optional[Image]:
    """Update image with partial data"""
    # Get the image first
    image = await get_image_by_id(db, image_id)
    if not image:
        return None
    
    # Update only provided fields
    update_data = image_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(image, field, value)
    
    await db.commit()
    await db.refresh(image)
    return image


async def delete_image(db: AsyncSession, image_id: str) -> bool:
    """Delete image by ID"""
    image = await get_image_by_id(db, image_id)
    if not image:
        return False
    
    # Delete the file from disk if it exists
    if os.path.exists(image.file_path):
        os.remove(image.file_path)
    
    # Delete from database
    await db.delete(image)
    await db.commit()
    return True


async def get_user_images(
    db: AsyncSession, 
    user_id: int, 
    limit: int = 100, 
    offset: int = 0
) -> tuple[List[Image], int]:
    """Get images for a specific user"""
    return await get_images(db, user_id=user_id, limit=limit, offset=offset)


# Utility functions for API responses
def image_to_response(image: Image) -> ImageResponse:
    """Convert database Image to API response"""
    return ImageResponse(
        id=image.id,
        user_id=image.user_id,
        filename=image.filename,
        original_filename=image.original_filename,
        file_path=image.file_path,
        file_size=image.file_size,
        mime_type=image.mime_type,
        uploaded_at=image.uploaded_at,
        is_analysis_complete=image.is_analysis_complete,
        composition_score=image.composition_score,
        gemini_response=image.gemini_response,
        analysis_summary=image.analysis_summary
    )


def create_image_list_response(
    images: List[Image], 
    total: int, 
    limit: int, 
    offset: int
) -> ImageListResponse:
    """Create paginated image list response"""
    return ImageListResponse(
        images=[image_to_response(img) for img in images],
        total=total,
        limit=limit,
        offset=offset
    ) 