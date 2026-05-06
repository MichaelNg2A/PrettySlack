# Current State

This file tracks the current working state of the project.

## Current Focus

- Extend the first PrettySlack code slices around tested URL, QR artifact, and PrettyLinks create-response simulation.
- Prepare to implement the persistence/store layer and dispatcher that will coordinate URL building, PrettyLinks create confirmation, QR generation, and durable record writing.
- Keep project-local memory separate from personal cross-project context.

## Recent Changes

- Added the first `prettyslack/link_builder.py` code slice to build `target_url` values from workflow fixture data.
- Added `tests/test_link_builder.py` and `tests/__init__.py` so the target URL builder is covered by an initial `unittest` suite.
- Added `scripts/build_sample_target_url.py` and moved the sample/demo runner out of `prettyslack/link_builder.py` so the module now stays focused on importable logic.
- Documented the target URL builder policy in `docs/WORKFLOW_STATE.md`.
- Added `prettyslack/qr_builder.py` to generate QR image artifacts from a public PrettyLink hostname and QR slug.
- Added `tests/test_qr_builder.py` so QR URL construction, image artifact generation, format selection, unsupported formats, and minimum raster dimensions are covered by `unittest`.
- Added `scripts/build_sample_qr_artifacts.py` to write sample QR SVG/PNG/JPEG artifacts under `/tmp/prettyslack_sample_qr`.
- Added `requirements.txt` with `qrcode[pil]` as the initial QR generation dependency.
- Added `prettyslack/prettylinks_create_simulator.py` as a temporary local PrettyLinks create-response simulator.
- Added `prettyslack/prettylinks_client.py` as a future-facing PrettyLinks client boundary that currently re-exports the create simulator.
- Added `tests/test_prettylinks_create_simulator.py` to cover simulated create success, defaulting, validation errors, slug collisions, self-redirect rejection, and allowed redirect types.
- Added `scripts/simulate_prettylinks_create.py` to print a simulated PrettyLinks create response from the sample workflow fixture.
- Confirmed the supported PrettySlack PrettyLink field surface is intentionally narrow: `slug`, `target_url`, `name`, `description`, and `redirect_type`.
- Removed inherited devcontainer image-source artifacts that are not needed by PrettySlack: `.npmignore`, `manifest.json`, `history/`, and `test-project/`.
- Removed `README_Original.md` after completing the inherited devcontainer artifact review.
- Added the ChatGPT VS Code extension to the devcontainer configuration.
- Removed the inherited Subversion source-build script and its `.devcontainer/Dockerfile` invocation because PrettySlack does not need Subversion and the CVE workaround applied to an unused tool.
- Removed the inherited `setuptools==78.1.1` and `gitpython==3.1.41` pin block from `.devcontainer/Dockerfile` because PrettySlack does not currently need global `GitPython`, and modern Python packaging does not require a global `setuptools` install for the current dependency set.
- Added `AGENTS.md` and project memory docs to support continuity across sessions.
- Added Codespaces access to the private `Operator_Context` repository.
- Added explicit memory update policy and session-closeout guidance to `AGENTS.md`.
- Captured initial PrettySlack product direction and UTM conventions in `docs/PROJECT_MEMORY.md`.
- Added an initial PrettySlack design document in `docs/DESIGN.md`.
- Added `docs/WORKFLOW_STATE.md` to document temporary workflow state and durable PrettySlack link records.
- Added JSON fixtures for workflow input and generated URL/QR link records.
- Chose DynamoDB over S3 JSON documents for v1 workflow/session state and durable PrettySlack link records.

## Next Steps

- Implement a persistence/store layer for durable PrettySlack link records.
- Implement a thin dispatcher that coordinates URL building, PrettyLinks create simulation/client calls, QR generation after PrettyLinks create confirmation, and record persistence.
- Generate PrettyLinks-ready URL and QR draft link records matching the sample durable fixtures where that still belongs outside the dispatcher/store work.
- Decide whether to keep the demo scripts as pure sample runners or broaden them into more general local helpers.
- Keep live Slack, AWS Lambda, DynamoDB, S3 uploads, and WordPress/PrettyLinks writes out of the first builder slices.
- After a useful first PrettySlack code slice is committed, review the remaining inherited devcontainer files for relevance: `.devcontainer/Dockerfile`, `.devcontainer/devcontainer.json`, and `.devcontainer/devcontainer-lock.json`.
- Re-check whether the remaining `.devcontainer/Dockerfile` ImageMagick purge is still needed: current upstream `python:3-trixie` inherits ImageMagick through `buildpack-deps:trixie`, but this should be revisited as upstream images and Debian packages change.

## Open Questions

- Exact live PrettyLinks API authentication and response details.
- Whether simulated edit/delete responses will be needed before live PrettyLinks API access is available.
- Whether Slack v1 should use slash commands, bot messages in a dedicated channel, or both.
- Which recent-value fields should be persisted first beyond `utm_source` and `utm_campaign`.
- Whether recent-value suggestions should live in DynamoDB alongside workflow/link records or remain a separate lightweight state shape.
- Whether QR artifacts should be deleted from S3, retained, or managed through lifecycle rules when PrettySlack records are deleted.
