from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Sequence
import uuid


class BoundingBox(BaseModel):
    y_min: int
    y_max: int
    x_min: int
    x_max: int


class ItemInTable(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    item_id: uuid.UUID
    image_id: uuid.UUID
    name: str
    bounding_box: dict[str, int]  # JSON from database
    analysis: str
    created_at: datetime
    is_positive: bool


class ItemCreate(BaseModel):
    image_id: uuid.UUID
    name: str
    bounding_box: BoundingBox
    analysis: str
    created_at: datetime = datetime.now()
    is_positive: bool


class ItemBulkCreate(BaseModel):
    image_id: uuid.UUID
    items: Sequence[ItemCreate]


class ItemResponse(BaseModel):
    item_id: uuid.UUID
    image_id: uuid.UUID
    name: str
    bounding_box: BoundingBox
    analysis: str
    is_positive: bool


class ItemListResponse(BaseModel):
    items: Sequence[ItemResponse]
    total: int
