import asyncio
from io import BytesIO

import boto3
from botocore.config import Config

from app.config import settings


class StorageService:

    def __init__(self):
        self.client = boto3.client(
            "s3",
            endpoint_url=settings.s3_endpoint,
            aws_access_key_id=settings.s3_access_key,
            aws_secret_access_key=settings.s3_secret_key,
            region_name=settings.s3_region,
            config=Config(
                signature_version="s3v4",
                s3={
                    "addressing_style": "path",
                },
            ),
        )

    async def download(
        self,
        object_key: str,
    ) -> bytes:

        def _download():
            response = self.client.get_object(
                Bucket=settings.s3_bucket,
                Key=object_key,
            )

            return response["Body"].read()

        return await asyncio.to_thread(
            _download
        )

    async def upload(
        self,
        *,
        object_key: str,
        data: bytes,
        content_type: str,
    ):

        def _upload():
            self.client.put_object(
                Bucket=settings.s3_bucket,
                Key=object_key,
                Body=BytesIO(data),
                ContentType=content_type,
            )

        await asyncio.to_thread(
            _upload
        )


storage_service = StorageService()
