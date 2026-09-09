from pydantic import BaseModel


class ModerationRequest(BaseModel):
    text: str


class ModerationResponse(BaseModel):
    category: str
    violation_probability: float
    confidence: float
    explanation: str
    flags: list[str]
