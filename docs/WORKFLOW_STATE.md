# PrettySlack Workflow And Link State

This document describes two related PrettySlack data shapes:

- workflow state: temporary state while Slack is collecting or reviewing a request
- link record: durable PrettySlack state after an individual PrettyLink has been created

These are application-level contracts, not DynamoDB-enforced schemas. DynamoDB stores typed attributes, and `boto3` will hand Lambda code Python dictionary-like data with these shapes.

## Naming Decisions

The field names below are PrettySlack field names. PrettySlack should mirror PrettyLinks names where the concepts map directly, but several containers and workflow fields are PrettySlack-owned.

- `target_url`: the final PrettyLinks redirect target after PrettySlack adds UTM parameters.
- `base_target_url`: the landing page URL before UTM parameters are added.
- `payload`: PrettySlack-owned UTM data used to generate `target_url`.
- `link`: PrettySlack-owned container for the link fields PrettySlack collects or stores.
- `mode`: workflow-level creation request: `typed`, `qr`, or `both`.
- `access_method`: single-link record value: `URL` or `QR`.

`mode` belongs to a workflow request. A durable link record should represent one actual PrettyLink, so it uses `access_method` instead.

## Workflow State

Workflow state is used while PrettySlack is still collecting fields, generating link output, or waiting for approval.

Workflow state is pre-variant. It should usually contain the base slug and shared request fields, not the final QR slug, `target_url`, generated `utm_term`, or QR artifact details. Those belong to generated payloads or durable link records.

```json
{
  "workflow_id": "wf_20260430_cn25_why",
  "status": "ready_for_payload",
  "step": "build_payload",
  "mode": "both",
  "link": {
    "slug": "CN25_Why",
    "base_target_url": "https://cng.bio/Alaska2026/",
    "name": "CN25 Why",
    "description": "Celebrity cruise night Top 10 flyer",
    "redirect_type": "307"
  },
  "payload": {
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

### Workflow Fields

- `workflow_id`: unique identifier for the Slack-guided workflow.
- `status`: lifecycle state for the workflow. For payload generation, the expected value is currently `ready_for_payload`.
- `step`: current workflow step. For payload generation, this should indicate that collection is complete.
- `mode`: which link variants to generate.
  - `typed`: typed URL variant only.
  - `qr`: QR variant only.
  - `both`: typed URL and QR variants.
- `link`: collected link fields used to generate PrettyLinks payloads.
- `payload`: UTM fields used to generate PrettyLinks `target_url` values.
- `created_at`: ISO 8601 timestamp for workflow creation.
- `updated_at`: ISO 8601 timestamp for the last workflow update.
- `expires_at`: Unix timestamp used for DynamoDB TTL cleanup of temporary workflow state.

## Link Record

A link record is PrettySlack's durable record of one individual PrettyLink after creation. A typed URL and QR pair should become two link records, not one `both` record.

```json
{
  "link_id": "psl_20260430_cn25_why_url",
  "workflow_id": "wf_20260430_cn25_why",
  "status": "created",
  "access_method": "URL",
  "link": {
    "slug": "CN25_Why",
    "base_target_url": "https://cng.bio/Alaska2026/",
    "target_url": "https://cng.bio/Alaska2026/?utm_source=Celebrity_CruiseNight_20250917&utm_medium=event&utm_campaign=TA_Top10_Flyer&utm_term=URL&utm_content=Flyer",
    "name": "CN25 Why",
    "description": "Celebrity cruise night Top 10 flyer",
    "redirect_type": "307"
  },
  "payload": {
    "utm_source": "Celebrity_CruiseNight_20250917",
    "utm_medium": "event",
    "utm_campaign": "TA_Top10_Flyer",
    "utm_term": "URL",
    "utm_content": "Flyer"
  },
  "created_at": "2026-04-30T00:05:00Z",
  "updated_at": "2026-04-30T00:05:00Z",
  "deleted_at": null
}
```

### Link Record Fields

- `link_id`: PrettySlack-owned durable record identifier. This is not intended to be a PrettyLinks database ID.
- `workflow_id`: source workflow that produced the link record.
- `status`: PrettySlack-side lifecycle state, such as `created`, `updated`, or `deleted`.
- `access_method`: access method for this individual link record: `URL` or `QR`.
- `link`: PrettyLinks-aligned fields plus `base_target_url`.
- `payload`: UTM data used to generate the final `target_url`, including generated `utm_term`.
- `qr_code`: optional QR artifact metadata for QR link records.
- `created_at`: ISO 8601 timestamp for PrettySlack record creation.
- `updated_at`: ISO 8601 timestamp for the last PrettySlack record update.
- `deleted_at`: ISO 8601 timestamp when PrettySlack marked the record deleted, or `null`.

QR link records may include a `qr_code` object that points to generated QR image artifacts in S3. In AWS terminology, the S3 object path/name inside a bucket is commonly called the object key, so PrettySlack uses `s3_key`.

```json
{
  "qr_code": {
    "s3_bucket": "prettyslack-qr-artifacts",
    "image_svg": {
      "s3_key": "qr/2026/CN25_Why_QR.svg",
      "content_type": "image/svg+xml",
      "created_at": "2026-04-30T00:05:00Z"
    },
    "image_png": {
      "s3_key": "qr/2026/CN25_Why_QR.png",
      "content_type": "image/png",
      "created_at": "2026-04-30T00:05:00Z"
    },
    "image_jpeg": {
      "s3_key": "qr/2026/CN25_Why_QR.jpg",
      "content_type": "image/jpeg",
      "created_at": "2026-04-30T00:05:00Z"
    }
  }
}
```

## Generated Payload Direction

Given a workflow with `mode=both`, PrettySlack should produce two PrettyLinks-ready payloads:

- one using `slug=CN25_Why` and a generated `target_url` with `utm_term=URL`
- one using `slug=CN25_Why_QR` and a generated `target_url` with `utm_term=QR`

PrettyLinks should receive `target_url`. PrettySlack uses `base_target_url` only while generating the final URL.
