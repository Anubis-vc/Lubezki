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
