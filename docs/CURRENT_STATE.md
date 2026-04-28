# Current State

This file tracks the current working state of the project.

## Current Focus

- Define PrettySlack as a real product rather than continuing from inherited devcontainer image scaffolding.
- Review and refine the first `docs/DESIGN.md` draft before writing the first app code.
- Keep project-local memory separate from personal cross-project context.

## Recent Changes

- Added the ChatGPT VS Code extension to the devcontainer configuration.
- Added `AGENTS.md` and project memory docs to support continuity across sessions.
- Added Codespaces access to the private `Operator_Context` repository.
- Added explicit memory update policy and session-closeout guidance to `AGENTS.md`.
- Captured initial PrettySlack product direction and UTM conventions in `docs/PROJECT_MEMORY.md`.
- Added an initial PrettySlack design document in `docs/DESIGN.md`.

## Next Steps

- Review `docs/DESIGN.md` for accuracy, especially UTM semantics, v0.5/v1 scope, and Slack interaction assumptions.
- Build the first milestone around testable URL/UTM payload generation before live Slack, AWS Lambda, or PrettyLinks API integration.
- Decide how to handle recent-value suggestions for hand-entered UTM fields, likely local JSON first and S3 later.

## Open Questions

- Exact PrettyLinks API payload shape and authentication requirements.
- Whether Slack v1 should use slash commands, bot messages in a dedicated channel, or both.
- Which recent-value fields should be persisted first beyond `utm_source` and `utm_campaign`.
