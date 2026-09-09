import uuid
from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel


class ReviewCreatedData(BaseModel):
    review_id: uuid.UUID


class ReviewCreatedEvent(BaseModel):
    event_id: uuid.UUID
    event_type: Literal["review.created"] = "review.created"
    event_version: int = 1
    occurred_at: datetime
    data: ReviewCreatedData

    @classmethod
    def create(
        cls,
        review_id: uuid.UUID,
    ):
        return cls(
            event_id=uuid.uuid4(),
            occurred_at=datetime.now(timezone.utc),
            data=ReviewCreatedData(
                review_id=review_id,
            ),
        )


class ModerationCompletedData(BaseModel):
    review_id: uuid.UUID
    decision: str
    reason: str

    category: str
    violation_probability: float
    confidence: float


class ModerationCompletedEvent(BaseModel):
    event_id: uuid.UUID
    event_type: Literal["moderation.completed"]
    event_version: int
    occurred_at: datetime
    data: ModerationCompletedData
