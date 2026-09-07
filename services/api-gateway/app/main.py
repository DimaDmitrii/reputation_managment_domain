import os

import httpx
from fastapi import FastAPI, HTTPException


from app.schemas.media import MediaUploadCreate

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


@app.post(
    "/api/v1/media/uploads",
    status_code=201,
)
async def create_media_upload(
    data: MediaUploadCreate,
):
    try:
        async with httpx.AsyncClient(
            timeout=5
        ) as client:

            response = await client.post(
                f"{MEDIA_SERVICE_URL}/media/uploads",
                json=data.model_dump(),
            )

    except httpx.RequestError:
        service_not_available("Media Service")

    if response.status_code >= 400:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.json().get(
                "detail",
                "Media Service error",
            ),
        )

    return response.json()


@app.post(
    "/api/v1/media/{media_id}/complete"
)
async def complete_media_upload(
    media_id: str,
):
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.post(
                f"{MEDIA_SERVICE_URL}/media/{media_id}/complete"
            )
    except httpx.RequestError:
        service_not_available("Media Service")

    if response.status_code >= 400:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.json().get(
                "detail",
                "Media Service error",
            ),
        )

    return response.json()


def service_not_available(servicename: str):
    clear_servicename = servicename.replace("service", "")
    clear_servicename = clear_servicename.replace("Service", "")
    raise HTTPException(
        status_code=503,
        detail=f"{clear_servicename} Service unavailable",
    )
