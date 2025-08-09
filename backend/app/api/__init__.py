from fastapi import APIRouter
from app.api import images

api_router = APIRouter()
api_router.include_router(images.router, tags=["images"])
