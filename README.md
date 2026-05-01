# PrettySlack

PrettySlack is an early-stage workflow automation project for creating PrettyLinks shortened, UTM-tracked campaign links from Slack.

The current design target is a small Python service that can collect link details, generate UTM-tagged destination URLs, prepare typed URL and QR variants, and eventually submit those links to a WordPress/PrettyLinks integration.

This repository is intentionally moving in small, reviewable steps. The current work is focused on data contracts and fixtures before live Slack, AWS Lambda, DynamoDB, S3, QR image generation, or WordPress writes are added.

## Current Shape

- [docs/DESIGN.md](docs/DESIGN.md): product and architecture direction.
- [docs/WORKFLOW_STATE.md](docs/WORKFLOW_STATE.md): workflow-state and durable link-record shapes.
- [fixtures/](fixtures/): sample JSON data used to make the data contracts concrete.
- [AGENTS.md](AGENTS.md): entry point for persistent project guidance used by AI-enhanced SDLC tools.
- [AGENTS_Readme.md](AGENTS_Readme.md): human-readable explanation of the agent guidance structure.

## AI-Assisted Development

Codex from OpenAI is being used during development of this repository. Its role is collaborative: proposed changes are reviewed, discussed, and intentionally accepted by a human before they become part of the project.

That means this repo is expected to mature at human review speed, not at raw AI generation speed. The goal is to keep the design understandable, explainable, and maintainable rather than to maximize the volume of generated code.

## Original README

The original README copied from the Python devcontainer image source is preserved at [README_Original.md](README_Original.md).
