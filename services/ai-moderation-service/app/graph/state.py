from typing import TypedDict


class ModerationState(TypedDict):
    text: str

    normalized_text: str

    flags: list[str]

    category: str
    violation_probability: float
    confidence: float

    explanation: str
