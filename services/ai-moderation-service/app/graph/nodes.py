import re

from app.graph.state import ModerationState


def normalize_text(
    state: ModerationState,
) -> dict:

    text = state["text"]

    text = text.lower().strip()

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return {
        "normalized_text": text,
    }


def check_rules(
    state: ModerationState,
) -> dict:

    text = state["normalized_text"]

    flags: list[str] = []

    spam_markers = {
        "telegram",
        "телеграм",
        "whatsapp",
        "ватсап",
        "переходи по ссылке",
    }

    toxic_markers = {
        "идиот",
        "тупой",
        "урод",
    }

    if any(
        marker in text
        for marker in spam_markers
    ):
        flags.append("possible_spam")

    if any(
        marker in text
        for marker in toxic_markers
    ):
        flags.append("possible_toxicity")

    return {
        "flags": flags,
    }


def route_after_rules(
    state: ModerationState,
) -> str:

    if "possible_toxicity" in state["flags"]:
        return "rule_violation"

    return "model"


def mock_model(
    state: ModerationState,
) -> dict:

    flags = state["flags"]

    if "possible_spam" in flags:
        return {
            "category": "spam",
            "violation_probability": 0.70,
            "confidence": 0.78,
            "explanation": (
                "Text contains possible "
                "external contact or spam markers"
            ),
        }

    return {
        "category": "clean",
        "violation_probability": 0.05,
        "confidence": 0.95,
        "explanation": (
            "No significant violation "
            "signals detected"
        ),
    }


def rule_violation(
    state: ModerationState,
) -> dict:

    return {
        "category": "toxicity",
        "violation_probability": 0.97,
        "confidence": 0.98,
        "explanation": (
            "Explicit toxicity marker detected"
        ),
    }


def postprocess(
    state: ModerationState,
) -> dict:

    probability = max(
        0.0,
        min(
            1.0,
            state["violation_probability"],
        ),
    )

    confidence = max(
        0.0,
        min(
            1.0,
            state["confidence"],
        ),
    )

    return {
        "violation_probability": probability,
        "confidence": confidence,
    }
