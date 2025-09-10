import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Sequence
import uuid

from app.models.model_definitions import Items
from app.schemas.item import ItemCreate

logger = logging.getLogger(__name__)


async def get_item(session: AsyncSession, item_id: uuid.UUID) -> Items | None:
    logger.info(f"Fetching item with ID: {item_id}")

    return await session.get(Items, item_id)


async def create_item(session: AsyncSession, item: ItemCreate) -> Items | None:
    logger.info("Creating new item")

    db_item = Items(**item.model_dump())
    session.add(db_item)
    await session.commit()
    await session.refresh(db_item)
    logger.info(f"Successfully created item with ID: {db_item.item_id}")
    return db_item


async def get_items_for_image(
    session: AsyncSession, image_id: str
) -> tuple[Sequence[Items], int]:
    logger.info(f"Fetching items for image {image_id}")

    items_stmt = select(Items).where(Items.image_id == uuid.UUID(image_id))
    items = (await session.scalars(items_stmt)).all()
    logger.info(f"Retrieved {len(items)} items for image {image_id}")
    return items, len(items)
