# AGENTS.md Reader Notes

This file is for human readers who notice `AGENTS.md` and want to understand why it exists.

`AGENTS.md` is used as the entry point for project guidance consumed by AI-enhanced SDLC tools. It tells those tools which project memory files to review at the start of a session, how to treat project documentation, and how to avoid mixing project facts with private personal context.

## Repository Memory Structure

PrettySlack keeps project-specific context in this repository:

- [docs/PROJECT_MEMORY.md](docs/PROJECT_MEMORY.md): durable project context, conventions, and architecture notes.
- [docs/CURRENT_STATE.md](docs/CURRENT_STATE.md): current focus, recent changes, next steps, and open questions.
- [docs/DECISIONS.md](docs/DECISIONS.md): notable decisions and their rationale.
- [docs/WORKFLOW_STATE.md](docs/WORKFLOW_STATE.md): data-shape notes for PrettySlack workflow state and durable link records.

This split into multiple memory/state files is a human-driven project convention, chosen in the absence of a clear industry-wide standard for persistent AI-assisted SDLC context. The goal is to make the project easier to re-enter across fresh development sessions without depending on chat history.

## Private Cross-Repository Context

The instructions also allow an optional private context repository named `Operator_Context`.

That private repository is intentionally separate from this project repository. Its purpose is to hold cross-project working preferences and reusable operator context that should not automatically become part of a public or project-specific codebase.

This structure is intentional: project facts stay with the project, while personal working context stays private.

- Project architecture, rationale, status, and decisions belong in this repository.
- Personal or cross-project working context belongs in the private context repository.
- If the two ever conflict, project-specific documentation in this repository wins for PrettySlack work.

This split is meant to keep public project artifacts understandable on their own while still allowing AI-assisted tooling to use private context when it is available in the local workspace.

For GitHub Codespaces, access to that private repository is configured through [.devcontainer/devcontainer.json](.devcontainer/devcontainer.json).

## Privacy And Security Notes

The memory files are not a place for secrets.

`AGENTS.md` explicitly instructs tools not to store secrets, tokens, credentials, or private keys in memory files. That applies to both this repository and the optional private context repository.

The intent is to preserve useful engineering context while keeping sensitive material out of committed documentation.

## AI-Assisted Workflow

This repository is being developed with AI-assisted SDLC tooling, including Codex from OpenAI.

The presence of `AGENTS.md` should not be read as a sign that generated changes are accepted automatically. The working model for this repository is human-reviewed, incremental, and deliberately paced. AI tools may propose or apply changes, but the project direction and accepted content remain subject to human review.
