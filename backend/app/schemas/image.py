from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


# TODO: add validation for mime types
class ImageBase(BaseModel):
    file_size: int
    mime_type: str
    created_date: datetime
    updated_date: datetime
    dimensions: tuple[int, int]  # width x height
    user_id: int


class ImageInTable(ImageBase):
    model_config = ConfigDict(from_attributes=True)

    image_id: int
    is_analysis_complete: bool | None = None
    score: int | None = Field(default=None, ge=0, le=100)
    analysis: str | None = None


class ImageCreate(ImageBase):
    pass


class ImageUpdate(BaseModel):
    is_analysis_complete: bool | None = None
    score: int | None = Field(default=None, ge=0, le=100)
    analysis: str | None = None


class ImageResponse(BaseModel):
    user_id: int | None
    file_path: str
    mime_type: str
    is_analysis_complete: bool
    score: int | None
    analysis: str


class ImageListResponse(BaseModel):
    images: list[ImageResponse]
    total: int
    limit: int
    offset: int
