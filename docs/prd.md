# PRD: Anthropic Core Workflow RL Environment

## Introduction

Default target chosen from the delivery instructions: Anthropic's core workflow. This delivery models a chat-centric task loop that feels like a compact signed-in product slice, implemented as a greenfield repo-first RL environment under `~/Projects/anthropic-aglit/deliveries/anthropic-core-workflow-rl`.

## Product / Workflow Summary

The environment represents a user working through high-priority research operations requests inside a conversation-driven workspace. The first slice focuses on viewing seeded threads, reviewing thread history, drafting a response, sending the response, and restoring the environment to a deterministic baseline.

## Environment Goal

Create a locally runnable and deployable RL environment with restorable state transitions, auditable events, and a stable API surface managed through OpenAPI.

## User Persona and Task Objective

- Persona: Research Operations Analyst
- Task objective: Resolve urgent internal requests accurately and efficiently while maintaining deterministic environment state.

## Boundaries and Exclusions

Included:
- Thread list, detail, draft, send, reset, reward/event log
- Seeded conversation state
- Restorable runtime state
- OpenAPI-defined environment API

Excluded from the first slice:
- Authentication
- Multi-user collaboration
- File attachments
- Model execution backends
- Production persistence beyond seeded JSON runtime state

## Reset Conditions and Seeded Starting States

The environment ships with seeded threads, messages, and a persona record in `data/seed_state.json`. `POST /api/reset` restores `data/runtime_state.json` to the seeded baseline, clearing draft/send mutations and returning the reward log to the initial seed event.

## State Model and Restore / Replay Strategy

Meaningful actions:
- View state: reads the current environment snapshot.
- Save draft: updates `thread.draft` and appends a `save_draft` event.
- Send reply: appends a new assistant message, clears nothing by default, and records a `send_reply` event with positive reward.
- Reset: overwrites runtime state from seed state.

Replay / restore semantics:
- Runtime state is stored as a full JSON snapshot.
- Reward and event history is explicit in `events[]`.
- Reset is authoritative and deterministic.

## Observation Space

The agent observes:
- Persona metadata
- Thread list with status and message counts
- Active thread messages
- Draft content
- Event and reward log

## Action Space

- Select thread
- Save draft
- Send reply
- Reset environment
- Read current state via API

## Reward Model

- `save_draft`: small positive shaping reward (`0.2`)
- `send_reply`: larger positive reward (`1.0`)
- `reset`: neutral reward, but restores evaluation determinism

Future versions should add rubric-based task completion scoring and penalties for malformed replies.

## Termination Conditions

Episode termination can occur when:
- A required reply is sent successfully
- The environment is manually reset
- A max-step threshold is reached in the evaluator

## API Surface / OpenAPI Ownership

All environment APIs are defined in `api/openapi.yaml`, which is the source of truth for:
- `GET /api/state`
- `POST /api/reset`
- `POST /api/save-draft`
- `POST /api/send-reply`

Implementation changes must update the OpenAPI spec in the same change.

## Backend / Data Model Requirements

- `data/seed_state.json` holds deterministic seeded entities
- `data/runtime_state.json` is created on demand and stores mutable runtime state
- Event entries must include action type, reward, and explanatory detail
- Future migration path: move JSON state into SQLite or Postgres while preserving reset semantics

## Required Repository Structure

- `README.md`
- `AGENTS.md`
- `api/openapi.yaml`
- `app.py`
- `data/seed_state.json`
- `static/index.html`
- `static/styles.css`
- `static/app.js`
- `docs/prd.md`

## Local Development and Launch

Run locally with:

```bash
python3 app.py
```

Default port is `8000`; set `PORT` to override. Open `http://127.0.0.1:$PORT`.

## Hosting / Deployment Plan

Default deployment target is Vercel. Because the current machine lacks the `vercel` CLI on PATH, deployment should proceed through the Vercel web flow or by adding the minimal adapter Vercel expects for Python hosting.

## Instrumentation / Data Requirements

- Capture each mutation in `events[]`
- Preserve reward values with the action record
- Keep seed and runtime state separate for deterministic resets
- Future work: add evaluator-visible step counters and hidden grading fields

## Evaluation Scenarios

- Read seeded thread and identify the urgent request
- Draft a reply without sending it
- Send the reply and verify message count increments
- Reset and verify the environment returns to seeded state

## QA Plan

- Launch locally
- Validate seeded render in the browser
- Perform a real send transition
- Perform a real reset transition
- Record a walkthrough video showing both transitions
- Deploy and repeat a smoke validation against the deployed URL

## Risks and Open Questions

- Deployment adapter for Vercel still needs implementation and validation
- GitHub PR creation depends on either `gh` installation or web-based repo access
- Google Docs publication still depends on active Docs auth scope in the current session
- The first slice uses file-backed state rather than a real database
