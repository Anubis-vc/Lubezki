from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.image import ImageInTable
from app.models.model_definitions import Images
import logging

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
