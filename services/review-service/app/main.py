from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.reviews import router
from app.messaging.broker import broker

# регистрируем subscriber
import app.messaging.handlers  # noqa


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with broker:
        await broker.start()
        yield


app = FastAPI(
    title="Review Service",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(router)


@app.get("/health")
async def health():
    return {
        "service": "review-service",
        "status": "ok",
    }
