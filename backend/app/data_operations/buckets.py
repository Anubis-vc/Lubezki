# # TODO: could add cloudfront to help with costs and performance
# TODO: find a way to manage roles dynamically
from typing import Any
from dotenv import load_dotenv
load_dotenv()

from app.core.config import settings

import boto3
from botocore.exceptions import ClientError
import uuid

s3_client = boto3.client("s3")

async def get_upload_url(filename: str) -> tuple[dict[str, Any], str]:
    """ Upload an image to an s3 bucket"""
    key = f"{uuid.uuid4()}-{filename}"
    
    presigned_url = s3_client.generate_presigned_post(
        Bucket=settings.AWS_BUCKET_NAME,
        Key=key,
        ExpiresIn=600,
        Conditions=["content-length-range", 0, 20 * 1024 * 1024]
    )
    return presigned_url, key


async def get_single_image_url(key: str) -> str:
    url = s3_client.generate_presigned_url(
		ClientMethod="get_object",
		Params={ "Bucket": settings.AWS_BUCKET_NAME, "Key": key },
		ExpiresIn=3600
	)
    return url

async def get_many_image_urls(keys: list[str]) -> list[str]:
    urls = []
    for key in keys:
        url = await get_single_image_url(key)
        urls.append(url)
    return urls

async def delete_image(key: str) -> bool:
    try:
        s3_client.delete_object(Bucket=settings.AWS_BUCKET_NAME, Key=key)
        return True
    except ClientError as e:
        print(e)
        return False