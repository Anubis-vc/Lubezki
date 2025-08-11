import contextlib
import logging
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.types import JSON
from sqlalchemy.pool import NullPool
from typing import Any, AsyncIterator
from sqlalchemy import text
from uuid import uuid4

from app.core.config import settings

logger = logging.getLogger(__name__)

class Base(DeclarativeBase):
    __mapper_args__ = {"eager_defaults": True}
    type_annotation_map = {
        dict[str, Any]: JSON,
    }

# lots of help from https://github.com/ThomasAitken/demo-fastapi-async-sqlalchemy/blob/main/backend/app/api/dependencies/core.py
class DatabaseSessionManager:
    def __init__(self, host: str, engine_kwargs: dict[str, Any]):
        self._engine = create_async_engine(
            host,
            echo=engine_kwargs.get("echo", False),
            poolclass=NullPool,
            connect_args={
                "prepared_statement_name_func": lambda: f"__asyncpg_{uuid4()}__",
                },
        )
        self._sessionmaker = async_sessionmaker(
            bind=self._engine,
            autocommit=False,
            expire_on_commit=False,
        )

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        """Get a database session"""
        async with self._sessionmaker() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise

    async def close(self):
        """Close the database engine"""
        if self._engine:
            await self._engine.dispose()

    async def health_check(self) -> bool:
        """Simple health check"""
        async with self.session() as session:
            result = await session.execute(text("SELECT 1"))
            return result.fetchone() is not None


# Create the session manager
session_manager = DatabaseSessionManager(
    settings.DB_CXN_STRING, {"echo": settings.echo_sql}
)


async def get_db_session():
    """Dependency function for getting database sessions"""
    async with session_manager.session() as session:
        yield session
