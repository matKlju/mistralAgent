"""Command-line entry point for the Mistral agent."""

from __future__ import annotations

import argparse
import sys
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
        output_path = args.output_file or DEFAULT_OUTPUT_PATH
        output_path.write_text(cleaned_response, encoding="utf-8")
    except Exception as exc:  # pragma: no cover - simple CLI guard
        print(f"Error running agent: {exc}", file=sys.stderr)
        return 1

    print(cleaned_response)
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    raise SystemExit(main())
