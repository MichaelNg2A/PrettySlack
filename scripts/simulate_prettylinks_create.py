#!/usr/bin/env python3
"""Build and print a simulated PrettyLinks create response."""

from pathlib import Path
import json
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from prettyslack.link_builder import build_target_url, load_workflow_state
from prettyslack.prettylinks_create_simulator import create_pretty_link


def main():
    """Load the sample workflow fixture and print a simulated create response."""
    workflow_state = load_workflow_state("fixtures/sample_workflow_state.json")
    link = workflow_state["link"]

    target_url = build_target_url(
        link["base_target_url"],
        workflow_state["payload"],
        "URL",
    )
    pretty_links_payload = {
        "slug": link["slug"],
        "target_url": target_url,
        "name": link["name"],
        "description": link["description"],
        "redirect_type": link["redirect_type"],
    }

    result = create_pretty_link(pretty_links_payload)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
