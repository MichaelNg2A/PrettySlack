"""Tests for the temporary PrettyLinks create simulator."""

import unittest

from prettyslack.prettylinks_create_simulator import create_pretty_link


class TestPrettyLinksCreateSimulator(unittest.TestCase):
    """Validate simulated PrettyLinks create responses."""

    def setUp(self):
        """Create a reusable PrettyLinks-style payload."""
        self.payload = {
            "slug": "CN25_Why",
            "target_url": (
                "https://cng.bio/Alaska2026/"
                "?utm_source=Celebrity_CruiseNight_20250917"
                "&utm_medium=event"
                "&utm_campaign=TA_Top10_Flyer"
                "&utm_term=URL"
                "&utm_content=Flyer"
            ),
            "name": "CN25 Why",
            "description": "Celebrity cruise night Top 10 flyer",
            "redirect_type": "307",
        }

    def test_create_pretty_link_returns_success_response(self):
        """Reflect a valid payload as a simulated PrettyLinks creation."""
        result = create_pretty_link(self.payload)

        pretty_link = result["pretty_link"]

        self.assertTrue(result["ok"])
        self.assertEqual(result["status"], "created")
        self.assertEqual(result["provider"], "prettylinks_simulator")
        self.assertEqual(result["errors"], [])
        self.assertEqual(pretty_link["slug"], "CN25_Why")
        self.assertEqual(pretty_link["pretty_link_url"], "https://cng.bio/CN25_Why")
        self.assertEqual(pretty_link["target_url"], self.payload["target_url"])
        self.assertEqual(pretty_link["redirect_type"], "307")
        self.assertTrue(pretty_link["id"].startswith("sim_"))
        self.assertNotIn("track_me", pretty_link)
        self.assertNotIn("nofollow", pretty_link)
        self.assertNotIn("sponsored", pretty_link)
        self.assertNotIn("param_forwarding", pretty_link)

    def test_defaults_optional_prettylinks_fields(self):
        """Fill optional PrettyLinks-aligned fields with local defaults."""
        result = create_pretty_link({
            "slug": "CN25_Why",
            "target_url": self.payload["target_url"],
        })

        pretty_link = result["pretty_link"]

        self.assertTrue(result["ok"])
        self.assertEqual(pretty_link["name"], "CN25_Why")
        self.assertEqual(pretty_link["description"], "")
        self.assertEqual(pretty_link["redirect_type"], "307")

    def test_accepts_custom_pretty_link_hostname(self):
        """Build the reflected public link URL from a caller-provided hostname."""
        result = create_pretty_link(
            self.payload,
            pretty_link_hostname="links.example.com",
        )

        self.assertEqual(
            result["pretty_link"]["pretty_link_url"],
            "https://links.example.com/CN25_Why",
        )

    def test_rejects_missing_required_fields(self):
        """Return structured validation errors for missing required fields."""
        result = create_pretty_link({})

        self.assertFalse(result["ok"])
        self.assertEqual(result["status"], "rejected")
        self.assertIsNone(result["pretty_link"])
        self.assertEqual(
            {error["field"] for error in result["errors"]},
            {"slug", "target_url"},
        )

    def test_rejects_invalid_target_url(self):
        """Reject target URLs that are not absolute HTTP(S) URLs."""
        result = create_pretty_link(self.payload | {"target_url": "Alaska2026"})

        self.assertFalse(result["ok"])
        self.assertEqual(result["errors"][0]["field"], "target_url")
        self.assertEqual(result["errors"][0]["code"], "invalid_url")

    def test_rejects_self_redirect_to_public_pretty_link_url(self):
        """Reject payloads where the PrettyLink would point at itself."""
        result = create_pretty_link(
            self.payload | {"target_url": "https://cng.bio/CN25_Why"},
        )

        self.assertFalse(result["ok"])
        self.assertIn(
            {
                "field": "target_url",
                "code": "self_redirect",
                "message": "Target URL must differ from the PrettyLink URL.",
            },
            result["errors"],
        )

    def test_rejects_existing_slug_in_simulated_store(self):
        """Allow callers to simulate PrettyLinks slug availability checks."""
        result = create_pretty_link(
            self.payload,
            existing_slugs={"CN25_Why"},
        )

        self.assertFalse(result["ok"])
        self.assertEqual(result["errors"][0]["field"], "slug")
        self.assertEqual(result["errors"][0]["code"], "already_exists")

    def test_rejects_slug_with_slashes(self):
        """Reject slug values that look like paths instead of PrettyLinks slugs."""
        result = create_pretty_link(self.payload | {"slug": "CN25_Why/"})

        self.assertFalse(result["ok"])
        self.assertEqual(result["errors"][0]["field"], "slug")
        self.assertEqual(result["errors"][0]["code"], "invalid")

    def test_accepts_308_redirect_type(self):
        """Allow permanent method-preserving redirects."""
        result = create_pretty_link(self.payload | {"redirect_type": "308"})

        self.assertTrue(result["ok"])
        self.assertEqual(result["pretty_link"]["redirect_type"], "308")

    def test_rejects_unsupported_redirect_type(self):
        """Reject redirect types outside the small supported simulator set."""
        result = create_pretty_link(self.payload | {"redirect_type": "pixel"})

        self.assertFalse(result["ok"])
        self.assertEqual(result["errors"][0]["field"], "redirect_type")
        self.assertEqual(result["errors"][0]["code"], "unsupported")


if __name__ == "__main__":
    unittest.main()
