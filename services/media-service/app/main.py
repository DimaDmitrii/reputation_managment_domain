from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.media import router as media_router
from app.messaging.broker import broker

# Импорт регистрирует subscriber.
import app.messaging.handlers  # noqa


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with broker:
        await broker.start()
        yield


app = FastAPI(
    title="Media Service",
    version="0.1.0",
    lifespan=lifespan,
)


app.include_router(media_router)


@app.get("/health")
async def health():
    return {
        "service": "media-service",
        "status": "ok",
    }
