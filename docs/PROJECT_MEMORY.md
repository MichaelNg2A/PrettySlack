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
- Product direction: Slack-operated workflow automation for creating tracked PrettyLinks-style campaign links.
- Primary user for v1: Michael, with possible use by Connie later.

## Working Conventions

- Use `AGENTS.md` as the entrypoint for agent instructions in this repo.
- Keep project memory in this repository and personal cross-project memory in the private `Operator_Context` repository.
- Prefer explicit, reviewable documentation over implicit chat-only decisions.

## Architecture Notes

- PrettySlack should reduce the manual/executive-function burden of provisioning campaign tracking links from Slack.
- Expected public architecture direction: Slack interaction -> serverless Python service -> link payload generation -> supported PrettyLinks API integration.
- PrettySlack is intentionally not a full Slack-driven control surface for PrettyLinks. Its scope is the basic PrettyLinks lifecycle that PrettySlack needs: add/create, edit/update, and delete/remove PrettyLink records through the supported integration path.
- The initial implementation should make URL/UTM payload generation testable before adding live Slack, AWS, or WordPress/PrettyLinks writes.
- `prettyslack/link_builder.py` is now a pure importable module for target URL construction; human-runnable sample execution lives in `scripts/build_sample_target_url.py`.
- `prettyslack/qr_builder.py` is now a pure importable module for QR artifact generation; human-runnable sample execution lives in `scripts/build_sample_qr_artifacts.py`.
- `prettyslack/prettylinks_create_simulator.py` is a temporary local simulator for PrettyLinks create responses. It validates and reflects PrettySlack's narrow create payload without network calls.
- `prettyslack/prettylinks_client.py` currently exists as a future-facing client boundary and re-exports the create simulator until the real supported PrettyLinks integration is implemented.
- The initial local test convention uses Python's built-in `unittest`, currently run with `python3 -m unittest`.
- Current architecture direction favors small focused modules coordinated inside one application boundary rather than a monolithic all-in-one workflow module.
- Provisional module boundaries currently look like:
  - `workflow_orchestrator.py`: Slack-facing workflow progression, readiness checks, and handoff timing.
  - `link_builder_dispatcher.py`: a thin coordinator that interprets URL/QR/both requests and dispatches the necessary downstream work.
  - `link_builder.py`: pure target URL construction.
  - `qr_builder.py`: QR artifact generation.
  - `prettylinks_create_simulator.py`: temporary local create-response simulator for downstream development.
  - `prettylinks_client.py`: eventual submission to the supported PrettyLinks integration path and receipt of lifecycle status.
  - `link_record_store.py` or similar: DynamoDB persistence for completed PrettySlack-side records.
- The dispatcher direction is intentionally thin: it should call focused helpers for URL building, optional QR generation, PrettyLinks submission, and DynamoDB recording, then return a structured result to the workflow orchestrator.
- Exact module and function names are still provisional and may change as implementation details become clearer.
- Keep provider boundaries explicit enough to support clean integration seams, but public project docs should focus on supported/public API paths.

## UTM And Link Conventions

- Current tracked-link base domain is `cng.bio`.
- PrettySlack should support creating typed URL links, QR links, or a pair of both.
- QR variants conventionally append `_QR` to the PrettyLink slug and set `utm_term=QR`.
- Typed/manual URL variants set `utm_term=URL`.
- `utm_source` identifies where the traffic came from. It is often event-specific or placement-specific and should support guided free entry plus recent-value suggestions.
  - Examples: `VFW_VendorFaire`, `Celebrity_CruiseNight_20250917`, `Business_Card`, `Tesla_Wrap`.
- `utm_medium` identifies the broad channel/context. Treat this as a controlled or suggested list.
  - Default for in-person/print/event material: `event`.
  - Other possible values discussed: `vehicle` for vehicle wrap advertising.
  - Older values like `Paper` and `wrap` existed, but the preferred direction is to normalize them where useful.
