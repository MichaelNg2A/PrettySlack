# PrettySlack

PrettySlack is an early-stage workflow automation project for creating PrettyLinks shortened, UTM-tracked campaign links from Slack.

The current design target is a small Python service that can collect link details, generate UTM-tagged destination URLs, prepare typed URL and QR variants, and eventually submit those links to a WordPress/PrettyLinks integration.

This repository is intentionally moving in small, reviewable steps. The current work is focused on data contracts and fixtures before live Slack, AWS Lambda, DynamoDB, S3, QR image generation, or WordPress writes are added.

## Current Implementation

The first working Python module is in place:

- [prettyslack/link_builder.py](prettyslack/link_builder.py): builds a final `target_url` from `base_target_url`, UTM payload values, and an explicit `utm_term`.

At the moment, the code focuses on URL construction only. Slack handling, Lambda entrypoints, DynamoDB reads/writes, QR image generation, and WordPress/PrettyLinks submission are still planned follow-on pieces.

## Current Shape

- [prettyslack/](prettyslack/): Python package for PrettySlack code.
- [docs/DESIGN.md](docs/DESIGN.md): product and architecture direction.
- [docs/WORKFLOW_STATE.md](docs/WORKFLOW_STATE.md): workflow-state and durable link-record shapes.
- [fixtures/](fixtures/): sample JSON data used to make the data contracts concrete.
- [docs/CURRENT_STATE.md](docs/CURRENT_STATE.md): current focus, recent changes, and next steps.
- [docs/PROJECT_MEMORY.md](docs/PROJECT_MEMORY.md): durable project context and conventions.
- [AGENTS.md](AGENTS.md): entry point for persistent project guidance used by AI-enhanced SDLC tools.
- [AGENTS_Readme.md](AGENTS_Readme.md): human-readable explanation of the agent guidance structure.

## AI-Assisted Development

Codex from OpenAI is being used during development of this repository. Its role is collaborative: proposed changes are reviewed, discussed, and intentionally accepted by a human before they become part of the project.

That means this repo is expected to mature at human review speed, not at raw AI generation speed. The goal is to keep the design understandable, explainable, and maintainable rather than to maximize the volume of generated code.

## Original README

The original README copied from the Python devcontainer image source is preserved at [README_Original.md](README_Original.md).
