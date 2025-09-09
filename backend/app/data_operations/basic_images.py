from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import logging

from app.schemas.image import ImageInTable
from app.models.model_definitions import Images

logger = logging.getLogger(__name__)


async def create_image(
    session: AsyncSession, image_data: ImageInTable
) -> Images | None:
    """Create a new image record"""
    logger.info(f"Creating new image for user {image_data.user_id}")

    db_image = Images(**image_data.model_dump())
    session.add(db_image)
    await session.commit()
    await session.refresh(db_image)
    logger.info(f"Successfully created image with ID: {db_image.image_id}")
    return db_image


async def get_images(session: AsyncSession) -> Sequence[Images]:
    """Get all images from the database"""
    logger.info("Getting all gallery images from the database")

    result = await session.scalars(select(Images))
    return result.all()


async def get_image_by_id(session: AsyncSession, image_id: str) -> Images | None:
    """Get an image by its ID"""
    logger.info(f"Getting image with ID: {image_id}")
    result = await session.get(Images, image_id)
    return result
