from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class BoundingBox(BaseModel):
    center_x: int
    center_y: int
    height: int = Field(gt=0)
    width: int = Field(gt=0)


# main database item model
class Item(BaseModel):
    model_config = ConfigDict(extra="forbid")

    item_id: str
    image_id: int
    name: str
    bounding_box: BoundingBox
    analysis: str
    confidence_score: float | None = None
    created_at: datetime
    updated_at: datetime


# request models - what clients send to the api
class ItemCreate(BaseModel):
    image_id: int
    name: str
    bounding_box: BoundingBox
    analysis: str


class ItemUpdate(BaseModel):
    name: str | None = None
    bounding_box: BoundingBox | None
    analysis: str | None = None


class ItemDelete(BaseModel):
    item_id: str


# allow bulk creation of a model
class ItemBulkCreate(BaseModel):
    image_id: int
    items: list[ItemCreate]


# Response models - what clients receive from the API
class ItemResponse(BaseModel):
    item_id: str
    image_id: int
    name: str
    bounding_box: BoundingBox
    analysis: str
    created_at: datetime
    updated_at: datetime


# model for list of items
class ItemListResponse(BaseModel):
    items: list[ItemResponse]
    total_count: int
    image_id: int


class ItemAnalysisResponse(BaseModel):
    item_id: str
    name: str
    bounding_box: BoundingBox
    analysis: str
    image_id: int
