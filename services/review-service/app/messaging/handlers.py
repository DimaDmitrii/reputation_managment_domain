from app.db import SessionFactory
from app.messaging.broker import broker
from app.messaging.events import ModerationCompletedEvent
from app.repositories.review import ReviewRepository


@broker.subscriber(
    "moderation.completed",
    group_id="review-service",
)
async def moderation_completed(
    event: ModerationCompletedEvent,
):
    async with SessionFactory() as session:

        repository = ReviewRepository(
            session
        )

        review = await repository.get(
            event.data.review_id
        )

        if review is None:
            return

        # простая идемпотентность для MVP
        if review.status != "pending_moderation":
            return

        await repository.update_moderation_status(
            review,
            status=event.data.decision,
            reason=event.data.reason,
        )
