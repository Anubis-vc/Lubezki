from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException
from sqlalchemy import select, func
from typing import Sequence
import uuid
from datetime import datetime

from app.models.model_definitions import Images
from app.schemas.image import ImageCreate, ImageAnalysisUpdate, ImageUploadUpdate


async def get_image_by_id(session: AsyncSession, image_id: int) -> Images | None:
    """Get image by ID"""
    return await session.get(Images, image_id)


# TODO: two, queries, possible to do in one?
async def get_images_for_user(
    session: AsyncSession,
    user_id: uuid.UUID,
    cursor: datetime | None = None,
    limit: int = 50,
) -> tuple[Sequence[Images], int, datetime]:
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
    )
    if cursor:
        data_stmt = data_stmt.where(Images.created_at < cursor)
    data_stmt = data_stmt.limit(limit)

    images = (await session.scalars(data_stmt)).all()

    if images:
        return images, total, images[-1].created_at
    else:
        return images, total, datetime.now()


async def create_image(session: AsyncSession, image_data: ImageCreate) -> Images:
    """Create a new image record"""
    db_image = Images(**image_data.model_dump())
    session.add(db_image)
    await session.commit()
    await session.refresh(db_image)
    return db_image


async def update_image_analysis(
    session: AsyncSession, image_id: int, image_update: ImageAnalysisUpdate
) -> Images | None:
    """Update image with analysis results"""
    # Get the image first
    image = await get_image_by_id(session, image_id)
    if not image:
        return None

    # Update fields
    image.analysis = image_update.analysis
    image.score = image_update.score
    image.is_analysis_complete = image_update.is_analysis_complete

    await session.commit()
    await session.refresh(image)
    return image


# TODO: may have to add this to a background task to kick off analaysis
async def update_image_upload(
    session: AsyncSession, image_id: int, image_update: ImageUploadUpdate
) -> Images | None:
    """Update image with upload status"""
    image = await get_image_by_id(session, image_id)
    if not image:
        return None

    image.status = image_update.status
    await session.commit()
    await session.refresh(image)
    return image


async def delete_image(session: AsyncSession, image_id: int) -> bool:
    """Delete image by ID"""
    image = await get_image_by_id(session, image_id)
    if not image:
        return False

    # Delete from database
    await session.delete(image)
    await session.commit()
    return True
