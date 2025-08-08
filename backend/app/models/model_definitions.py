from typing import Annotated, Any
from sqlalchemy import String, Text, ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
import uuid

from app.core.database_async import Base

timestamp = Annotated[
    datetime, mapped_column(nullable=False, server_default=func.current_timestamp())
]
int_pk = Annotated[int, mapped_column(BigInteger, primary_key=True)]


class Items(Base):
    __tablename__ = "items"

    item_id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    image_id: Mapped[int] = mapped_column(ForeignKey("images.image_id"), index=True)
    name: Mapped[str] = mapped_column(String(255))
    bounding_box: Mapped[
        dict[str, Any]
    ]  # Store as JSON: {"center_x": int, "center_y": int, "height": int, "width": int}
    analysis: Mapped[str] = mapped_column(Text)
    created_at: Mapped[timestamp]
    image: Mapped["Images"] = relationship("Images", back_populates="items")


class Images(Base):
    __tablename__ = "images"

    image_id: Mapped[int_pk]
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
    # as a reminder, this is just python sugar for the foreign key relationship, does not create a column in the database
    # user: Mapped["Users"] = relationship("Users", back_populates="images")
    items: Mapped[list["Items"]] = relationship(
        "Items", back_populates="image", cascade="all, delete-orphan"
    )


# TODO: commenting out for now, will need to figure out how to handle users

# class Users(Base):
#     __tablename__ = "users"

#     id: Mapped[int_pk]
#     email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
#     hashed_password: Mapped[str] = mapped_column(String(255))
#     created_at: Mapped[timestamp]
#     updated_at: Mapped[timestamp]
#     last_login: Mapped[datetime | None]
#     status: Mapped[str] = mapped_column(String(20), default="active")
#     images: Mapped[list[Images]] = relationship("Images", back_populates="user", cascade="all, delete-orphan")
