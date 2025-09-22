"""Project-wide constant definitions for the Mistral agent."""

from __future__ import annotations

from pathlib import Path

DEFAULT_SYSTEM_PROMPT = (
    "You are an AI service-developer focused on generating new services. "
    "Use the provided context to understand the existing service structure and keep your designs "
    "aligned with those workflow rules. The user’s regular prompt describes the service to build, "
    ""
    "and your final answer must be valid JSON that encodes the resulting service definition."
)

DEFAULT_CONTEXT_PATH = Path(__file__).with_name("test_context.json")
try:
    DEFAULT_CONTEXT = DEFAULT_CONTEXT_PATH.read_text(encoding="utf-8")
except OSError:
    DEFAULT_CONTEXT = "No bundled test context available."
SERVICE_DESIGN_GUIDE_PATH = Path(__file__).with_name("SERVICE_DESIGN_GUIDE.md")
try:
    SERVICE_DESIGN_GUIDE = SERVICE_DESIGN_GUIDE_PATH.read_text(encoding="utf-8")
except OSError:
    SERVICE_DESIGN_GUIDE = "Service design guide not found."
DEFAULT_SAMPLE_QUESTION = "Create a service that returns the current national holidays of the current year, for Estonia. Use this api : https://openholidaysapi.org/swagger/v1/swagger.json"
DEFAULT_OUTPUT_PATH = Path(__file__).resolve().parent.parent / "service_response.json"
