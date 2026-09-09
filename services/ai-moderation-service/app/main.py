from fastapi import FastAPI

from app.graph.graph import moderation_graph
from app.schemas import (
    ModerationRequest,
    ModerationResponse,
)


app = FastAPI(
    title="AI Moderation Service",
    version="0.1.0",
)


@app.post(
    "/moderate",
    response_model=ModerationResponse,
)
async def moderate(
    request: ModerationRequest,
):
    result = await moderation_graph.ainvoke(
        {
            "text": request.text,
            "normalized_text": "",
            "flags": [],
            "category": "",
            "violation_probability": 0.0,
            "confidence": 0.0,
            "explanation": "",
        }
    )

    return ModerationResponse(
        category=result["category"],
        violation_probability=(
            result["violation_probability"]
        ),
        confidence=result["confidence"],
        explanation=result["explanation"],
        flags=result["flags"],
    )


@app.get("/health")
async def health():
    return {
        "service": "ai-moderation-service",
        "status": "ok",
    }
