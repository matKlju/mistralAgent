"""Convenience abstractions for interacting with Mistral via LangChain.

Features
- Loads Mistral credentials from environment variables or overrides.
- Builds a reusable prompt template with configurable system prompt.
- Provides a simple `.run()` API that injects optional context blocks.
"""

from __future__ import annotations

import os
from typing import Optional

from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.output_parsers import StrOutputParser

from .constants import DEFAULT_SYSTEM_PROMPT
from .prompt_utils import append_language_directive, build_prompt_template, format_context

# Load environment variables early so the API key is discoverable.
load_dotenv()

DEFAULT_MODEL = "codestral-2501"


class MistralAgent:
    """LangChain chat wrapper that manages prompts, model, and execution."""

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        model: str = DEFAULT_MODEL,
        system_prompt: str = DEFAULT_SYSTEM_PROMPT,
    ) -> None:
        self._api_key = api_key or os.getenv("MISTRAL_API_KEY")
        if not self._api_key:
            raise RuntimeError(
                "Missing Mistral API key. Set the MISTRAL_API_KEY environment variable "
                "or pass api_key explicitly."
            )

        self._system_prompt = system_prompt
        self._model = ChatMistralAI(model=model, mistral_api_key=self._api_key)
        self._prompt = build_prompt_template()
        self._chain = self._prompt | self._model | StrOutputParser()

    def run(self, question: str, *, context: Optional[str] = None) -> str:
        """Send a prompt to the agent and return the text response."""
        context_block = format_context(context)
        augmented_question, _language = append_language_directive(question)
        return self._chain.invoke(
            {
                "system_prompt": self._system_prompt,
                "context_block": context_block,
                "question": augmented_question,
            }
        )


def create_agent(**kwargs: object) -> MistralAgent:
    """Factory helper for callers that prefer a function interface."""

    return MistralAgent(**kwargs)
