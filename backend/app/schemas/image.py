from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Sequence, Any
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
    status: str = "pending"


class ImageInTable(ImageBase):
    model_config = ConfigDict(from_attributes=True)

    image_id: int
    user_id: uuid.UUID
    storage_path: str


class ImageCreate(ImageBase):
    user_id: uuid.UUID


class ImageCreateURLResponse(BaseModel):
    presigned_url: dict[str, Any]


class ImageAnalysisUpdate(BaseModel):
    image_id: int
    is_analysis_complete: bool
    score: int
    analysis: str
    updated_at: datetime = datetime.now()


class ImageUploadUpdate(BaseModel):
    image_id: int
    status: str


class ImageResponse(BaseModel):
    original_name: str
    size_bytes: int
    mime_type: str
    width_px: int
    height_px: int
    is_analysis_complete: bool = False
    score: int | None = Field(default=None, ge=0, le=100)
    analysis: str | None = None
    download_url: str


class ImageListResponse(BaseModel):
    images: Sequence[ImageResponse]
    urls: list[str]
    total: int
    cursor: datetime


class ImageDeleteResponse(BaseModel):
    message: str
    s3_deleted: bool
    db_deleted: bool
