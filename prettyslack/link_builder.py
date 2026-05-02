"""Build PrettySlack target URLs."""

import json
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


UTM_KEYS = {
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_term",
    "utm_content",
}


def normalize_base_target_url(base_target_url):
    """Normalize a base target URL before adding PrettySlack UTM values."""
    if "://" not in base_target_url:
        base_target_url = f"https://{base_target_url}"

    parts = urlsplit(base_target_url)

    path = parts.path
    if not path:
        path = "/"
    elif not path.endswith("/") and "." not in path.rsplit("/", 1)[-1]:
        path = f"{path}/"

    return urlunsplit((
        "https",
        parts.netloc,
        path,
        parts.query,
        parts.fragment,
    ))


def build_target_url(base_target_url, payload, utm_term):
    """Build a target URL from a base target URL, UTM payload, and access method."""
    normalized_url = normalize_base_target_url(base_target_url)
    parts = urlsplit(normalized_url)

    existing_query = dict(parse_qsl(parts.query, keep_blank_values=True))
    preserved_query = {
        key: value
        for key, value in existing_query.items()
        if key.lower() not in UTM_KEYS
    }

    pretty_slack_utm = {
        "utm_source": payload["utm_source"],
        "utm_medium": payload["utm_medium"],
        "utm_campaign": payload["utm_campaign"],
        "utm_term": utm_term,
        "utm_content": payload["utm_content"],
    }

    final_query = preserved_query | pretty_slack_utm

    return urlunsplit((
        parts.scheme,
        parts.netloc,
        parts.path,
        urlencode(final_query),
        parts.fragment,
    ))


def load_workflow_state(path):
    """Load workflow state from a JSON fixture file."""
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


if __name__ == "__main__":
    workflow_state = load_workflow_state("fixtures/sample_workflow_state.json")

    target_url = build_target_url(
        workflow_state["link"]["base_target_url"],
        workflow_state["payload"],
        "URL",
    )

    print(target_url)
