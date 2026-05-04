#!/usr/bin/env python3
"""Build and print a sample PrettySlack target URL from the workflow fixture."""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from prettyslack.link_builder import build_target_url, load_workflow_state


def main():
    """Load the sample workflow fixture and print its URL variant target URL."""
    workflow_state = load_workflow_state("fixtures/sample_workflow_state.json")

    target_url = build_target_url(
        workflow_state["link"]["base_target_url"],
        workflow_state["payload"],
        "URL",
    )

    print(target_url)


if __name__ == "__main__":
    main()
