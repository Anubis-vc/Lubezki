from pydantic import BaseModel, ConfigDict
from datetime import datetime


# Main database model - represents the complete image record
class Image(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
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
    file_path: str
    file_size: int
    mime_type: str
    user_id: int


class ImageUpdate(BaseModel):
    id: str
    user_id: int
    is_analysis_complete: bool
    composition_score: int


class ImageDelete(BaseModel):
    id: str


# Response models - what clients receive from the API
class ImageCreateResponse(BaseModel):
    id: str