from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str

    s3_internal_endpoint: str
    s3_public_endpoint: str
    s3_access_key: str
    s3_secret_key: str
    s3_bucket: str = "review-media"
    s3_region: str = "us-east-1"

    upload_url_ttl: int = 900
    max_file_size: int = 10 * 1024 * 1024

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
