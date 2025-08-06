from fastapi import APIRouter, Depends, HTTPException, UploadFile, status, Cookie
from typing import Annotated
from datetime import datetime
import uuid

# importing all the models
from app.models import ImageCreate, ImageDelete, ImageUpdate, ImageCreateResponse

# importing services (keep GeminiService as it has actual logic)
from app.services.gemini_service import GeminiService

# importing queries directly
from app.utils.queries import (
    upload_to_blob_standard, 
    insert_image, 
    get_image_by_id, 
    update_image_analysis, 
    get_all_images,
    delete_image
)

# importing config for bucket settings
from app.core.config import settings

router = APIRouter()
gemini_service = GeminiService()

# TODO: how to get a file upload into the db

'''
1) Bring file in
2) Add file to db associated with a user with all its info
3) Send file to image analysis processing
4) Allow user to see image before it is done processing, provided by flag in db
5) Once analysis complete, update the Images and Items tables

Useful to decouple these pieces? Is it possible to run the second process in the background
somehow while the user can still look at the image
'''

# upload image to blob storage and add to db for the user
@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_image(user_id: str, file: UploadFile) -> dict:
    # Upload to blob storage directly
    blob_url = upload_to_blob_standard(
        settings.BUCKET_NAME, 
        f"{user_id}/{uuid.uuid4()}", 
        file
    )
    
    # Create image record
    image_record = ImageCreate(
        filename=file.filename,
        file_path=blob_url,
        file_size=file.size,
        mime_type=file.content_type,
        user_id=user_id,
    )
    
    # Insert directly into database
    response = insert_image(image_record)
    if not response:
        raise HTTPException(status_code=500, detail="Internal server error")
    
    return {"id": response["id"]}

@router.post("/{image_id}/analyze", response_model=ImageResponse)
async def analyze_image(image_id: int, analysis_request: dict):
    """
    Analyze an uploaded image using Google Gemini
    """
    # Get image from database directly
    db_image = get_image_by_id(image_id)
    if not db_image:
        raise HTTPException(status_code=404, detail="Image not found")
    
    try:
        # Analyze image with Gemini
        analysis_result = gemini_service.analyze_image(
            db_image["file_path"], 
            analysis_request.get("prompt")
        )
        
        if not analysis_result["success"]:
            raise HTTPException(
                status_code=500, 
                detail=f"Analysis failed: {analysis_result['error']}"
            )
        
        # Extract composition score from response (simple heuristic)
        composition_score = None
        response_text = analysis_result["response_text"].lower()
        if "score" in response_text or "rating" in response_text:
            # Simple score extraction - you might want to improve this
            for i in range(1, 11):
                if f"score: {i}" in response_text or f"rating: {i}" in response_text:
                    composition_score = i
                    break
        
        # Update database with analysis results directly
        updated_image = update_image_analysis(
            image_id=image_id,
            gemini_response=analysis_result,
            analysis_summary=analysis_result["response_text"],
            composition_score=composition_score
        )
        
        return ImageResponse(**updated_image)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{image_id}", response_model=ImageResponse)
async def get_image(image_id: int):
    """
    Get image details by ID
    """
    db_image = get_image_by_id(image_id)
    if not db_image:
        raise HTTPException(status_code=404, detail="Image not found")
    
    return ImageResponse(**db_image)

@router.get("/", response_model=list[ImageResponse])
async def get_images(skip: int = 0, limit: int = 100):
    """
    Get all images with pagination
    """
    images_data = get_all_images(limit=limit, offset=skip)
    return [ImageResponse(**image) for image in images_data]

@router.delete("/{image_id}")
async def delete_image(image_id: str):
    """
    Delete an image and its file
    """
    db_image = get_image_by_id(image_id)
    if not db_image:
        raise HTTPException(status_code=404, detail="Image not found")
    
    try:
        # Delete from database directly
        result = delete_image(image_id)
        if not result:
            raise HTTPException(status_code=500, detail="Failed to delete image")
        
        return {"message": "Image deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 