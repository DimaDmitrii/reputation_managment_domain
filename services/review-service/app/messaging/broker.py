from faststream.kafka import KafkaBroker

from app.config import settings


broker = KafkaBroker(
    settings.kafka_bootstrap_servers,
)


review_created_publisher = broker.publisher(
    "review.created"
)
