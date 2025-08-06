from app.core.database import get_supabase
from fastapi import UploadFile
from fastapi.encoders import jsonable_encoder

# models for db upload and everything
from app.models import ImageCreate
from backend.app.models.image import Image

# TODO: add security and oauth lol
# TODO: Reconfigure database to have row level security and policies
# TODO: Set up bucket for uploads.

# uploading image to storage for anything less than 6 MB
def upload_to_blob_standard(bucket_name: str, filename: str, file: UploadFile) -> str:
    supabase = get_supabase()
    data, _ = supabase.storage.from_(bucket_name).upload(filename, file)
    return data if data else None

# add an image record to db
def insert_image(image: ImageCreate) -> Image:
    supabase = get_supabase()
    image = jsonable_encoder(image)
    data = supabase.table('images').insert(image).execute()
    
    # this returns a dictionary representation of the new image
    return data.data[0] if data.data else None

def get_image_by_id(image_id):
    """Get image by ID"""
    supabase = get_supabase()
    result = supabase.table('images').select('*').eq('id', image_id).execute()
    return result.data[0] if result.data else None

def get_all_images(limit=100, offset=0):
    """Get all images with pagination"""
    supabase = get_supabase()
    result = supabase.table('images').select('*').order('uploaded_at', desc=True).range(offset, offset + limit - 1).execute()
    return result.data

def update_image_analysis(image_id, gemini_response, analysis_summary, composition_score):
    """Update image with analysis results"""
    supabase = get_supabase()
    data = {
        'gemini_response': gemini_response,
        'analysis_summary': analysis_summary,
        'composition_score': composition_score
    }
    result = supabase.table('images').update(data).eq('id', image_id).execute()
    return result.data[0] if result.data else None

def delete_image(image_id):
    """Delete image by ID"""
    supabase = get_supabase()
    result = supabase.table('images').delete().eq('id', image_id).execute()
    return result.data[0] if result.data else None 