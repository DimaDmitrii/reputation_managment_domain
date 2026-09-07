import uuid

from botocore.exceptions import ClientError
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.db import get_session as get_session_db
from app.messaging.broker import media_uploaded_publisher
from app.messaging.events import MediaUploadedEvent
from app.repositories.media import MediaRepository
from app.schemas.media import (
    MediaCompleteResponse,
    MediaUploadCreate,
    MediaUploadResponse,
)
from app.services.storage import storage_service


router = APIRouter(
    prefix="/media",
    tags=["media"],
)


ALLOWED_CONTENT_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}


@router.post(
    "/uploads",
    response_model=MediaUploadResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_upload(
    data: MediaUploadCreate,
    session: AsyncSession = Depends(get_session_db)
):
    extension = check_extension_by(data.content_type)
    file_size = check_file_size_by(data.size)

    media_id = uuid.uuid4()
    object_key = (
        f"media/{media_id}/original{extension}"
    )

    repository = MediaRepository(session)
    await repository.create(
        media_id=media_id,
        filename=data.filename,
        object_key=object_key,
        content_type=data.content_type,
        expected_size=file_size,
    )

    upload_url = storage_service.generate_upload_url(
        object_key=object_key,
        content_type=data.content_type,
    )
    return MediaUploadResponse(
        media_id=media_id,
        upload_url=upload_url,
        expires_in=settings.upload_url_ttl,
    )


@router.post(
    "/{media_id}/complete",
    response_model=MediaCompleteResponse,
)
async def complete_upload(
    media_id: uuid.UUID,
    session: AsyncSession = Depends(get_session_db),
):
    repository = MediaRepository(session)
    media = await repository.get(media_id)
    check_media_uploaded(media)

    if media.status == "uploaded":
        return MediaCompleteResponse(
            media_id=media.id,
            status=media.status,
            size=media.actual_size or 0,
        )

    try:
        metadata = await storage_service.head_object(media.object_key)
    except ClientError as exc:
        error_code = exc.response.get(
            "Error",
            {},
        ).get("Code")

        if error_code in {
            "404",
            "NoSuchKey",
            "NotFound",
        }:
            raise HTTPException(
                status_code=409,
                detail="File has not been uploaded to S3",
            )

        raise
    
    actual_size = metadata["ContentLength"]
    check_actual_file_size(actual_size, media.expected_size)

    if media.status == "uploading":
        media = await repository.mark_uploaded(
            media,
            actual_size,
        )

    event = MediaUploadedEvent.create(
        media_id=media.id,
        object_key=media.object_key,
        content_type=media.content_type,
    )
    
    await media_uploaded_publisher.publish(
        event.model_dump(mode="json"),
        key=str(media.id).encode()
    )

    return MediaCompleteResponse(
        media_id=media.id,
        status=media.status,
        size=media.actual_size or actual_size,
    )


def check_extension_by(content_type: str):
    extension = ALLOWED_CONTENT_TYPES.get(content_type)
    if extension is None:
        raise HTTPException(
            status_code=415,
            detail="Unsupported media extension"
        )
    return extension

def check_file_size_by(file_size: int):
    if file_size > settings.max_file_size:
        raise HTTPException(
            status_code=413,
            detail="Uploaded file is too big"
        )
    return file_size

def check_media_uploaded(media: object):
    if media is None:
        raise HTTPException(
            status_code=404,
            detail="Media not found",
        )

def check_actual_file_size(actual_size: int, expected_size: int):
    if actual_size > settings.max_file_size:
        raise HTTPException(
            status_code=413,
            detail="Uploaded file is too large",
        )

    if actual_size != expected_size:
        raise HTTPException(
            status_code=409,
            detail=(
                "Uploaded file size does not match the declared size"
            ),
        )
