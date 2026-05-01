# Current State

This file tracks the current working state of the project.

## Current Focus

- Define the first PrettySlack data contracts before writing the first app code.
- Prepare to implement a small Python builder that reads workflow-state JSON and generates PrettyLinks-ready URL/QR link records.
- Keep project-local memory separate from personal cross-project context.

## Recent Changes

- Added the ChatGPT VS Code extension to the devcontainer configuration.
- Added `AGENTS.md` and project memory docs to support continuity across sessions.
- Added Codespaces access to the private `Operator_Context` repository.
- Added explicit memory update policy and session-closeout guidance to `AGENTS.md`.
- Captured initial PrettySlack product direction and UTM conventions in `docs/PROJECT_MEMORY.md`.
- Added an initial PrettySlack design document in `docs/DESIGN.md`.
- Added `docs/WORKFLOW_STATE.md` to document temporary workflow state and durable PrettySlack link records.
- Added JSON fixtures for workflow input and generated URL/QR link records.
- Chose DynamoDB over S3 JSON documents for v1 workflow/session state and durable PrettySlack link records.

## Next Steps

- Build the first Python milestone around reading `fixtures/sample_workflow_state.json` and generating `target_url` values.
- Generate PrettyLinks-ready URL and QR link records matching the sample durable fixtures.
- Keep live Slack, AWS Lambda, DynamoDB, S3, QR image generation, and WordPress/PrettyLinks writes out of the first code slice.

## Open Questions

- Exact PrettyLinks API payload shape and authentication requirements.
- Whether Slack v1 should use slash commands, bot messages in a dedicated channel, or both.
- Which recent-value fields should be persisted first beyond `utm_source` and `utm_campaign`.
- Whether recent-value suggestions should live in DynamoDB alongside workflow/link records or remain a separate lightweight state shape.
