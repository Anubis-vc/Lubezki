from fastapi import APIRouter, Depends, HTTPException, UploadFile, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.api.deps import SessionDep
from app.models.image import ImageCreate, ImageUpdate, ImageResponse, ImageListResponse
from app.services.gemini_service import GeminiService

from app.utils.queries import (
    save_uploaded_file,
    create_image,
    get_image_by_id,
    update_image_analysis,
    get_images,
    delete_image,
    image_to_response,
    create_image_list_response
)

# Import database dependency
from app.core.database import get_db
from app.core.config import settings

router = APIRouter()
gemini_service = GeminiService()


@router.post("/upload", response_model=ImageResponse, status_code=status.HTTP_201_CREATED)
async def upload_image(
    user_id: int,
    file: UploadFile,
    db: AsyncSession = Depends(get_db)
) -> ImageResponse:
    """Upload an image file and create a database record"""
    
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=400, 
            detail="File must be an image"
        )
    
    # Validate file size
    if file.size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File size must be less than {settings.MAX_FILE_SIZE} bytes"
        )
    
    try:
        # Save file to disk
        file_path, filename = await save_uploaded_file(file, settings.UPLOAD_DIR)
        
        # Create image record
        image_data = ImageCreate(
            filename=filename,
            original_filename=file.filename,
            file_path=file_path,
            file_size=file.size,
            mime_type=file.content_type,
            user_id=user_id,
        )
        
        # Insert into database
        db_image = await create_image(db, image_data)
        
        return image_to_response(db_image)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.post("/{image_id}/analyze", response_model=ImageResponse)
async def analyze_image(
    image_id: str,
    analysis_request: dict,
    db: AsyncSession = Depends(get_db)
):
    """Analyze an uploaded image using Google Gemini"""
    
    # Get image from database
    db_image = await get_image_by_id(db, image_id)
    if not db_image:
        raise HTTPException(status_code=404, detail="Image not found")
    
    try:
        # Analyze image with Gemini
        analysis_result = gemini_service.analyze_image(
            db_image.file_path, 
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
        
        # Update database with analysis results
        updated_image = await update_image_analysis(
            db=db,
            image_id=image_id,
            gemini_response=analysis_result["response_text"],
            analysis_summary=analysis_result["response_text"],
            composition_score=composition_score
        )
        
        return image_to_response(updated_image)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{image_id}", response_model=ImageResponse)
async def get_image(
    image_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get image details by ID"""
    db_image = await get_image_by_id(db, image_id)
    if not db_image:
        raise HTTPException(status_code=404, detail="Image not found")
    
    return image_to_response(db_image)


@router.get("/", response_model=ImageListResponse)
async def get_images_endpoint(
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    limit: int = Query(100, ge=1, le=1000, description="Number of images to return"),
    offset: int = Query(0, ge=0, description="Number of images to skip"),
    db: AsyncSession = Depends(get_db)
):
    """Get images with optional filtering and pagination"""
    images, total = await get_images(
        db=db,
        user_id=user_id,
        limit=limit,
        offset=offset
    )
    
    return create_image_list_response(images, total, limit, offset)


@router.put("/{image_id}", response_model=ImageResponse)
async def update_image(
    image_id: str,
    image_update: ImageUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update image metadata"""
    from app.utils.queries import update_image as update_image_query
    
    db_image = await update_image_query(db, image_id, image_update)
    if not db_image:
        raise HTTPException(status_code=404, detail="Image not found")
    
    return image_to_response(db_image)


@router.delete("/{image_id}")
async def delete_image_endpoint(
    image_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Delete an image and its file"""
    success = await delete_image(db, image_id)
    if not success:
        raise HTTPException(status_code=404, detail="Image not found")
    
    return {"message": "Image deleted successfully"} 