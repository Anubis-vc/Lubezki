import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Sequence
import uuid
from datetime import datetime

from app.models.model_definitions import Images
from app.schemas.image import ImageCreate, ImageAnalysisUpdate, ImageUploadUpdate

logger = logging.getLogger(__name__)


async def get_image_by_id(session: AsyncSession, image_id: int) -> Images | None:
    """Get image by ID"""
    logger.debug(f"Fetching image with ID: {image_id}")
    return await session.get(Images, image_id)


async def get_images_for_user(
    session: AsyncSession,
    user_id: uuid.UUID,
    cursor: datetime | None = None,
    limit: int = 50,
) -> tuple[Sequence[Images], int, datetime]:
    """Get images with pagination"""
    logger.debug(
        f"Fetching images for user {user_id}, limit: {limit}, cursor: {cursor}"
    )

    data_stmt = (
        select(Images)
        .where(Images.user_id == user_id)
        .order_by(Images.created_at.desc())
    )
    if cursor:
        data_stmt = data_stmt.where(Images.created_at < cursor)
    data_stmt = data_stmt.limit(limit)

    images = (await session.scalars(data_stmt)).all()
    count = len(images)

    if images:
        last_cursor = images[-1].created_at
        logger.info(f"Retrieved {count} images for user {user_id}")
        return images, count, last_cursor
    else:
        logger.info(f"No images found for user {user_id}")
        return images, 0, datetime.now()


async def create_image(session: AsyncSession, image_data: ImageCreate) -> Images | None:
    """Create a new image record"""
    logger.info(f"Creating new image for user {image_data.user_id}")

    db_image = Images(**image_data.model_dump())
    session.add(db_image)
    await session.commit()
    await session.refresh(db_image)
    logger.info(f"Successfully created image with ID: {db_image.image_id}")
    return db_image


async def update_image_analysis(
    session: AsyncSession, image_id: int, image_update: ImageAnalysisUpdate
) -> Images | None:
    """Update image with analysis results"""
    logger.info(f"Updating analysis for image {image_id}")

    image = await get_image_by_id(session, image_id)
    if not image:
        logger.warning(f"Image {image_id} not found for analysis update")
        return None

    image.analysis = image_update.analysis
    image.score = image_update.score
    image.is_analysis_complete = image_update.is_analysis_complete

    await session.commit()
    await session.refresh(image)
    logger.info(f"Successfully updated analysis for image {image_id}")
    return image


async def update_image_upload(
    session: AsyncSession, image_id: int, image_update: ImageUploadUpdate
) -> Images | None:
    """Update image with upload status"""
    logger.info(f"Updating upload status for image {image_id} to {image_update.status}")

    image = await get_image_by_id(session, image_id)
    if not image:
        logger.warning(f"Image {image_id} not found for upload update")
        return None

    image.status = image_update.status
    await session.commit()
    await session.refresh(image)
    logger.info(f"Successfully updated upload status for image {image_id}")
    return image


async def delete_image(session: AsyncSession, image_id: int) -> bool:
    """Delete image by ID"""
    logger.info(f"Deleting image {image_id}")

    image = await get_image_by_id(session, image_id)
    if not image:
        logger.warning(f"Image {image_id} not found for deletion")
        return False

    await session.delete(image)
    await session.commit()
    logger.info(f"Successfully deleted image {image_id}")
    return True
