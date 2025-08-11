import logging
from fastapi import APIRouter, HTTPException
import uuid

from app.api.deps import SessionDep
from app.data_operations import get_item, get_items_for_image
from app.schemas.item import ItemResponse, ItemListResponse

router = APIRouter(prefix="/items")
logger = logging.getLogger(__name__)


@router.get("/{item_id}/", response_model=ItemResponse)
async def get_item_by_id(item_id: uuid.UUID, db: SessionDep):
    """Get an item by its ID"""

    try:
        db_item = await get_item(db, item_id)
        if not db_item:
            logger.warning(f"Item not found with ID: {item_id}")
            raise HTTPException(status_code=404, detail="Item not found")

        logger.info(f"Successfully retrieved item with ID: {item_id}")
        return db_item
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error fetching item {item_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/image/{image_id}/", response_model=ItemListResponse)
async def get_items_by_image_id(image_id: int, db: SessionDep):
    """Get all items for a specific image"""

    try:
        items, count = await get_items_for_image(db, image_id)
        logger.info(f"Successfully retrieved {count} items for image {image_id}")
        return {"items": items, "count": count}
    except Exception as e:
        logger.error(f"Error fetching items for image {image_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
