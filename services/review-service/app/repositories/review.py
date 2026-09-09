import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.review import Review


class ReviewRepository:

    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def create(
        self,
        *,
        author_id: uuid.UUID,
        target_id: uuid.UUID,
        text: str,
        rating: int,
        media_ids: list[str],
    ) -> Review:

        review = Review(
            author_id=author_id,
            target_id=target_id,
            text=text,
            rating=rating,
            media_ids=media_ids,
            status="pending_moderation",
        )

        self.session.add(review)

        await self.session.commit()
        await self.session.refresh(review)

        return review

    async def get(
        self,
        review_id: uuid.UUID,
    ) -> Review | None:

        result = await self.session.execute(
            select(Review).where(
                Review.id == review_id
            )
        )

        return result.scalar_one_or_none()

    async def update_moderation_status(
        self,
        review: Review,
        *,
        status: str,
        reason: str,
    ) -> None:

        review.status = status
        review.moderation_reason = reason

        await self.session.commit()
