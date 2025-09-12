from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, Header

from app.core.database_async import get_db_session
from app.core.config import settings

SessionDep = Annotated[AsyncSession, Depends(get_db_session)]


async def verify_api_key(x_api_key: str = Header(None)) -> str:
    """Simple API key authentication dependency"""
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API key required")
    
    if x_api_key != settings.API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    
    return x_api_key
