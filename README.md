# PrettySlack

PrettySlack is an early-stage workflow automation project for creating PrettyLinks shortened, UTM-tracked campaign links from Slack.

The current design target is a small Python service that can collect link details, generate UTM-tagged destination URLs, prepare typed URL and QR variants, generate QR image artifacts, and eventually submit those links to a supported WordPress/PrettyLinks integration.

This repository is intentionally moving in small, reviewable steps. The current work is focused on data contracts, fixtures, URL construction, QR artifact generation, and local PrettyLinks response simulation before live Slack, AWS Lambda, DynamoDB, S3 uploads, or WordPress writes are added.

## Current Implementation

The first working Python modules are in place, along with an initial test/demo spine:

- [prettyslack/link_builder.py](prettyslack/link_builder.py): builds a final `target_url` from `base_target_url`, UTM payload values, and an explicit `utm_term`.
- [prettyslack/qr_builder.py](prettyslack/qr_builder.py): builds the public PrettyLink URL encoded into a QR code and returns SVG, PNG, and JPEG image artifacts in memory.
- [prettyslack/prettylinks_create_simulator.py](prettyslack/prettylinks_create_simulator.py): simulates a PrettyLinks create response for the narrow PrettySlack-supported field surface.
- [prettyslack/prettylinks_client.py](prettyslack/prettylinks_client.py): temporary future-facing client boundary that currently re-exports the create simulator.
- [tests/test_link_builder.py](tests/test_link_builder.py): validates the current target URL builder behavior with focused unit tests.
- [tests/test_qr_builder.py](tests/test_qr_builder.py): validates QR URL construction, QR image artifact generation, format selection, unsupported formats, and minimum raster output size.
- [tests/test_prettylinks_create_simulator.py](tests/test_prettylinks_create_simulator.py): validates simulated PrettyLinks create success and validation responses.
- [scripts/build_sample_target_url.py](scripts/build_sample_target_url.py): runs the sample workflow fixture through the builder and prints the resulting URL.
- [scripts/build_sample_qr_artifacts.py](scripts/build_sample_qr_artifacts.py): runs the sample workflow fixture through the QR builder and writes local sample artifacts under `/tmp/prettyslack_sample_qr`.
- [scripts/simulate_prettylinks_create.py](scripts/simulate_prettylinks_create.py): runs the sample workflow fixture through target URL construction and prints a simulated PrettyLinks create response.
- [requirements.txt](requirements.txt): declares the initial QR generation dependency, `qrcode[pil]`.

At the moment, the code focuses on URL construction, QR artifact generation, and local PrettyLinks create-response simulation only. Slack handling, Lambda entrypoints, DynamoDB reads/writes, S3 uploads, and live WordPress/PrettyLinks submission are still planned follow-on pieces.

## Current Shape

- [prettyslack/](prettyslack/): Python package for PrettySlack code.
- [tests/](tests/): Python unit tests for the current code slices.
- [scripts/](scripts/): small human-runnable demo/helper scripts.
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
