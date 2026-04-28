# PrettySlack Design

## Purpose

PrettySlack is a Slack-guided workflow tool for creating tracked campaign links using the PrettyLinks WordPress plugin.

The main goal is to make the correct link-provisioning workflow easy enough that it happens on time, without requiring the operator to remember UTM conventions, PrettyLinks fields, QR variants, or manual WordPress admin steps.

PrettySlack is primarily an operator workflow automation project. The first real use case is marketing attribution, but the design should demonstrate production-minded platform habits: clear boundaries, testable logic, secure handling of credentials, and modest architecture that fits the problem size.

## Problem Statement

The current workflow is manual and easy to miss:

1. Identify a marketing piece that needs a short URL.
2. Decide the destination URL and UTM values.
3. Decide the public slug.
4. Check whether the slug already exists.
5. Log into WordPress.
6. Open the PrettyLinks admin interface.
7. Enter one or more PrettyLinks records.
8. Generate a QR code when needed.

The failure mode is not lack of knowledge. The failure mode is process friction: a low-frequency, detail-heavy workflow that is easy to delay or forget.

PrettySlack should turn that into a guided Slack flow that produces correct payloads and, eventually, creates the links directly.

## Scope

### v0.5 Proof Of Direction

v0.5 should prove the core link-building logic without depending on live Slack, AWS, WordPress, or PrettyLinks access.

It should:

- Accept structured link request inputs.
- Generate typed URL and/or QR variants.
- Generate encoded target URLs with UTM parameters.
- Produce a PrettyLinks-shaped payload for each link.
- Validate the known project conventions.
- Store enough example fixtures and tests to make the behavior reviewable.

v0.5 does not need to call external APIs.

### v1.0 Useful Workflow

v1.0 should create links through the supported public integration path.

It should:

- Run from Slack, preferably in a dedicated channel or guided interaction.
- Deploy as a small serverless service, likely AWS Lambda behind an HTTP endpoint.
- Create PrettyLinks records through the official PrettyLinks API.
- Generate QR SVG artifacts for QR variants.
- Persist recent UTM values for low-friction reuse.
- Handle secrets outside the repository.

### Deferred Capabilities

Later versions may support retargeting existing PrettyLinks records. This is useful when links must be created before an event-specific landing page exists: the initial target can point to the default link-in-bio page, then later be updated to an event-specific path when that page is ready.

This is lower priority than reliable link creation because the manual workaround is tolerable for small batches.

## UTM Model

PrettySlack uses UTM values as a practical attribution system for small-business marketing workflows. The conventions are intentionally optimized for the current reporting questions rather than strict generic marketing taxonomy.

### Fields

- `utm_source`: where the traffic came from.
  Examples: `VFW_VendorFaire`, `Celebrity_CruiseNight_20250917`, `Business_Card`, `Tesla_Wrap`.
- `utm_medium`: broad channel or context.
  Default: `event` for in-person, print, booth, flyer, and similar material.
  Other expected value: `vehicle` for wrapped-vehicle advertising.
- `utm_campaign`: message, material theme, or campaign bucket.
  Examples: `TA_Top10_Flyer`, `AI_Top10_Flyer`, `Groups_Benefits_Flyer`, `Princess_Military_Flyer`, `Royal_Military_Flyer`, `Direct_Link`, `Celebrity_2024`.
- `utm_term`: access method.
  Accepted v1 values: `URL`, `QR`.
- `utm_content`: format or placement context.
  Examples: `Flyer`, `Business_Card`, `Vehicle_Wrap`.

### Intentional Deviations

- `utm_term` is used for access method (`URL` vs `QR`) instead of keyword tracking.
- `utm_campaign` may identify a specific persuasive material or message rather than a broad advertising campaign.
- `utm_content` is used for format/context, not always the unique creative identifier.

This gives the operator useful answers:

- Where did the person encounter the link?
- Which message or material likely caught their attention?
- Did they type the URL or scan the QR code?
- What kind of physical or digital item carried the link?

## Link Variants

PrettySlack should support three creation modes:

- Typed URL only: create one link with `utm_term=URL`.
- Typed URL plus QR: create a typed link with `utm_term=URL`, a QR link with `utm_term=QR`, and a QR SVG for the QR link.
- QR only: create a QR link with `utm_term=QR` and a QR SVG, usually when the typed link already exists.

QR variants conventionally append `_QR` to the slug.

Each link request must specify a destination target URL or path before UTM parameters are added. The destination might be the default link-in-bio page, or it might be an event-specific landing page such as `/Alaska2026/` or `/20250405VFWFaire/`.

Example pair:

```text
Slug: CN25_Why
Target: https://cng.bio/Alaska2026/?utm_source=Celebrity_CruiseNight_20250917&utm_medium=event&utm_campaign=TA_Top10_Flyer&utm_term=URL&utm_content=Flyer

Slug: CN25_Why_QR
Target: https://cng.bio/Alaska2026/?utm_source=Celebrity_CruiseNight_20250917&utm_medium=event&utm_campaign=TA_Top10_Flyer&utm_term=QR&utm_content=Flyer
```

## Interaction Model

The preferred Slack experience is guided, not command-syntax-heavy.

PrettySlack should ask for or confirm:

- Destination URL or path.
- Final target URL after UTM parameters are applied.
- PrettyLink slug.
- Whether to create typed URL, QR, or both.
- `utm_source`.
- `utm_medium`, defaulting to `event`.
- `utm_campaign`.
- `utm_content`.
- Redirect type, defaulting to a temporary redirect unless changed.

For low-frequency use, the tool should emphasize recognition over memorization:

- Show recent values first for fields that are often reused.
- Allow free entry when recent values do not apply.
- Confirm the final generated links before creating external records.

## Persistence

RDS is not justified for the first version.

Preferred persistence direction:

- v0.5: local JSON fixtures for recent-value behavior and tests.
- v1.0: a small JSON state document in S3 for recent values and lightweight configuration.

Likely recent-value fields:

- `utm_source`
- `utm_campaign`
- `utm_content`

`utm_medium` and `utm_term` should be more controlled and need less free-form memory.

## Architecture

Expected public architecture:

```text
Slack
  -> HTTP endpoint
  -> AWS Lambda Python service
  -> link builder and validator
  -> PrettyLinks API client
  -> PrettyLinks records on WordPress
```

Internal code should separate:

- Slack request parsing and response formatting.
- Guided workflow state.
- Link and UTM modeling.
- PrettyLinks payload generation.
- External provider clients.
- Recent-value persistence.

The link-building core should be testable without Slack, AWS, network access, or WordPress credentials.

## Security Notes

- Do not commit Slack secrets, WordPress credentials, API tokens, or private keys.
- Use AWS Secrets Manager or SSM Parameter Store for deployed credentials.
- Validate Slack requests before processing.
- Keep logs useful but avoid leaking credentials, tokens, or full sensitive payloads.
- Prefer least-privilege IAM for Lambda, S3 state access, and secret reads.
- Public documentation should describe supported public integration paths and avoid private deployment-specific details.

## Open Questions

- Exact PrettyLinks API payload shape, authentication method, and update behavior.
- Whether Slack v1 should use slash commands, bot messages in a dedicated channel, or both.
- Whether slug existence checks belong in v1 or a later milestone.
- Whether retargeting existing links should support one-at-a-time edits, batch updates, or both.
- Whether QR SVG generation should happen inside Lambda or be returned as a generated artifact from a separate step.
- Which redirect type should be the default: `302`, `307`, or configurable per link.
- Whether recent-value state should be global, per Slack user, or per Slack channel.
