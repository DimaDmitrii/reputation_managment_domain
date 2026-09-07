from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    kafka_bootstrap_servers: str = "kafka:19092"

    s3_endpoint: str = "http://minio:9000"
    s3_access_key: str
    s3_secret_key: str
    s3_bucket: str = "review-media"
    s3_region: str = "us-east-1"


settings = Settings()
