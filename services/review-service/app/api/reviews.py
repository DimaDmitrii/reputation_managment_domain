import uuid

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.messaging.broker import review_created_publisher
from app.messaging.events import ReviewCreatedEvent
from app.repositories.review import ReviewRepository
from app.schemas.review import (
    ReviewCreate,
    ReviewResponse,
)


router = APIRouter(
    prefix="/reviews",
    tags=["reviews"],
)


@router.post(
    "",
    response_model=ReviewResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_review(
    data: ReviewCreate,
    session: AsyncSession = Depends(get_session),
):
    repository = ReviewRepository(session)

    review = await repository.create(
        author_id=data.author_id,
        target_id=data.target_id,
        text=data.text,
        rating=data.rating,
        media_ids=[
            str(media_id)
            for media_id in data.media_ids
        ],
    )

    event = ReviewCreatedEvent.create(
        review.id
    )

    await review_created_publisher.publish(
        event.model_dump(mode="json"),
        key=str(review.id).encode(),
    )

    return review


@router.get(
    "/{review_id}",
    response_model=ReviewResponse,
)
async def get_review(
    review_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
):
    review = await ReviewRepository(
        session
    ).get(review_id)

    if review is None:
        raise HTTPException(
            status_code=404,
            detail="Review not found",
        )

    return review


@router.get(
    "/internal/{review_id}",
    response_model=ReviewResponse,
    include_in_schema=False,
)
async def get_internal_review(
    review_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
):
    review = await ReviewRepository(
        session
    ).get(review_id)

    if review is None:
        raise HTTPException(
            status_code=404,
            detail="Review not found",
        )

    return review
