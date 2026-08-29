from fastapi import FastAPI

app = FastAPI(
    title="Media Service",
    version="0.1.0",
)


@app.get("/health")
async def health():
    return {
        "service": "media-service",
        "status": "ok",
    }
