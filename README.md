# Anthropic Core Workflow RL Environment

This delivery bootstraps a production-oriented RL environment for Anthropic's core workflow. The environment models a chat-oriented task loop with seeded conversations, restorable state transitions, and an OpenAPI-defined backend surface.

## Stack

- Python 3 standard library HTTP server
- Static HTML, CSS, and JavaScript frontend
- JSON file-backed seeded environment state
- OpenAPI contract in `api/openapi.yaml`

## Local Run

```bash
python3 app.py
```

Then open `http://127.0.0.1:8000`.

## Current Slice

- Conversation list view
- Thread detail view
- Draft editing and send transition
- Reset to seeded baseline
- Environment event log and reward hints

## Project Layout

- `app.py`: local server and API implementation
- `static/`: UI assets
- `data/seed_state.json`: seeded restorable environment state
- `api/openapi.yaml`: API contract
- `AGENTS.md`: delivery-specific operating instructions
