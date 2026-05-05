"""Simulate PrettyLinks create responses for local PrettySlack work."""

from hashlib import sha1
from urllib.parse import urlsplit

from prettyslack.qr_builder import build_pretty_link_url


SIMULATED_PROVIDER = "prettylinks_simulator"
DEFAULT_REDIRECT_TYPE = "307"
ALLOWED_REDIRECT_TYPES = {"301", "302", "307", "308"}


def create_pretty_link(payload, pretty_link_hostname="cng.bio", existing_slugs=None):
    """Validate and reflect a PrettyLinks-style payload without network calls."""
    normalized_payload = _normalize_payload(payload)
    errors = _validate_payload(
        normalized_payload,
        pretty_link_hostname,
        existing_slugs or (),
    )

    if errors:
        return {
            "ok": False,
            "status": "rejected",
            "provider": SIMULATED_PROVIDER,
            "pretty_link": None,
            "errors": errors,
        }

    pretty_link_url = build_pretty_link_url(
        pretty_link_hostname,
        normalized_payload["slug"],
    )

    return {
        "ok": True,
        "status": "created",
        "provider": SIMULATED_PROVIDER,
        "pretty_link": {
            "id": _simulated_pretty_link_id(normalized_payload["slug"]),
            "slug": normalized_payload["slug"],
            "pretty_link_url": pretty_link_url,
            "target_url": normalized_payload["target_url"],
            "name": normalized_payload["name"],
            "description": normalized_payload["description"],
            "redirect_type": normalized_payload["redirect_type"],
        },
        "errors": [],
    }


def _normalize_payload(payload):
    normalized_payload = dict(payload)

    if "slug" in normalized_payload and isinstance(normalized_payload["slug"], str):
        normalized_payload["slug"] = normalized_payload["slug"].strip()

    normalized_payload.setdefault("name", normalized_payload.get("slug", ""))
    normalized_payload.setdefault("description", "")
    normalized_payload.setdefault("redirect_type", DEFAULT_REDIRECT_TYPE)

    return normalized_payload


def _validate_payload(payload, pretty_link_hostname, existing_slugs):
    errors = []
    _validate_required_string(payload, "slug", errors)
    _validate_required_string(payload, "target_url", errors)

    slug = payload.get("slug")
    target_url = payload.get("target_url")

    if isinstance(slug, str) and slug:
        if slug.startswith(("?", "#")):
            errors.append(_error(
                "slug",
                "invalid",
                "Slug must not be only query or fragment characters.",
            ))
        if slug.startswith("/") or slug.endswith("/"):
            errors.append(_error(
                "slug",
                "invalid",
                "Slug must not start or end with a slash.",
            ))
        if slug in existing_slugs:
            errors.append(_error(
                "slug",
                "already_exists",
                "Slug is already present in the simulated PrettyLinks store.",
            ))

    if isinstance(target_url, str) and target_url:
        _validate_target_url(target_url, errors)

        if isinstance(slug, str) and slug:
            pretty_link_url = build_pretty_link_url(pretty_link_hostname, slug)
            if target_url == pretty_link_url:
                errors.append(_error(
                    "target_url",
                    "self_redirect",
                    "Target URL must differ from the PrettyLink URL.",
                ))

    redirect_type = str(payload.get("redirect_type", ""))
    if redirect_type not in ALLOWED_REDIRECT_TYPES:
        errors.append(_error(
            "redirect_type",
            "unsupported",
            "Redirect type must be one of 301, 302, 307, or 308.",
        ))

    return errors


def _validate_required_string(payload, field, errors):
    value = payload.get(field)
    if not isinstance(value, str) or not value.strip():
        errors.append(_error(
            field,
            "required",
            f"{field} is required.",
        ))


def _validate_target_url(target_url, errors):
    parts = urlsplit(target_url)

    if parts.scheme not in {"http", "https"} or not parts.netloc:
        errors.append(_error(
            "target_url",
            "invalid_url",
            "Target URL must be an absolute http or https URL.",
        ))


def _simulated_pretty_link_id(slug):
    slug_hash = sha1(slug.encode("utf-8")).hexdigest()[:12]
    return f"sim_{slug_hash}"


def _error(field, code, message):
    return {
        "field": field,
        "code": code,
        "message": message,
    }
