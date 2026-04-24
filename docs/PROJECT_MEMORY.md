# Project Memory

This file stores durable, project-specific context that should survive across sessions.

## Purpose

- Capture architecture, conventions, and constraints for this repository.
- Preserve rationale that would otherwise be lost in chat history.
- Keep this focused on stable facts, not temporary work notes.

## Repository Context

- Repository name: `PrettySlack`
- Environment: GitHub Codespaces with a repo-level devcontainer
- Current editor integration expectation: VS Code in a Codespace

## Working Conventions

- Use `AGENTS.md` as the entrypoint for agent instructions in this repo.
- Keep project memory in this repository and personal cross-project memory in the private `Operator_Context` repository.
- Prefer explicit, reviewable documentation over implicit chat-only decisions.

## Architecture Notes

- Add stable architectural decisions and system constraints here.

## Environment Notes

- The devcontainer installs Python, Node, Git, and the ChatGPT VS Code extension.
- Codespaces is configured to request write access to `MichaelNg2A/Operator_Context` for cross-repository persistent context.

## Known Constraints

- Personal working preferences should not be mixed into project source-of-truth docs unless they affect project-specific workflow.
- Sensitive data belongs in GitHub Secrets or another secret-management system, not in repository memory files.
