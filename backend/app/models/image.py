from pydantic import BaseModel, ConfigDict
from datetime import datetime


# Main database model - represents the complete image record
class Image(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: int
    user_id: int
    filename: str
    original_filename: str
    file_path: str
    # in bytes
    file_size: int
    mime_type: str
    uploaded_at: datetime
    # below updated after complete analysis
    is_analysis_complete: bool
    composition_score: int | None = None


# Request models - what clients send to the API
class ImageCreate(BaseModel):
    filename: str
    original_filename: str
    file_path: str
    file_size: int
    mime_type: str


class ImageUpdate(BaseModel):
    id: int
    user_id: int
    is_analysis_complete: bool
    composition_score: int


class ImageDelete(BaseModel):
    id: int


# Response models - what clients receive from the API
class ImageResponse(BaseModel):
    id: int
    filename: str
    original_filename: str
    file_path: str
    file_size: int
    mime_type: str
    uploaded_at: datetime
    is_analysis_complete: bool
    composition_score: int | None = None
