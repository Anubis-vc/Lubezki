from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class BoundingBox(BaseModel):
    center_x: int
    center_y: int
    height: int = Field(gt=0)
    width: int = Field(gt=0)


class ItemInTable(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    id: int
    image_id: int
    name: str
    x_center: int = Field(ge=0)
    y_center: int = Field(ge=0)
    width: int = Field(ge=0)
    height: int = Field(ge=0)
    analysis: str
    created_at: datetime


class ItemCreate(BaseModel):
    image_id: int
    name: str
    bounding_box: BoundingBox
    analysis: str


class ItemDelete(BaseModel):
    item_id: str


class ItemBulkCreate(BaseModel):
    image_id: int
    items: list[ItemCreate]


class ItemResponse(BaseModel):
    item_id: str
    image_id: int
    name: str
    bounding_box: BoundingBox
    analysis: str
    created_at: datetime


class ItemListResponse(BaseModel):
    items: list[ItemResponse]
    total_count: int
    image_id: int