- `utm_campaign` identifies the message or campaign bucket. It should support guided free entry plus recent-value suggestions.
  - Examples: `TA_Top10_Flyer`, `AI_Top10_Flyer`, `Groups_Benefits_Flyer`, `Princess_Military_Flyer`, `Royal_Military_Flyer`, `Direct_Link`.
  - Campaign names may use a topic-first pattern so related assets sort together, such as `TA_Top10_Flyer` and future variants like `TA_Top10_Email`.
- `utm_content` identifies the physical or content context.
  - Examples: `Flyer`, `Business_Card`.
- `utm_term` is intentionally used for access method in this project, even though that is non-standard compared with keyword usage.
  - Accepted v1 values: `URL`, `QR`.
- Recent-value memory is desirable for fields that are often reused but not globally standardized, especially `utm_source` and `utm_campaign`.
- RDS is likely overkill for PrettySlack state. DynamoDB is the preferred v1 state store for Slack workflow/session state and durable PrettySlack link records because it is AWS-native, inexpensive at expected scale, and less fragile than shared JSON state in S3.
- S3 is the preferred storage location for generated QR code image artifacts. DynamoDB records should store S3 bucket/key metadata rather than binary QR image data.
- QR image artifacts are generated in memory by `qr_builder.py`; a separate future S3 upload module should upload those bytes and produce the durable S3 metadata.
- QR codes should encode the public PrettyLink URL, such as `https://cng.bio/CN25_Why_QR`, not the UTM-expanded PrettyLinks redirect `target_url`.
- PrettySlack workflow/link state is documented in `docs/WORKFLOW_STATE.md`.
- Workflow state uses `mode` for the requested variants (`typed`, `qr`, or `both`). Durable link records represent one actual PrettyLink and use `access_method` (`URL` or `QR`).
- PrettySlack mirrors PrettyLinks field names where useful, but containers such as `link`, `payload`, and `qr_code` are PrettySlack-owned.
- PrettySlack's supported PrettyLink field surface is intentionally narrow: `slug`, `target_url`, `name`, `description`, and `redirect_type`.
- PrettySlack's default redirect type is currently `307`. Supported redirect type values for local create simulation are `301`, `302`, `307`, and `308`.

## Environment Notes

- The devcontainer installs Python, Node, Git, and the ChatGPT VS Code extension.
- Codespaces is configured to request write access to `MichaelNg2A/Operator_Context` for cross-repository persistent context.
- `.devcontainer/scripts/post-create.sh` uses the Codespaces-granted HTTPS credentials to clone `MichaelNg2A/Operator_Context` into `/workspaces/Operator_Context` after container creation when the repo is accessible and not already present.
- Inherited `devcontainers/images:/src/python` artifacts that do not support PrettySlack should be removed after review. Removed so far: `.npmignore`, `manifest.json`, `history/`, `test-project/`, `.devcontainer/scripts/install-subversion.sh`, and the inherited `setuptools`/`GitPython` pin block in `.devcontainer/Dockerfile`.
- Remaining inherited devcontainer files should be reviewed later for relevance: `.devcontainer/Dockerfile`, `.devcontainer/devcontainer.json`, and `.devcontainer/devcontainer-lock.json`.
- The remaining `.devcontainer/Dockerfile` ImageMagick purge is inherited from `devcontainers/images:/src/python`. On future devcontainer review, check whether `python:3-trixie` still includes ImageMagick and whether the current package still warrants removal for CVE-2019-10131.
- Cleanup principle: keep the development environment working, but remove unused inherited tools/configuration when doing so will not break current or foreseeable workflows. This reduces repository noise and avoids carrying unnecessary security/update surface.
- `poppler-utils` may be installed manually in a Codespace when PDF text extraction is needed; it is not currently part of the repo devcontainer definition.

## Known Constraints

- Personal working preferences should not be mixed into project source-of-truth docs unless they affect project-specific workflow.
- Sensitive data belongs in GitHub Secrets or another secret-management system, not in repository memory files.
