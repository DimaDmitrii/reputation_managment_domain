import uuid

from pydantic import BaseModel, Field


class MediaUploadCreate(BaseModel):
    filename: str = Field(
        min_length=1,
        max_length=255,
    )

    content_type: str

    size: int = Field(
        gt=0,
    )


class MediaUploadResponse(BaseModel):
    media_id: uuid.UUID
    upload_url: str
    expires_in: int


class MediaCompleteResponse(BaseModel):
    media_id: uuid.UUID
    status: str
    size: int


class MediaUploadedData(BaseModel):
    media_id: uuid.UUID
    object_key: str
    content_type: str
