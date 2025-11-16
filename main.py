"""Entry point for generating a service response using predefined configuration."""

from __future__ import annotations

import json
import time
import uuid
from datetime import datetime

from app import create_agent
from app.constants import DEFAULT_OUTPUT_PATH, DEFAULT_SAMPLE_QUESTION
from app.prompt_utils import load_default_context


def strip_code_fences(text: str) -> str:
    """Remove surrounding Markdown code fences if present."""

    stripped = text.strip()
    if not stripped.startswith("```"):
        return stripped

    lines = stripped.splitlines()
    if not lines:
        return stripped

    first = lines[0]
    if first.startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].startswith("```"):
        lines = lines[:-1]
    return "\n".join(lines).strip()


def ensure_uuid_node_ids(text: str) -> str:
    """Rewrite node IDs (and associated edges) to fresh UUID4 values."""

    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return text

    if not isinstance(payload, dict):
        return text

    nodes = payload.get("nodes")
    if not isinstance(nodes, list):
        return text

    id_mapping: dict[str, str] = {}
    for node in nodes:
        if not isinstance(node, dict):
            continue
        old_id = node.get("id")
        new_id = str(uuid.uuid4())
        node["id"] = new_id
        if isinstance(old_id, str):
            id_mapping[old_id] = new_id

        data = node.get("data")
        if isinstance(data, dict):
            assign_elements = data.get("assignElements")
            if isinstance(assign_elements, list):
                for element in assign_elements:
                    if isinstance(element, dict):
                        element["id"] = str(uuid.uuid4())

    edges = payload.get("edges")
    if isinstance(edges, list):
        for edge in edges:
            if not isinstance(edge, dict):
                continue
            source = edge.get("source")
            target = edge.get("target")
            if isinstance(source, str) and source in id_mapping:
                edge["source"] = id_mapping[source]
            if isinstance(target, str) and target in id_mapping:
                edge["target"] = id_mapping[target]

    return json.dumps(payload, ensure_ascii=False, indent=2)


def main() -> None:
    """Generate a service response using default configuration values."""

    print("Generating...")
    agent = create_agent()
    context_value = load_default_context()
    start_time = time.perf_counter()
    response = agent.run(DEFAULT_SAMPLE_QUESTION, context=context_value)
    cleaned_response = strip_code_fences(response)
    normalized_response = ensure_uuid_node_ids(cleaned_response)
    DEFAULT_OUTPUT_PATH.write_text(normalized_response, encoding="utf-8")
    duration = time.perf_counter() - start_time
    timestamp = datetime.now().strftime("%H:%M")
    print(f"Service ready in {duration:.2f}s at {timestamp}.")


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
