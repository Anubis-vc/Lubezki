import logging
import boto3
from dotenv import load_dotenv
import uuid
from PIL import Image
import io

from app.core.config import settings

load_dotenv()

logger = logging.getLogger(__name__)
s3_client = boto3.client("s3")


async def get_single_image_url(key: str) -> str:
    """Get a presigned URL to view the image"""
    logger.debug(f"Generating download URL for key: {key}")

    url = s3_client.generate_presigned_url(
        ClientMethod="get_object",
        Params={"bucket": settings.AWS_BASIC_BUCKET_NAME, "key": key},
        ExpiresIn=86400,
    )
    logger.debug(f"Successfully generated download URL for key: {key}")
    return url


async def get_gallery_urls() -> list[str]:
    """Get all the images from the gallery bucket"""

    urls = []
    response = s3_client.list_objects_v2(Bucket=settings.AWS_BASIC_BUCKET_NAME)
    for object in response["Contents"]:
        key = object["Key"]
        url = await get_single_image_url(key)
        urls.append(url)
    return urls


async def upload_file(file: Image.Image) -> str:
    key = str(uuid.uuid4())
    in_memory_file = io.BytesIO()
    file.save(in_memory_file, format="JPEG")
    in_memory_file.seek(0)

    s3_client.put_object(
        Bucket=settings.AWS_BASIC_BUCKET_NAME,
        Key=key,
        Body=in_memory_file,
        ContentType=f"image/{file.format}",
    )
    return key
