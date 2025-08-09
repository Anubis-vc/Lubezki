from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Sequence
from fastapi import HTTPException

from app.models.model_definitions import Items
from app.schemas.item import ItemCreate


async def get_item_by_id(session: AsyncSession, item_id: int) -> Items | None:
    return await session.get(Items, item_id)


async def create_item(session: AsyncSession, item: ItemCreate) -> Items:
    db_item = Items(**item.model_dump())
    session.add(db_item)
    await session.commit()
    await session.refresh(db_item)
    return db_item


# TODO: this uses two queries, can we do it in one?
async def get_items_for_image(
    session: AsyncSession, image_id: int
) -> tuple[Sequence[Items], int]:
    count_stmt = (
        select(func.count()).select_from(Items).where(Items.image_id == image_id)
    )
    count = await session.scalar(count_stmt) or 0

    if count == 0:
        raise HTTPException(status_code=404, detail="No items found for image")

    items_stmt = select(Items).where(Items.image_id == image_id)
    items = (await session.scalars(items_stmt)).all()

    return items, count
