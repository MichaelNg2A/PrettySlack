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

## 2026-04-30 - Use DynamoDB for PrettySlack workflow and link state

- Decision: Use DynamoDB as the preferred v1 state store for Slack workflow/session state and durable PrettySlack link records.
- Why: Lambda is stateless, and PrettySlack needs small durable state records between Slack interactions. DynamoDB is AWS-native, inexpensive at expected scale, supports key-based workflow records cleanly, and is less fragile than maintaining shared JSON state documents in S3.

## 2026-04-30 - Store QR image artifacts in S3

- Decision: Store generated QR code image files in S3 and store only S3 bucket/key metadata in PrettySlack link records.
- Why: QR images are generated artifacts, not workflow fields. Keeping binary/image data out of DynamoDB keeps records small and makes SVG/PNG/JPEG outputs easier to manage.

## 2026-05-05 - Use a create-specific PrettyLinks simulator before live integration

- Decision: Add `prettyslack/prettylinks_create_simulator.py` as a temporary local simulator for PrettyLinks create responses, with `prettyslack/prettylinks_client.py` kept as the future-facing client boundary.
- Why: The simulator unblocks the persistence/store layer and dispatcher without depending on live WordPress/PrettyLinks access. Naming it as a create simulator keeps the temporary artifact explicit and leaves room for possible edit/delete simulators if they are needed later.

## 2026-05-05 - Keep PrettySlack's PrettyLink field surface narrow

- Decision: PrettySlack supports only the basic PrettyLink lifecycle fields it needs: `slug`, `target_url`, `name`, `description`, and `redirect_type`.
- Why: PrettySlack is a workflow automation tool for creating and maintaining campaign links, not a full Slack-driven PrettyLinks administration surface.
