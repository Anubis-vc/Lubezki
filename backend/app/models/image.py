from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid


# Database model using SQLModel
class ImageBase(SQLModel):
    file_size: int = Field(description="File size in bytes")
    mime_type: str = Field(max_length=100)
    created_at: datetime = Field(default_factory=datetime.now)
    uploaded_at: datetime = Field(default_factory=datetime.now)
    is_analysis_complete: bool = False
    composition_score: int | None = Field(default=None, ge=0, le=100)


class ImageInTable(ImageBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: int | None = Field(
        default=None, index=True
    )  # TODO: look into "back populates"
    file_path: str = Field(max_length=500)


# API request models
class ImageCreate(ImageBase):
    user_id: int


class ImageUpdate(SQLModel):
    is_analysis_complete: bool | None = None
    composition_score: int | None = Field(default=None, ge=0, le=100)


# API Response models
class ImagePublic(ImageBase):
    id: uuid.UUID
    file_path: str = Field(max_length=500)


class ImagePublicList(SQLModel):
    images: list[ImagePublic]
    total: int
    limit: int
    offset: int
