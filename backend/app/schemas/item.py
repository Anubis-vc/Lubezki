from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Sequence
import uuid


class BoundingBox(BaseModel):
    center_x: int
    center_y: int
    height: int = Field(gt=0)
    width: int = Field(gt=0)


class ItemInTable(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    item_id: uuid.UUID
    image_id: int
    name: str
    bounding_box: BoundingBox
    analysis: str
    created_at: datetime


class ItemCreate(BaseModel):
    image_id: int
    name: str
    bounding_box: BoundingBox
    analysis: str
    created_at: datetime = datetime.now()


class ItemBulkCreate(BaseModel):
    image_id: int
    items: Sequence[ItemCreate]


class ItemResponse(BaseModel):
    item_id: uuid.UUID
    image_id: int
    name: str
    bounding_box: BoundingBox
    analysis: str


class ItemListResponse(BaseModel):
    items: Sequence[ItemResponse]
    total: int
