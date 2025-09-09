from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Sequence, Any
import uuid


class ImageBase(BaseModel):
    created_at: datetime
    original_name: str
    bucket: str
    storage_key: str
    thumbnail_key: str
    size_bytes: int
    mime_type: str
    width_px: int
    height_px: int
    thumbnail_width_px: int
    thumbnail_height_px: int
    updated_at: datetime
    is_analysis_complete: bool = False
    score: dict[str, Any] | None = Field(
        default=None, description="JSONB scores for multiple categories"
    )
    analysis: str | None = None
    status: str = "pending"


class ImageInTable(ImageBase):
    model_config = ConfigDict(from_attributes=True)

    image_id: uuid.UUID
    storage_key: str
    thumbnail_key: str


class ImageCreate(ImageBase):
    pass


class ImageCreateURLResponse(BaseModel):
    presigned_url: dict[str, Any]
    message: str


class ImageAnalysisUpdate(BaseModel):
    image_id: uuid.UUID
    is_analysis_complete: bool
    score: dict[str, Any]
    analysis: str
    updated_at: datetime = datetime.now()


class ImageUploadUpdate(BaseModel):
    image_id: uuid.UUID
    status: str


class ImageResponse(BaseModel):
    original_name: str
    size_bytes: int
    mime_type: str
    width_px: int
    height_px: int
    is_analysis_complete: bool = False
    score: dict[str, Any] | None = Field(
        default=None, description="JSONB scores for multiple categories"
    )
    analysis: str | None = None
    download_url: str


class ImageGalleryImage(BaseModel):
    base_image: str
    height_px: int
    width_px: int
    thumbnail_image: str
    thumbnail_width_px: int
    thumbnail_height_px: int


class ImageGalleryResponse(BaseModel):
    images: list[ImageGalleryImage]


class ImageListResponse(BaseModel):
    images: Sequence[ImageResponse]
    urls: list[str]
    total: int
    cursor: datetime


class ImageDeleteResponse(BaseModel):
    message: str
    s3_deleted: bool
    db_deleted: bool
