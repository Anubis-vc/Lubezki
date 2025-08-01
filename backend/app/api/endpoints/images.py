from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from typing import List, Optional
import json
import os

from app.services.image_service import ImageService
from app.services.gemini_service import GeminiService

router = APIRouter()
image_service = ImageService()
gemini_service = GeminiService()

@router.post("/upload", response_model=ImageResponse)
async def upload_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload an image for analysis
    """
    try:
        # Save file to disk
        file_path = image_service.save_uploaded_file(file)
        
        # Create database record
        db_image = image_service.create_image_record(db, file, file_path)
        
        return db_image
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{image_id}/analyze", response_model=ImageResponse)
async def analyze_image(
    image_id: int,
    analysis_request: AnalysisRequest,
    db: Session = Depends(get_db)
):
    """
    Analyze an uploaded image using Google Gemini
    """
    # Get image from database
    db_image = image_service.get_image_by_id(db, image_id)
    if not db_image:
        raise HTTPException(status_code=404, detail="Image not found")
    
    try:
        # Analyze image with Gemini
        analysis_result = gemini_service.analyze_image(
            db_image.file_path, 
            analysis_request.prompt
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
        
        # Update database with analysis results
        update_data = {
            "gemini_response": analysis_result,
            "analysis_summary": analysis_result["response_text"],
            "composition_score": composition_score
        }
        
        updated_image = image_service.update_image_analysis(db, image_id, update_data)
        
        return updated_image
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{image_id}", response_model=ImageResponse)
async def get_image(
    image_id: int,
    db: Session = Depends(get_db)
):
    """
    Get image details by ID
    """
    db_image = image_service.get_image_by_id(db, image_id)
    if not db_image:
        raise HTTPException(status_code=404, detail="Image not found")
    
    return db_image

@router.get("/", response_model=List[ImageResponse])
async def get_images(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all images with pagination
    """
    images = image_service.get_all_images(db, skip=skip, limit=limit)
    return images

@router.delete("/{image_id}")
async def delete_image(
    image_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete an image and its file
    """
    db_image = image_service.get_image_by_id(db, image_id)
    if not db_image:
        raise HTTPException(status_code=404, detail="Image not found")
    
    try:
        # Delete file from disk
        if os.path.exists(db_image.file_path):
            os.remove(db_image.file_path)
        
        # Delete from database
        db.delete(db_image)
        db.commit()
        
        return {"message": "Image deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 