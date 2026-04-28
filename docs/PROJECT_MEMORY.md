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
- The initial implementation should make URL/UTM payload generation testable before adding live Slack, AWS, or WordPress/PrettyLinks writes.
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
- RDS is likely overkill for recent-value memory. A small JSON document in local fixtures for early development and S3 for Lambda deployments is the preferred lightweight direction.

## Environment Notes

- The devcontainer installs Python, Node, Git, and the ChatGPT VS Code extension.
- Codespaces is configured to request write access to `MichaelNg2A/Operator_Context` for cross-repository persistent context.
- `poppler-utils` may be installed manually in a Codespace when PDF text extraction is needed; it is not currently part of the repo devcontainer definition.

## Known Constraints

- Personal working preferences should not be mixed into project source-of-truth docs unless they affect project-specific workflow.
- Sensitive data belongs in GitHub Secrets or another secret-management system, not in repository memory files.
