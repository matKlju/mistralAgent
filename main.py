"""Command-line entry point for the Mistral agent."""

from __future__ import annotations

import argparse
import json
import sys
import uuid
from pathlib import Path
from typing import Sequence

from app import create_agent
from app.constants import DEFAULT_OUTPUT_PATH, DEFAULT_SAMPLE_QUESTION
from app.prompt_utils import load_context_from_file, load_default_context


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    """Parse CLI arguments for agent execution."""

    parser = argparse.ArgumentParser(
        prog="main.py",
        description="Run a question against the Mistral agent",
    )
    parser.add_argument(
        "question",
        nargs="?",
        help="Question to send to the agent. Defaults to a built-in smoke test when omitted.",
    )
    parser.add_argument(
        "--context",
        help="Optional context block to provide extra background for the agent.",
    )
    parser.add_argument(
        "--context-file",
        type=Path,
        help=(
            "Path to a file whose contents should be supplied as context. "
            "Defaults to the bundled test_context.json when omitted."
        ),
    )
    parser.add_argument(
        "--model",
        help="Override the default model identifier configured in the agent.",
    )
    parser.add_argument(
        "--system-prompt",
        dest="system_prompt",
        help="Override the default system prompt.",
    )
    parser.add_argument(
        "--api-key",
        dest="api_key",
        help="Provide a Mistral API key without relying on environment variables.",
    )
    parser.add_argument(
        "--output-file",
        type=Path,
        help=(
            "Path to write the agent response JSON. "
            "Defaults to service_response.json in the project root."
        ),
    )
    return parser.parse_args(argv)


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


def main(argv: Sequence[str] | None = None) -> int:
    """Execute the CLI workflow and print the agent response."""

    args = parse_args(argv or sys.argv[1:])

    question = args.question or DEFAULT_SAMPLE_QUESTION

    agent_kwargs = {}
    if args.api_key:
        agent_kwargs["api_key"] = args.api_key
    if args.model:
        agent_kwargs["model"] = args.model
    if args.system_prompt:
        agent_kwargs["system_prompt"] = args.system_prompt

    try:
        agent = create_agent(**agent_kwargs)
        if args.context_file:
            context_value = load_context_from_file(args.context_file)
        elif args.context is not None:
            context_value = args.context
        else:
            context_value = load_default_context()
        response = agent.run(question, context=context_value)
        cleaned_response = strip_code_fences(response)
        normalized_response = ensure_uuid_node_ids(cleaned_response)
        output_path = args.output_file or DEFAULT_OUTPUT_PATH
        output_path.write_text(normalized_response, encoding="utf-8")
    except Exception as exc:  # pragma: no cover - simple CLI guard
        print(f"Error running agent: {exc}", file=sys.stderr)
        return 1

    print(normalized_response)
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    raise SystemExit(main())
