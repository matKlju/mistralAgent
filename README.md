# Mistral Agent Starter

A minimal project scaffold for experimenting with an AI agent powered by [Mistral](https://docs.mistral.ai), [LangChain](https://python.langchain.com), and a few complementary tools.

## Features
- Python-focused `.gitignore` and dependency lock-in via `requirements.txt`.
- Suggested libraries for building conversational agents with Mistral + LangChain.
- Basic FastAPI skeleton recommendation for exposing the agent as a service.

## Getting Started
1. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure credentials**
   - Copy `.env.example` to `.env` (create one if needed).
   - Add your `MISTRAL_API_KEY` and any other secrets.

## Next Steps
- Build an agent entry point, e.g., `app/agent.py`, that wires LangChain with the `mistralai` client.
- Add FastAPI routes (e.g., in `app/main.py`) to serve the agent over HTTP.
- Extend tests and tooling as the agent matures.

## Project Status
Initial scaffold committed with Git so you can track iterative improvements with confidence.
