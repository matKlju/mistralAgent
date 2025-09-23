"""Helper functions for loading and formatting prompt inputs."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from langchain_core.prompts import ChatPromptTemplate

from .constants import (
    DEFAULT_CONTEXT_PATHS,
    EXAMPLES_DIR,
    SERVICE_CHECKLIST,
    SERVICE_DESIGN_GUIDE,
)

PROMPT_MESSAGES = [
    ("system", "{system_prompt}"),
    ("human", "{context_block}\n\nUser question:\n{question}"),
]


def load_context_from_file(path: Path, *, include_guide: bool = True) -> str:
    """Read a context file from disk, optionally prefixing the guide."""

    try:
        content = path.read_text(encoding="utf-8")
    except OSError:
        return merge_with_guide(
            f"Context file '{path}' could not be read.", include_guide=include_guide
        )
    return merge_with_guide(content, include_guide=include_guide)


def load_default_context(*, include_guide: bool = True) -> str:
    """Load the shared default contexts shipped with the repository."""

    contexts: list[str] = []
    seen_paths = set()

    def append_path(path: Path) -> None:
        if path in seen_paths:
            return
        seen_paths.add(path)
        try:
            content = path.read_text(encoding="utf-8")
        except OSError:
            content = f"Context file '{path.name}' could not be read."
        contexts.append(content.strip())

    for path in DEFAULT_CONTEXT_PATHS:
        append_path(path)

    if EXAMPLES_DIR.exists():
        for path in sorted(EXAMPLES_DIR.glob("*.json")):
            append_path(path)

    combined = "\n\n=== Example Separator ===\n\n".join(contexts)
    return merge_with_guide(combined, include_guide=include_guide)


def build_prompt_template() -> ChatPromptTemplate:
    """Return the base prompt template shared by all agent instances."""

    return ChatPromptTemplate.from_messages(PROMPT_MESSAGES)


def format_context(context: Optional[str]) -> str:
    """Format optional context into the template-friendly block."""

    if context and context.strip():
        return f"Context provided:\n{context.strip()}"
    return "No additional context provided."


def merge_with_guide(content: str, *, include_guide: bool = True) -> str:
    """Prepend the design guide and checklist when requested."""

    if not include_guide:
        return content.strip()

    sections: list[str] = []
    if SERVICE_DESIGN_GUIDE.strip():
        sections.append(SERVICE_DESIGN_GUIDE.strip())
    if SERVICE_CHECKLIST.strip() and SERVICE_CHECKLIST.strip() != "{}":
        sections.append("Service Checklist:\n" + SERVICE_CHECKLIST.strip())

    if sections:
        prefix = "\n\n---\n\n".join(sections)
        return f"{prefix}\n\n---\n\n{content.strip()}"
    return content.strip()
