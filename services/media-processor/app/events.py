import uuid
from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel


class MediaUploadedData(BaseModel):
    media_id: uuid.UUID
    object_key: str
    content_type: str


class MediaUploadedEvent(BaseModel):
    event_id: uuid.UUID
    event_type: Literal["media.uploaded"]
    event_version: int
    occurred_at: datetime
    data: MediaUploadedData


class MediaProcessedData(BaseModel):
    media_id: uuid.UUID
    preview_key: str
    medium_key: str


class MediaProcessedEvent(BaseModel):
    event_id: uuid.UUID
    event_type: Literal["media.processed"] = "media.processed"
    event_version: int = 1
    occurred_at: datetime
    data: MediaProcessedData

    @classmethod
    def create(
        cls,
        *,
        media_id: uuid.UUID,
        preview_key: str,
        medium_key: str,
    ):
        return cls(
            event_id=uuid.uuid4(),
            occurred_at=datetime.now(timezone.utc),
            data=MediaProcessedData(
                media_id=media_id,
                preview_key=preview_key,
                medium_key=medium_key,
            ),
        )
