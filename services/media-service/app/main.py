from fastapi import FastAPI

from app.api.media import router as media_router


app = FastAPI(
    title="Media Service",
    version="0.1.0",
)


app.include_router(media_router)


@app.get("/health")
async def health():
    return {
        "service": "media-service",
        "status": "ok",
    }
