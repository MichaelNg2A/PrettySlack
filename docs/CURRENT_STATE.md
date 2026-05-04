# Current State

This file tracks the current working state of the project.

## Current Focus

- Extend the first PrettySlack code slice around tested URL construction.
- Prepare to implement generation of PrettyLinks-ready URL/QR draft link records from workflow-state JSON.
- Keep project-local memory separate from personal cross-project context.

## Recent Changes

- Added the first `prettyslack/link_builder.py` code slice to build `target_url` values from workflow fixture data.
- Added `tests/test_link_builder.py` and `tests/__init__.py` so the target URL builder is covered by an initial `unittest` suite.
- Added `scripts/build_sample_target_url.py` and moved the sample/demo runner out of `prettyslack/link_builder.py` so the module now stays focused on importable logic.
- Documented the target URL builder policy in `docs/WORKFLOW_STATE.md`.
- Removed inherited devcontainer image-source artifacts that are not needed by PrettySlack: `.npmignore`, `manifest.json`, `history/`, and `test-project/`.
- Updated `README_Original.md` so its `history` link points to the pinned upstream `devcontainers/images:/src/python/history` source instead of the removed local copy.
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

- Generate PrettyLinks-ready URL and QR draft link records matching the sample durable fixtures.
- Decide whether to keep the demo script as a pure sample runner or broaden it into a more general local helper.
- Keep live Slack, AWS Lambda, DynamoDB, S3, QR image generation, and WordPress/PrettyLinks writes out of the first code slice.
- After a useful first PrettySlack code slice is committed, review the remaining inherited devcontainer files for relevance: `.devcontainer/Dockerfile`, `.devcontainer/devcontainer.json`, `.devcontainer/devcontainer-lock.json`, and `.devcontainer/scripts/install-subversion.sh`.
- If the remaining devcontainer files are confirmed relevant and inherited cleanup is complete, consider removing `README_Original.md`.

## Open Questions

- Exact PrettyLinks API payload shape and authentication requirements.
- Whether Slack v1 should use slash commands, bot messages in a dedicated channel, or both.
- Which recent-value fields should be persisted first beyond `utm_source` and `utm_campaign`.
- Whether recent-value suggestions should live in DynamoDB alongside workflow/link records or remain a separate lightweight state shape.
- Whether PrettySlack needs Subversion at all; if not, remove `.devcontainer/scripts/install-subversion.sh` and its Dockerfile references during a later devcontainer cleanup.
