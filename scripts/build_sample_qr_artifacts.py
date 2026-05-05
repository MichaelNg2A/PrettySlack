#!/usr/bin/env python3
"""Build sample PrettySlack QR artifacts from the workflow fixture."""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from prettyslack.link_builder import load_workflow_state
from prettyslack.qr_builder import build_qr_artifacts


OUTPUT_DIR = Path("/tmp/prettyslack_sample_qr")
PRETTY_LINK_HOSTNAME = "cng.bio"


def main():
    """Load the sample workflow fixture and write QR artifacts to /tmp."""
    workflow_state = load_workflow_state("fixtures/sample_workflow_state.json")
    slug = f"{workflow_state['link']['slug']}_QR"

    result = build_qr_artifacts(PRETTY_LINK_HOSTNAME, slug)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(result["pretty_link_url"])
    for artifact in result["artifacts"].values():
        output_path = OUTPUT_DIR / artifact["filename"]
        output_path.write_bytes(artifact["data"])
        print(output_path)


if __name__ == "__main__":
    main()
