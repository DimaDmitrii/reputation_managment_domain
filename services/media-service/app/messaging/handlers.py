from faststream import AckPolicy

from app.db import SessionFactory
from app.messaging.broker import broker
from app.messaging.events import MediaProcessedEvent
from app.repositories.media import MediaRepository


@broker.subscriber(
    "media.processed",
    group_id="media-service",
    ack_policy=AckPolicy.NACK_ON_ERROR,
)
async def handle_media_processed(
    event: MediaProcessedEvent,
):
    async with SessionFactory() as session:
        repository = MediaRepository(
            session
        )

        media = await repository.get(
            event.data.media_id
        )

        if media is None:
            return

        if media.status == "processed":
            return

        await repository.mark_processed(
            media,
            preview_key=event.data.preview_key,
            medium_key=event.data.medium_key,
        )
