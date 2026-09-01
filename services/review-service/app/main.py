from fastapi import FastAPI

app = FastAPI(
    title="Review Service",
    version="0.1.0",
)


@app.get("/health")
async def health():
    return {
        "service": "review-service",
        "status": "ok",
    }
