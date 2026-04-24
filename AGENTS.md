# Agent Instructions

This repository uses `AGENTS.md` as the entrypoint for project guidance.

## Start Here

At the beginning of a new session, review these files if they exist:

1. `docs/PROJECT_MEMORY.md`
2. `docs/CURRENT_STATE.md`
3. `docs/DECISIONS.md`

If a private cross-repository context repo is available in the workspace at `/workspaces/Operator_Context`, also review:

1. `/workspaces/Operator_Context/AGENTS.md`
2. Any files referenced from that repo's `AGENTS.md`

## Source of Truth

- Project-specific architecture, rationale, status, and decisions belong in this repository.
- The private `Operator_Context` repository is for personal working preferences and cross-project context.
- If local project docs and private context conflict, prefer this repository for project decisions and implementation details.

## Memory Hygiene

- Do not store secrets, tokens, credentials, or private keys in any memory file.
- Keep memory docs concise and curated.
- Prefer updating durable facts after they are confirmed, not while they are still speculative.
- Treat the private context repo as intentional shared memory. Do not rewrite it casually.

## Update Rules

- Update `docs/CURRENT_STATE.md` when priorities or in-flight work materially change.
- Update `docs/PROJECT_MEMORY.md` when durable architecture or workflow conventions become established.
- Update `docs/DECISIONS.md` when a notable decision is made and the reason should be preserved.
- If asked to update the private context repo, make focused edits and preserve the distinction between personal preferences and project facts.

## Memory Update Policy

- Prefer suggesting project-memory updates before writing them.
- Do not silently update `docs/PROJECT_MEMORY.md`, `docs/CURRENT_STATE.md`, or `docs/DECISIONS.md` with durable conclusions unless the user asked for the update or confirmed it.
- Mechanical or clearly requested factual updates are fine.
- If a useful memory update is identified during work, propose it explicitly instead of assuming it should be written.
