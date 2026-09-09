import httpx

from faststream import FastStream
from faststream.kafka import KafkaBroker

from app.config import settings
from app.events import (
    ModerationCompletedEvent,
    ReviewCreatedEvent,
)


broker = KafkaBroker(
    settings.kafka_bootstrap_servers
)

app = FastStream(broker)


moderation_publisher = broker.publisher(
    "moderation.completed"
)


def make_decision(
    *,
    probability: float,
    confidence: float,
) -> str:

    if probability >= 0.85 and confidence >= 0.70:
        return "rejected"

    if probability <= 0.20 and confidence >= 0.70:
        return "published"

    return "manual_review"


@broker.subscriber(
    "review.created",
    group_id="moderation-service",
)
async def moderate_review(
    event: ReviewCreatedEvent,
):

    review_id = event.data.review_id

    async with httpx.AsyncClient(
        timeout=10,
    ) as client:

        # 1. Получаем Review
        response = await client.get(
            (
                f"{settings.review_service_url}"
                f"/reviews/internal/{review_id}"
            )
        )

        response.raise_for_status()

        review = response.json()

        # 2. AI analysis
        response = await client.post(
            (
                f"{settings.ai_moderation_service_url}"
                "/moderate"
            ),
            json={
                "text": review["text"],
            },
        )

        response.raise_for_status()

        ai_result = response.json()

    # 3. Business decision
    decision = make_decision(
        probability=(
            ai_result["violation_probability"]
        ),
        confidence=ai_result["confidence"],
    )

    # 4. Результат
    result_event = (
        ModerationCompletedEvent.create(
            review_id=review_id,
            decision=decision,
            reason=ai_result["explanation"],
            category=ai_result["category"],
            violation_probability=(
                ai_result[
                    "violation_probability"
                ]
            ),
            confidence=ai_result["confidence"],
        )
    )

    # 5. обратно в Kafka
    await moderation_publisher.publish(
        result_event.model_dump(
            mode="json"
        ),
        key=str(review_id).encode(),
    )
