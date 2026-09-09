from langgraph.graph import (
    END,
    START,
    StateGraph,
)

from app.graph.nodes import (
    check_rules,
    mock_model,
    normalize_text,
    postprocess,
    route_after_rules,
    rule_violation,
)
from app.graph.state import ModerationState


builder = StateGraph(
    ModerationState
)

builder.add_node(
    "normalize",
    normalize_text,
)

builder.add_node(
    "rules",
    check_rules,
)

builder.add_node(
    "model",
    mock_model,
)

builder.add_node(
    "rule_violation",
    rule_violation,
)

builder.add_node(
    "postprocess",
    postprocess,
)


builder.add_edge(
    START,
    "normalize",
)

builder.add_edge(
    "normalize",
    "rules",
)

builder.add_conditional_edges(
    "rules",
    route_after_rules,
    {
        "rule_violation": "rule_violation",
        "model": "model",
    },
)

builder.add_edge(
    "rule_violation",
    "postprocess",
)

builder.add_edge(
    "model",
    "postprocess",
)

builder.add_edge(
    "postprocess",
    END,
)


moderation_graph = builder.compile()
