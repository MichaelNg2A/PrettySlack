# PrettySlack Workflow State

This document describes the expected shape of a completed PrettySlack workflow item before it is converted into PrettyLinks payloads.

The first implementation should treat this as an application-level contract, not a DynamoDB-enforced schema. DynamoDB will store the workflow as an item with typed attributes, and `boto3` will hand Lambda code a Python dictionary with this general shape.

## Purpose

PrettySlack collects link details through a guided workflow. Once the required answers are present, the link builder should read the workflow state and produce one or more PrettyLinks-ready payloads.

The workflow state should use PrettyLinks field names where the concepts map directly. PrettySlack-specific names should be used only where PrettySlack has an intermediate concept that PrettyLinks does not.

## Key Naming Decision

- `base_target_url`: the landing page URL before UTM parameters are added.
- `target_url`: the final PrettyLinks redirect target after PrettySlack adds UTM parameters.

PrettyLinks should only receive `target_url`. PrettySlack uses `base_target_url` while generating typed URL and QR variants.

## Expected Shape

```json
{
  "workflow_id": "wf_20260430_cn25_why",
  "status": "ready_for_payload",
  "step": "build_payload",
  "mode": "both",
  "answers": {
    "slug": "CN25_Why",
    "base_target_url": "https://cng.bio/Alaska2026/",
    "name": "CN25 Why",
    "description": "Celebrity cruise night Top 10 flyer",
    "redirect_type": "307",
    "track_me": true,
    "nofollow": false,
    "sponsored": false,
    "param_forwarding": false,
    "utm_source": "Celebrity_CruiseNight_20250917",
    "utm_medium": "event",
    "utm_campaign": "TA_Top10_Flyer",
    "utm_content": "Flyer"
  },
  "created_at": "2026-04-30T00:00:00Z",
  "updated_at": "2026-04-30T00:05:00Z",
  "expires_at": 1770077100
}
```

## Top-Level Fields

- `workflow_id`: unique identifier for the Slack-guided workflow.
- `status`: lifecycle state for the workflow. For payload generation, the expected value is currently `ready_for_payload`.
- `step`: current workflow step. For payload generation, this should indicate that collection is complete.
- `mode`: which link variants to generate.
  - `typed`: typed URL variant only.
  - `qr`: QR variant only.
  - `both`: typed URL and QR variants.
- `answers`: collected fields used to generate PrettyLinks payloads.
- `created_at`: ISO 8601 timestamp for workflow creation.
- `updated_at`: ISO 8601 timestamp for the last workflow update.
- `expires_at`: Unix timestamp used for DynamoDB TTL cleanup.

## Answer Fields

These fields are expected inside `answers`.

- `slug`: base PrettyLink slug. QR variants append `_QR`.
- `base_target_url`: landing page URL before UTM parameters are added.
- `name`: PrettyLinks display name.
- `description`: PrettyLinks description.
- `redirect_type`: PrettyLinks redirect type, expected to be configurable. Initial examples use `307`.
- `track_me`: whether PrettyLinks tracking should be enabled.
- `nofollow`: whether the link should be marked nofollow.
- `sponsored`: whether the link should be marked sponsored.
- `param_forwarding`: whether PrettyLinks parameter forwarding should be enabled.
- `utm_source`: where the traffic came from.
- `utm_medium`: broad channel or context.
- `utm_campaign`: message, material theme, or campaign bucket.
- `utm_content`: format or placement context.

PrettySlack generates `utm_term` from the selected variant:

- typed URL variant: `utm_term=URL`
- QR variant: `utm_term=QR`

## Generated Payload Direction

Given the workflow above and `mode` set to `both`, PrettySlack should produce two payloads:

- one using `slug=CN25_Why` and a generated `target_url` with `utm_term=URL`
- one using `slug=CN25_Why_QR` and a generated `target_url` with `utm_term=QR`

The generated payloads should use `target_url`, not `base_target_url`.

