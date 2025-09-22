"""Convenience abstractions for interacting with Mistral via LangChain."""

from __future__ import annotations

import os
from typing import Optional

from dotenv import load_dotenv
from langchain_community.chat_models import ChatMistralAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables early so the API key is discoverable.
load_dotenv()

DEFAULT_MODEL = "codestral-2501"
DEFAULT_SYSTEM_PROMPT = (
    "You are a helpful AI assistant that provides concise, relevant answers. "
    "Use the supplied context when it is available, and otherwise rely on your "
    "general knowledge."
)


class MistralAgent:
    """Lightweight wrapper around the LangChain Mistral chat model."""

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
        self._prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "{system_prompt}"),
                (
                    "human",
                    "{context_block}\n\n" "User question:\n{question}",
                ),
            ]
        )
        self._chain = self._prompt | self._model | StrOutputParser()

    def run(self, question: str, *, context: Optional[str] = None) -> str:
        """Send a prompt to the agent and return the text response."""
        context_block = (
            f"Context provided:\n{context.strip()}"
            if context and context.strip()
            else "No additional context provided."
        )
        return self._chain.invoke(
            {
                "system_prompt": self._system_prompt,
                "context_block": context_block,
                "question": question,
            }
        )


def create_agent(**kwargs: object) -> MistralAgent:
    """Factory helper for callers that prefer a function interface."""

    return MistralAgent(**kwargs)
