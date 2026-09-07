import asyncio

from faststream import (
    AckPolicy,
    FastStream,
)
from faststream.kafka import KafkaBroker

from app.config import settings
from app.events import (
    MediaProcessedEvent,
    MediaUploadedEvent,
)
from app.image_processor import create_variant
from app.storage import storage_service


broker = KafkaBroker(
    settings.kafka_bootstrap_servers,
)

app = FastStream(broker)


processed_publisher = broker.publisher(
    "media.processed"
)


@broker.subscriber(
    "media.uploaded",
    group_id="media-processor",
    ack_policy=AckPolicy.NACK_ON_ERROR,
)
async def process_media(
    event: MediaUploadedEvent,
):
    media_id = event.data.media_id

    original = await storage_service.download(
        event.data.object_key
    )

    preview, medium = await asyncio.gather(
        asyncio.to_thread(
            create_variant,
            original,
            max_side=320,
            watermark=False,
            quality=78,
        ),
        asyncio.to_thread(
            create_variant,
            original,
            max_side=1280,
            watermark=True,
            quality=82,
        ),
    )

    base_key = f"media/{media_id}"

    preview_key = (
        f"{base_key}/preview.webp"
    )

    medium_key = (
        f"{base_key}/medium.webp"
    )

    await asyncio.gather(
        storage_service.upload(
            object_key=preview_key,
            data=preview,
            content_type="image/webp",
        ),
        storage_service.upload(
            object_key=medium_key,
            data=medium,
            content_type="image/webp",
        ),
    )

    processed_event = MediaProcessedEvent.create(
        media_id=media_id,
        preview_key=preview_key,
        medium_key=medium_key,
    )

    await processed_publisher.publish(
        processed_event.model_dump(
            mode="json"
        ),
        key=str(media_id).encode(),
    )
