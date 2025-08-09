import boto3
from botocore.exceptions import ClientError
import uuid
from typing import Any, Sequence
from dotenv import load_dotenv

from app.core.config import settings
from app.models.model_definitions import Images

load_dotenv()

# TODO: could add cloudfront to help with costs and performance
# TODO: find a way to manage roles dynamically
s3_client = boto3.client("s3")


async def get_upload_url(
    filename: str,
) -> tuple[dict[str, Any], str] | tuple[None, None]:
    """Upload an image to an s3 bucket"""

    key = f"{uuid.uuid4()}-{filename}"
    try:
        presigned_url = s3_client.generate_presigned_post(
            Bucket=settings.AWS_BUCKET_NAME,
            Key=key,
            ExpiresIn=600,
            Conditions=["content-length-range", 0, settings.MAX_FILE_SIZE],
        )
        return presigned_url, key
    except Exception as e:
        print(e)
        return None, None


async def get_single_image_url(key: str) -> str | None:
    """Get a presigned URL to view the image"""

    try:
        url = s3_client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": settings.AWS_BUCKET_NAME, "Key": key},
            ExpiresIn=3600,
        )
        return url
    except Exception as e:
        print(e)
        return None


# TODO: there has to be a better way to do this
async def get_image_urls_bulk(images: Sequence[Images]) -> list[str]:
    """Get presigned URLs for a list of images"""

    urls = []
    try:
        for image in images:
            url = await get_single_image_url(image.storage_path)
            if url:
                urls.append(url)
    except Exception as e:
        print(e)
    return urls


async def delete_image(key: str) -> bool:
    """Delete an image from the bucket"""

    try:
        s3_client.delete_object(Bucket=settings.AWS_BUCKET_NAME, Key=key)
        return True
    except ClientError as e:
        print(e)
        return False
