# Decisions

This file records notable project decisions and why they were made.

## 2026-04-23 - Use `AGENTS.md` as the repo entrypoint

- Decision: Use `AGENTS.md` as the primary Codex-discoverable instruction file for this repository.
- Why: `AGENTS.md` is the documented convention Codex can use as an instruction entrypoint, while other memory files remain normal supporting documents.

## 2026-04-23 - Split project memory from private personal context

- Decision: Keep project-specific memory in this repo and use a separate private repository for personal cross-project context.
- Why: This creates a cleaner boundary between shared project knowledge and personal working preferences, and reduces accidental exposure of more personal context.

## 2026-04-23 - Use `Operator_Context` as the private repo name

- Decision: Use `Operator_Context` as the private cross-project context repository name.
- Why: The name is explicit, durable, and better aligned with long-term working context than a generic name like `LLM`.
