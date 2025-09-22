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

## Usage
The repository includes a lightweight agent wrapper in `app/agent.py`:

```python
from app import create_agent

agent = create_agent()
print(agent.run("Summarise the LangChain toolkit."))
```

The helper loads `MISTRAL_API_KEY` from your environment, builds a LangChain chain,
and returns the agent's response as a string. Pass `context="..."` to supply extra
background information when needed.

## Next Steps
- Add FastAPI routes (e.g., in `app/main.py`) to serve the agent over HTTP.
- Extend tests and tooling as the agent matures.

## Project Status
Initial scaffold committed with Git so you can track iterative improvements with confidence.
