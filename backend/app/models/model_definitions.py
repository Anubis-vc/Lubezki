from typing import Annotated, Any
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
import uuid

from app.core.database_async import Base

timestamp = Annotated[
    datetime, mapped_column(nullable=False, server_default=func.current_timestamp())
]


class Items(Base):
    __tablename__ = "items"

    item_id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    image_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("images.image_id"), index=True
    )
    name: Mapped[str] = mapped_column(String(255))
    bounding_box: Mapped[
        dict[str, Any]
    ]  # Store as JSON: {"center_x": int, "center_y": int, "height": int, "width": int}
    analysis: Mapped[str] = mapped_column(Text)
    created_at: Mapped[timestamp]
    # as a reminder, this is just python sugar for the foreign key relationship, does not create a column in the database
    image: Mapped["Images"] = relationship("Images", back_populates="items")


class Images(Base):
    __tablename__ = "images"

    image_id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(index=True)
    created_at: Mapped[timestamp]
    original_name: Mapped[str] = mapped_column(String(255))
    bucket: Mapped[str] = mapped_column(String(255))
    storage_path: Mapped[str] = mapped_column(String(255))
    size_bytes: Mapped[int]
    mime_type: Mapped[str] = mapped_column(String(100))
    width_px: Mapped[int]
    height_px: Mapped[int]
    updated_at: Mapped[timestamp]
    is_analysis_complete: Mapped[bool | None] = mapped_column(default=False)
    score: Mapped[int | None] = mapped_column(default=None)  # 0-100 score
    analysis: Mapped[str | None] = mapped_column(Text, default=None)
    status: Mapped[str] = mapped_column(String(20), default="uploading")
    items: Mapped[list["Items"]] = relationship(
        "Items", back_populates="image", cascade="all, delete-orphan"
    )
