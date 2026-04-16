# AGENTS.md

## Purpose

This delivery implements a local and deployable RL environment that mimics Anthropic's core chat workflow.

## Architecture

- `app.py` serves the OpenAPI-backed endpoints and the static app.
- `data/seed_state.json` defines the seeded baseline that reset restores.
- `static/` contains the frontend for list, detail, compose, and reset flows.
- `api/openapi.yaml` owns the public environment contract.

## Commands

- Run locally: `python3 app.py`
- Smoke test: `curl http://127.0.0.1:8000/api/state`
- Reset state: `curl -X POST http://127.0.0.1:8000/api/reset`

## Agent Rules

- Keep the OpenAPI contract aligned with the implementation.
- Every user-visible mutation must create an event and remain restorable via reset.
- Preserve seeded entities so demos and evaluations are deterministic.
- Prefer additive changes to the environment state model over ad hoc UI-only behavior.

## Deployment

Deploy the app to Vercel as a Python project or wrap it behind a minimal ASGI/WSGI entrypoint if required by the platform.
