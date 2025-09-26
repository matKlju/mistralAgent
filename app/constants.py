"""Project-wide constant definitions for the Mistral agent."""

from __future__ import annotations

from pathlib import Path

DEFAULT_SYSTEM_PROMPT = (
    "You are an AI service-developer focused on generating new services. "
    "Study the design guide, checklist, and all provided service examples before planning your response. "
    "Mirror their structure, naming, and branching conventions. The user’s regular prompt describes the "
    "service to build, and your final answer must be valid JSON that encodes the resulting service definition "
    "while satisfying every checklist rule."
)

EXAMPLES_DIR = Path(__file__).with_name("examples")

DEFAULT_CONTEXT_FILENAMES = [
    "test_context.json",
    "sample_service_branching.json",
]

DEFAULT_CONTEXT_PATHS = [EXAMPLES_DIR / name for name in DEFAULT_CONTEXT_FILENAMES]

SERVICE_DESIGN_GUIDE_PATH = Path(__file__).with_name("SERVICE_DESIGN_GUIDE.md")

try:
    SERVICE_DESIGN_GUIDE = SERVICE_DESIGN_GUIDE_PATH.read_text(encoding="utf-8")
except OSError:
    SERVICE_DESIGN_GUIDE = "Service design guide not found."
SERVICE_CHECKLIST_PATH = Path(__file__).with_name("SERVICE_CHECKLIST.json")

try:
    SERVICE_CHECKLIST = SERVICE_CHECKLIST_PATH.read_text(encoding="utf-8")
except OSError:
    SERVICE_CHECKLIST = "{}"

# DEFAULT_SAMPLE_QUESTION = "Create a service that returns the current national holidays of the current year, for Estonia, from start of the year to the current day. Use this api : https://openholidaysapi.org/swagger/v1/swagger.json"

DEFAULT_SAMPLE_QUESTION = "Create a service that Provides information for 5 most recent active initiatives. Use this api example : https://rahvaalgatus.ee/initiatives?for=parliament&phase=sign&signedSince=2020-01-01&order=-signatureCount&signingEndsAt=2015-06-18T13%3A37%3A42Z&limit=5"


DEFAULT_OUTPUT_PATH = Path(__file__).resolve().parent.parent / "service_response.json"
