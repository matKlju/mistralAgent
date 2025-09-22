"""Helper functions for loading and formatting prompt inputs."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from langchain_core.prompts import ChatPromptTemplate

from .constants import DEFAULT_CONTEXT, DEFAULT_CONTEXT_PATH

PROMPT_MESSAGES = [
    ("system", "{system_prompt}"),
    ("human", "{context_block}\n\nUser question:\n{question}"),
]


def load_context_from_file(path: Path) -> str:
    """Read a context file from disk."""

    return path.read_text(encoding="utf-8")


def load_default_context() -> str:
    """Load the shared default context shipped with the repository."""

    return DEFAULT_CONTEXT


def build_prompt_template() -> ChatPromptTemplate:
    """Return the base prompt template shared by all agent instances."""

    return ChatPromptTemplate.from_messages(PROMPT_MESSAGES)


def format_context(context: Optional[str]) -> str:
    """Format optional context into the template-friendly block."""

    if context and context.strip():
        return f"Context provided:\n{context.strip()}"
    return "No additional context provided."
