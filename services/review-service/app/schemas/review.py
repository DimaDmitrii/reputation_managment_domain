import uuid

from pydantic import BaseModel, Field


class ReviewCreate(BaseModel):
    author_id: uuid.UUID
    target_id: uuid.UUID

    text: str = Field(
        min_length=1,
        max_length=5000,
    )

    rating: int = Field(
        ge=1,
        le=5,
    )

    media_ids: list[uuid.UUID] = []


class ReviewResponse(BaseModel):
    id: uuid.UUID
    author_id: uuid.UUID
    target_id: uuid.UUID

    text: str
    rating: int

    media_ids: list[str]

    status: str
    moderation_reason: str | None

    model_config = {
        "from_attributes": True,
    }
