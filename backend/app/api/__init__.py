from fastapi import APIRouter
from app.api import images, items

api_router = APIRouter()
api_router.include_router(images.router, tags=["images"])
api_router.include_router(items.router, tags=["items"])
