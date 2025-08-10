import logging
import boto3
import uuid
from typing import Any, Sequence
from dotenv import load_dotenv

from app.core.config import settings
from app.models.model_definitions import Images

load_dotenv()

logger = logging.getLogger(__name__)

# TODO: could add cloudfront to help with costs and performance
# TODO: find a way to manage roles dynamically
s3_client = boto3.client("s3")


async def get_upload_url(
    filename: str,
) -> tuple[dict[str, Any], str]:
    """Upload an image to an s3 bucket"""
    logger.info(f"Generating upload URL for filename: {filename}")

    key = f"{uuid.uuid4()}-{filename}"
    presigned_url = s3_client.generate_presigned_post(
        Bucket=settings.AWS_BUCKET_NAME,
        Key=key,
        ExpiresIn=600,
        Conditions=["content-length-range", 0, settings.MAX_FILE_SIZE],
    )
    logger.info(f"Successfully generated upload URL for key: {key}")
    return presigned_url, key


async def get_single_image_url(key: str) -> str:
    """Get a presigned URL to view the image"""
    logger.debug(f"Generating download URL for key: {key}")

    url = s3_client.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": settings.AWS_BUCKET_NAME, "Key": key},
        ExpiresIn=3600,
    )
    logger.debug(f"Successfully generated download URL for key: {key}")
    return url


# TODO: there has to be a better way to do this
async def get_image_urls_bulk(images: Sequence[Images]) -> list[str]:
    """Get presigned URLs for a list of images"""
    logger.info(f"Generating bulk download URLs for {len(images)} images")

    urls = []
    for image in images:
        url = await get_single_image_url(image.storage_path)
        if url:
            urls.append(url)
        else:
            logger.error(f"Failed to generate download URL for image {image.image_id}")

    logger.info(
        f"Successfully generated {len(urls)} download URLs out of {len(images)} images"
    )
    return urls


async def delete_image(key: str) -> bool:
    """Delete an image from the bucket"""
    logger.info(f"Deleting image from S3 with key: {key}")

    s3_client.delete_object(Bucket=settings.AWS_BUCKET_NAME, Key=key)
    logger.info(f"Successfully deleted image from S3 with key: {key}")
    return True
