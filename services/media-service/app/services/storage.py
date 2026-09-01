import asyncio

import boto3
from botocore.config import Config

from app.config import settings

class StorageService:

    def __init__(self):
        config = Config(
            signature_version="s3v4",
            s3={
                "addressing_style": "path",
            },
        )

        self.internal_client = boto3.client(
            "s3",
            endpoint_url=settings.s3_internal_endpoint,
            aws_access_key_id=settings.s3_access_key,
            aws_secret_access_key=settings.s3_secret_key,
            region_name=settings.s3_region,
            config=config,
        )

        self.public_client = boto3.client(
            "s3",
            endpoint_url=settings.s3_public_endpoint,
            aws_access_key_id=settings.s3_access_key,
            aws_secret_access_key=settings.s3_secret_key,
            region_name=settings.s3_region,
            config=config,
        )

    def generate_upload_url(
        self,
        *,
        object_key: str,
        content_type: str,
    ) -> str:

        return self.public_client.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": settings.s3_bucket,
                "Key": object_key,
                "ContentType": content_type,
            },
            ExpiresIn=settings.upload_url_ttl,
        )

    async def head_object(
        self,
        object_key: str,
    ) -> dict:

        return await asyncio.to_thread(
            self.internal_client.head_object,
            Bucket=settings.s3_bucket,
            Key=object_key,
        )


storage_service = StorageService()
