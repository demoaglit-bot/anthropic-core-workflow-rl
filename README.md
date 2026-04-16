# Anthropic Core Workflow RL Environment

This delivery bootstraps a local RL environment that models a focused slice of Anthropic's core workflow: review tasks in a queue, inspect task context, draft a response, submit it, and reset the environment to a seeded state.

## Scope

- Queue view of seeded tasks
- Detail view for a selected task
- Draft and submit response flow
- Deterministic reset to the original seeded state
- HTTP JSON API defined in `api/openapi.yaml`

## Local Run

```bash
PORT=8016 python3 app.py
```

Then open `http://127.0.0.1:8016`.

## API Surface

- `GET /api/state`
- `GET /api/episode`
- `GET /api/tasks`
- `GET /api/tasks/{task_id}`
- `POST /api/tasks/{task_id}/draft`
- `POST /api/tasks/{task_id}/submit`
- `POST /api/reset`

## Delivery Notes

This is the bootstrap baseline for the full delivery. It is intentionally dependency-light so it can run on a machine without Node tooling.

## Deploy

- Local server: `app.py`
- Vercel entrypoint: `api/index.py`
- Routing: `vercel.json`

## RL Notes

- Observation space: environment metadata, queue state, selected task detail, transition log
- Action space: inspect queue, inspect task, save draft, submit task, reset episode
- Reward hints: positive reward for useful progression, penalty for invalid submission
