# Mistral Service Generator

A streamlined project for generating service definitions with Mistral and LangChain. The agent combines a service design guide with JSON templates to produce fully wired service flows.

## Features
- Preconfigured `MistralAgent` wrapper (`app/agent.py`) that loads environment secrets via `python-dotenv`.
- Service design guide (`app/SERVICE_DESIGN_GUIDE.md`) distilled from example workflows, plus a machine-readable checklist (`app/SERVICE_CHECKLIST.json`).
- Default contexts and sample question (`app/examples/test_context.json`, `app/examples/sample_service_branching.json`, `app/constants.py`) showcasing linear and branching services.
- Automated UUID regeneration and code-fence stripping to keep saved JSON responses clean (`main.py`).

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
   ```bash
   cp .env.example .env  # if needed
   ```
   Add your `MISTRAL_API_KEY` to `.env` (or export it) so the agent can reach Mistral’s API.

## Generating a Service
All configuration is file-driven. Update the following as needed:
- **System prompt & defaults**: `app/constants.py`
- **Design guide**: `app/SERVICE_DESIGN_GUIDE.md`
- **Checklist**: `app/SERVICE_CHECKLIST.json`
- **Example contexts**: files under `app/examples/` (e.g., `test_context.json`, `sample_service_branching.json`, and the `common*` flows)

Then run:
```bash
python main.py
```
This will:
1. Load the design guide, checklist, and bundled example contexts.
2. Ask the default sample question (also defined in `app/constants.py`).
3. Generate a service JSON response, strip Markdown fences, refresh UUIDs, and save the result to `service_response.json`.
4. Print the normalized JSON to stdout.

## Customising Generation
- **Change the sample prompt**: edit `DEFAULT_SAMPLE_QUESTION` in `app/constants.py`.
- **Swap or edit context**: update JSON files under `app/examples/` and/or the guide.
- **Use a different output file**: update `DEFAULT_OUTPUT_PATH` in `app/constants.py`.
- **Extend helper logic**: adjust `app/prompt_utils.py` or `main.py` if you need additional preprocessing.

## Testing & Validation
Currently the repository focuses on generation. Add unit tests or integration scripts as you extend the agent’s functionality (e.g., verifying JSON schema compliance, checking edge wiring).

## Project Status
The workflow has been tailored for file-based configuration and automated service generation—ready to adapt as you add more templates or refine the guide.
