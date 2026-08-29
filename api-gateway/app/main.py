import os

import httpx
from fastapi import FastAPI, HTTPException

app = FastAPI(
    title="API Gateway",
    version="0.1.0",
)

REVIEW_SERVICE_URL = os.getenv(
    "REVIEW_SERVICE_URL",
    "http://review-service:8001",
)

MEDIA_SERVICE_URL = os.getenv(
    "MEDIA_SERVICE_URL",
    "http://media-service:8002",
)


@app.get("/health")
async def health():
    return {
        "service": "api-gateway",
        "status": "ok",
    }


@app.get("/api/v1/reviews/health")
async def review_health():
    try:
        async with httpx.AsyncClient(timeout=3) as client:
            response = await client.get(
                f"{REVIEW_SERVICE_URL}/health"
            )

        response.raise_for_status()

        return response.json()

    except httpx.HTTPError:
        raise HTTPException(
            status_code=503,
            detail="Review Service unavailable",
        )


@app.get("/api/v1/media/health")
async def media_health():
    try:
        async with httpx.AsyncClient(timeout=3) as client:
            response = await client.get(
                f"{MEDIA_SERVICE_URL}/health"
            )

        response.raise_for_status()

        return response.json()

    except httpx.HTTPError:
        raise HTTPException(
            status_code=503,
            detail="Media Service unavailable",
        )
