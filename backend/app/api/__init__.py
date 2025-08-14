from fastapi import APIRouter
from app.api import images, items, basic

api_router = APIRouter()
api_router.include_router(images.router, tags=["images"])
api_router.include_router(items.router, tags=["items"])
api_router.include_router(basic.router, tags=["basic"])
