from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile
from fastapi.exceptions import HTTPException
from sqlalchemy import select, func
from typing import Sequence
import uuid

from app.models.model_definitions import Images
from app.schemas.image import ImageCreate, ImageUpdate


# TODO: upload file to bucket
async def save_uploaded_file(
    file: UploadFile, upload_dir: str = "uploads"
) -> tuple[str, str]:
    print("need to implement, find bucket info first")
    return ("", "")


# Database operations
async def create_image(session: AsyncSession, image_data: ImageCreate) -> Images:
    """Create a new image record"""
    db_image = Images(**image_data.model_dump())
    session.add(db_image)
    await session.commit()
    await session.refresh(db_image)
    return db_image


async def get_image_by_id(session: AsyncSession, image_id: int) -> Images | None:
    """Get image by ID"""
    return await session.get(Images, image_id)


# TODO: two, queries, possible to do in one?
async def get_images_for_user(
    session: AsyncSession, user_id: uuid.UUID, limit: int = 100, offset: int = 0
) -> tuple[Sequence[Images], int, int, int]:
    """Get images with pagination"""
    total_stmt = (
        select(func.count()).select_from(Images).where(Images.user_id == user_id)
    )
    total = await session.scalar(total_stmt) or 0

    if total == 0:
        raise HTTPException(status_code=404, detail="No images found for user")

    # get results
    data_stmt = (
        select(Images)
        .where(Images.user_id == user_id)
        .order_by(Images.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    images = (await session.scalars(data_stmt)).all()

    return images, total, limit, offset


async def update_image_analysis(
    session: AsyncSession, image_id: int, image_update: ImageUpdate
) -> Images | None:
    """Update image with analysis results"""
    # Get the image first
    image = await get_image_by_id(session, image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    # Update fields
    image.analysis = image_update.analysis
    image.score = image_update.score
    image.is_analysis_complete = image_update.is_analysis_complete

    await session.commit()
    await session.refresh(image)
    return image


async def delete_image(session: AsyncSession, image_id: int) -> bool:
    """Delete image by ID"""
    image = await get_image_by_id(session, image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    # Delete from database
    await session.delete(image)
    await session.commit()
    return True


# # Utility functions for API responses
# def image_to_response(image: Images) -> ImageResponse:
#     """Convert database Images to API response"""
#     return ImageResponse(
#         user_id=image.user_id,
#         file_path=f"uploads/{image.image_id}",  # Placeholder path
#         mime_type=image.mime_type,
#         is_analysis_complete=image.is_analysis_complete or False,
#         score=image.score,
#         analysis=image.analysis or ""
#     )


# def create_image_list_response(
#     images: list[Images],
#     total: int,
#     limit: int,
#     offset: int
# ) -> ImageListResponse:
#     """Create paginated image list response"""
#     return ImageListResponse(
#         images=[image_to_response(img) for img in images],
#         total=total,
#         limit=limit,
#         offset=offset
#     )
