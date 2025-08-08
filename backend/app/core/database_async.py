import contextlib
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    AsyncConnection,
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.types import JSON
from typing import Any, AsyncIterator

from app.core.config import settings


class Base(DeclarativeBase):
    __mapper_args__ = {"eager_defaults": True}
    type_annotation_map = {dict[str, Any]: JSON}


class DatabaseSessionManager:
    def __init__(self, host: str, engine_kwargs: dict[str, Any]):
        self._engine = create_async_engine(host, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(
            autocommit=False, bind=self._engine, expire_on_commit=False
        )

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if not self._engine:
            raise Exception("DatabaseSessionManager not initialized")

        async with self._engine.begin() as conn:
            try:
                yield conn
            except Exception:
                await conn.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if not self._sessionmaker:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._sessionmaker() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise

    async def close(self):
        if not self._engine:
            raise Exception("DatabaseSessionManager not initialized")

        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None


session_manager = DatabaseSessionManager(
    settings.DB_CXN_STRING, {"echo": settings.echo_sql}
)


# TODO: may have to update this like this, don't know tradeoff yet
# async def get_db():
#     async with session_manager.session() as session:
#         try:
#             yield session
#             await session.commit()
#         except Exception:
#             if session.in_transaction():
#                 await session.rollback()
#             raise
async def get_db():
    async with session_manager.session() as session:
        yield session
