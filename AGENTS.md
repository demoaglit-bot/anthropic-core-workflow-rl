# AGENTS.md

## Purpose

This project contains a greenfield RL environment that approximates a core Anthropic task-handling workflow. Agents interact with a seeded queue of tasks, inspect state, write drafts, submit responses, and reset the environment deterministically.

## Layout

- `app.py`: local HTTP server, API implementation, and static file serving
- `api/openapi.yaml`: source of truth for the environment API
- `data/seed_state.json`: deterministic seed data and reset baseline
- `templates/index.html`: minimal UI for local inspection
- `static/style.css`: local styling

## Local Commands

- Run server: `python3 app.py`
- Manual validation: open `http://127.0.0.1:8000`, draft a response, submit it, then call reset

## Test Commands

- Manual smoke test for bootstrap:
  - load queue
  - open a task
  - save a draft
  - submit response
  - reset state

## OpenAPI Ownership

Any API change must be reflected in `api/openapi.yaml` before implementation is considered complete.

## Reset / Restore Behavior

- The seed state in `data/seed_state.json` is the canonical restore source.
- `POST /api/reset` restores in-memory state from that seed.
- Every mutating action updates explicit task status fields so the state is replayable and inspectable.

## Agent Rules

- Keep the environment deterministic.
- Preserve a restorable state transition for every action.
- Prefer standard-library Python unless a clear dependency is necessary.
