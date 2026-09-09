from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    kafka_bootstrap_servers: str = "kafka:19092"

    review_service_url: str = (
        "http://review-service:8001"
    )

    ai_moderation_service_url: str = (
        "http://ai-moderation-service:8004"
    )


settings = Settings()
