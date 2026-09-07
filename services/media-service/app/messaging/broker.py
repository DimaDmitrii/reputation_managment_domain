from faststream.kafka import KafkaBroker

from app.config import settings


broker = KafkaBroker(
    settings.kafka_bootstrap_servers,
)

media_uploaded_publisher = broker.publisher(
    "media.uploaded",
)
