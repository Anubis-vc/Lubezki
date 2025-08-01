import os
import uuid
from typing import Optional
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.models.image import Image
from app.schemas.image import ImageCreate, ImageUpdate
from app.core.config import settings

class ImageService:
    def __init__(self):
        self.upload_dir = settings.UPLOAD_DIR
        os.makedirs(self.upload_dir, exist_ok=True)
    
    def save_uploaded_file(self, file: UploadFile) -> str:
        """
        Save uploaded file to disk and return the file path
        """
        # Validate file extension
        file_extension = os.path.splitext(file.filename)[1].lower()
        if file_extension not in settings.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"File type not allowed. Allowed types: {settings.ALLOWED_EXTENSIONS}"
            )
        
        # Generate unique filename
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(self.upload_dir, unique_filename)
        
        # Save file
        try:
            with open(file_path, "wb") as buffer:
                content = file.file.read()
                if len(content) > settings.MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=400,
                        detail=f"File too large. Maximum size: {settings.MAX_FILE_SIZE} bytes"
                    )
                buffer.write(content)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")
        
        return file_path
    
    def create_image_record(self, db: Session, file: UploadFile, file_path: str) -> Image:
        """
        Create image record in database
        """
        file_extension = os.path.splitext(file.filename)[1].lower()
        unique_filename = os.path.basename(file_path)
        
        image_data = ImageCreate(
            filename=unique_filename,
            original_filename=file.filename,
            file_path=file_path,
            file_size=file.size,
            mime_type=file.content_type
        )
        
        db_image = Image(**image_data.dict())
        db.add(db_image)
        db.commit()
        db.refresh(db_image)
        
        return db_image
    
    def get_image_by_id(self, db: Session, image_id: int) -> Optional[Image]:
        """
        Get image by ID
        """
        return db.query(Image).filter(Image.id == image_id).first()
    
    def update_image_analysis(self, db: Session, image_id: int, analysis_data: dict) -> Optional[Image]:
        """
        Update image with analysis results
        """
        db_image = self.get_image_by_id(db, image_id)
        if not db_image:
            return None
        
        update_data = ImageUpdate(**analysis_data)
        for field, value in update_data.dict(exclude_unset=True).items():
            setattr(db_image, field, value)
        
        db.commit()
        db.refresh(db_image)
        return db_image
    
    def get_all_images(self, db: Session, skip: int = 0, limit: int = 100):
        """
        Get all images with pagination
        """
        return db.query(Image).offset(skip).limit(limit).all() 