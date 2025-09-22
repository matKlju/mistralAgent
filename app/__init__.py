"""Application package exposing the Mistral agent factory."""

from .agent import create_agent, MistralAgent

__all__ = ["create_agent", "MistralAgent"]
