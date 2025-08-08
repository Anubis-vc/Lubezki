from typing import Annotated, Any
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime

from app.core.database_async import Base


timestamp = Annotated[
    datetime, mapped_column(nullable=False, server_default=func.CURRENT_TIMESTAMP())
]


class Items(Base):
    __tablename__ = "Items"

    item_id: Mapped[int] = mapped_column(primary_key=True)
    image_id: Mapped[int] = mapped_column(index=True)
    name: Mapped[str] = mapped_column(String(255))
    bounding_box: Mapped[
        dict[str, Any]
    ]  # Store as JSON: {"center_x": int, "center_y": int, "height": int, "width": int}
    analysis: Mapped[str] = mapped_column(Text)
    created_at: Mapped[timestamp]


class Images(Base):
    __tablename__ = "Images"

    # may have to somehow get bigint for id if this fails
    image_id: Mapped[int] = mapped_column(primary_key=True)
    file_size: Mapped[int]
    mime_type: Mapped[str] = mapped_column(String(100))
    created_date: Mapped[timestamp]
    updated_date: Mapped[timestamp]
    dimensions: Mapped[str] = mapped_column(
        String(20)
    )  # Store as "width,height" string
    user_id: Mapped[int] = mapped_column(index=True)
    is_analysis_complete: Mapped[bool | None] = mapped_column(default=False)
    score: Mapped[int | None] = mapped_column(default=None)  # 0-100 score
    analysis: Mapped[str | None] = mapped_column(Text, default=None)


class Users(Base):
    __tablename__ = "Users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[timestamp]
    updated_at: Mapped[timestamp]
    last_login: Mapped[datetime | None]
    status: Mapped[str] = mapped_column(String(20), default="active")
