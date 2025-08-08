from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Sequence
import uuid


# TODO: add validation for mime types
class ImageBase(BaseModel):
    created_at: datetime
    original_name: str
    bucket: str
    storage_path: str
    size_bytes: int
    mime_type: str
    width_px: int
    height_px: int
    updated_at: datetime
    is_analysis_complete: bool = False
    score: int | None = Field(default=None, ge=0, le=100)
    analysis: str | None = None


class ImageInTable(ImageBase):
    model_config = ConfigDict(from_attributes=True)

    image_id: int
    user_id: uuid.UUID
    storage_path: str


class ImageCreate(ImageBase):
    user_id: uuid.UUID


class ImageUpdate(BaseModel):
    image_id: int
    is_analysis_complete: bool = False
    score: int | None = None
    analysis: str | None = None
    updated_at: datetime = datetime.now()


class ImageResponse(ImageBase):
    image_id: int


class ImageListResponse(BaseModel):
    images: Sequence[ImageResponse]
    total: int
    limit: int
    offset: int
