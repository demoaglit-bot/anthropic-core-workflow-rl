# Product Requirements Document

## Target Workflow

This delivery models a focused slice of Anthropic's core task-handling workflow. The environment starts with a seeded queue, allows the agent to inspect task context, draft a response, submit it, and reset the episode deterministically.

## Environment Goal

Provide a local, restorable RL environment where an agent can learn to progress from queued work to a valid submitted response while preserving inspectable state transitions.

## User Persona And Task Objective

- Persona: internal operator or evaluation harness driving a support-and-analysis task queue
- Objective: inspect the right task, write a useful draft, and submit a final response on the seeded target task

## Boundaries And Exclusions

- Included: queue view, task detail, drafting, submission, reset, reward hints, transition logging
- Excluded in bootstrap: multi-user auth, external model calls, persistent database, deployment wiring

## Seeded Starting State

- Three seeded tasks with distinct categories and priorities
- One target task designated for episode scoring
- Empty drafts and empty final responses
- Deterministic reward profile in seed state

## Reset And Restore Strategy

- Canonical seed source: `data/seed_state.json`
- `POST /api/reset` restores all in-memory state from seed and increments `reset_count`
- Every mutation appends an explicit transition event with timestamp and reward value

## Observation Space

- Environment metadata
- Queue summary for all tasks
- Full target-task detail including status, context, draft, final response, and history
- Transition log for the current episode

## Action Space

- Read queue state
- Read task detail
- Save draft for a task
- Submit a task
- Reset the environment

## Reward Model

- `draft_saved`: `0.2`
- `successful_submit`: `1.0`
- `submit_without_draft`: `-0.5`

## Termination Conditions

- Successful submission of the target task
- External evaluator can also impose a max-step cap

## API Surface And OpenAPI Ownership

The API surface is defined in `api/openapi.yaml` and must remain the source of truth for any change.

- `GET /api/state`
- `GET /api/episode`
- `GET /api/tasks`
- `GET /api/tasks/{task_id}`
- `POST /api/tasks/{task_id}/draft`
- `POST /api/tasks/{task_id}/submit`
- `POST /api/reset`

## Backend And Data Model

- Runtime: standard-library Python HTTP server
- Seed store: JSON file in `data/seed_state.json`
- Restore semantics: full reload from seed for reset, in-memory updates for episode progression

## Required Repository Structure

- `README.md`
- `AGENTS.md`
- `PRD.md`
- `api/openapi.yaml`
- `app.py`
- `data/seed_state.json`
- `templates/index.html`
- `static/style.css`

## Local Development

Run `python3 app.py` and open `http://127.0.0.1:8000`.

## Deployment Plan

Primary target remains Vercel, but the bootstrap currently optimizes for local execution on a machine without Node, `gh`, or `vercel` on PATH.

## Instrumentation Requirements

- Transition log with timestamps and rewards
- Queue and task state observable through JSON endpoints

## Evaluation Scenarios

- Save a valid draft and verify task status transitions to `drafted`
- Submit a drafted task and verify status transitions to `submitted`
- Attempt submission without a draft and verify penalty path
- Reset and verify deterministic return to seed state

## QA Plan

- Manual API smoke test
- Browser smoke test of queue, detail, draft, submit, and reset flow
- Recorded walkthrough of the local UI once runtime validation is available

## Major Risks And Open Questions

- Google Docs publication, Vercel deployment, and GitHub PR creation require tools not available in the current execution environment
- Persistent database-backed restore semantics remain future work beyond bootstrap
