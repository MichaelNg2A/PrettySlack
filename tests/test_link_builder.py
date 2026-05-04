"""Tests for PrettySlack target URL building."""

import unittest

from prettyslack.link_builder import build_target_url


class TestLinkBuilder(unittest.TestCase):
    """Validate target URL generation behavior."""

    def setUp(self):
        """Create a reusable sample payload for tests."""
        self.payload = {
            "utm_source": "Celebrity_CruiseNight_20250917",
            "utm_medium": "event",
            "utm_campaign": "TA_Top10_Flyer",
            "utm_content": "Flyer",
        }

    def test_happy_path_builds_expected_target_url(self):
        """Build the expected target URL from a simple base URL."""
        target_url = build_target_url(
            "https://cng.bio/Alaska2026/",
            self.payload,
            "URL",
        )

        expected_url = (
            "https://cng.bio/Alaska2026/"
            "?utm_source=Celebrity_CruiseNight_20250917"
            "&utm_medium=event"
            "&utm_campaign=TA_Top10_Flyer"
            "&utm_term=URL"
            "&utm_content=Flyer"
        )

        self.assertEqual(target_url, expected_url)

    def test_preserves_existing_non_utm_query_params(self):
        """Keep non-UTM query parameters already present in the base URL."""
        target_url = build_target_url(
            "https://cng.bio/Trips?vendor=Princess",
            self.payload,
            "URL",
        )

        expected_url = (
            "https://cng.bio/Trips/"
            "?vendor=Princess"
            "&utm_source=Celebrity_CruiseNight_20250917"
            "&utm_medium=event"
            "&utm_campaign=TA_Top10_Flyer"
            "&utm_term=URL"
            "&utm_content=Flyer"
        )

        self.assertEqual(target_url, expected_url)

    def test_preserves_fragment_after_query_string(self):
        """Keep the fragment and place it after the generated query string."""
        target_url = build_target_url(
            "https://cng.bio/Certifications#Princess",
            self.payload,
            "URL",
        )

        expected_url = (
            "https://cng.bio/Certifications/"
            "?utm_source=Celebrity_CruiseNight_20250917"
            "&utm_medium=event"
            "&utm_campaign=TA_Top10_Flyer"
            "&utm_term=URL"
            "&utm_content=Flyer"
            "#Princess"
        )

        self.assertEqual(target_url, expected_url)

    def test_missing_scheme_defaults_to_https(self):
        """Add https when the base URL does not include a scheme."""
        target_url = build_target_url(
            "cng.bio/Alaska2026/",
            self.payload,
            "URL",
        )

        expected_url = (
            "https://cng.bio/Alaska2026/"
            "?utm_source=Celebrity_CruiseNight_20250917"
            "&utm_medium=event"
            "&utm_campaign=TA_Top10_Flyer"
            "&utm_term=URL"
            "&utm_content=Flyer"
        )

        self.assertEqual(target_url, expected_url)

    def test_replaces_existing_utm_query_params(self):
        """Replace UTM parameters already present in the base URL."""
        target_url = build_target_url(
            "https://cng.bio/Trips?utm_source=old_source&utm_medium=old_medium",
            self.payload,
            "URL",
        )

        expected_url = (
            "https://cng.bio/Trips/"
            "?utm_source=Celebrity_CruiseNight_20250917"
            "&utm_medium=event"
            "&utm_campaign=TA_Top10_Flyer"
            "&utm_term=URL"
            "&utm_content=Flyer"
        )

        self.assertEqual(target_url, expected_url)

    def test_accepts_qr_as_utm_term(self):
        """Use the caller-provided access method as utm_term."""
        target_url = build_target_url(
            "https://cng.bio/Alaska2026/",
            self.payload,
            "QR",
        )

        expected_url = (
            "https://cng.bio/Alaska2026/"
            "?utm_source=Celebrity_CruiseNight_20250917"
            "&utm_medium=event"
            "&utm_campaign=TA_Top10_Flyer"
            "&utm_term=QR"
            "&utm_content=Flyer"
        )

        self.assertEqual(target_url, expected_url)

    def test_forces_http_to_https(self):
        """Replace an http scheme with https in the final target URL."""
        target_url = build_target_url(
            "http://cng.bio/Alaska2026/",
            self.payload,
            "URL",
        )

        expected_url = (
            "https://cng.bio/Alaska2026/"
            "?utm_source=Celebrity_CruiseNight_20250917"
            "&utm_medium=event"
            "&utm_campaign=TA_Top10_Flyer"
            "&utm_term=URL"
            "&utm_content=Flyer"
        )

        self.assertEqual(target_url, expected_url)

    def test_encodes_spaces_and_special_characters(self):
        """Safely encode payload values that contain spaces or special characters."""
        payload = {
            "utm_source": "Celebrity Cruise Night",
            "utm_medium": "event",
            "utm_campaign": "A&B Test",
            "utm_content": "Top 10 Flyer",
        }

        target_url = build_target_url(
            "https://cng.bio/Alaska2026/",
            payload,
            "URL",
        )

        expected_url = (
            "https://cng.bio/Alaska2026/"
            "?utm_source=Celebrity+Cruise+Night"
            "&utm_medium=event"
            "&utm_campaign=A%26B+Test"
            "&utm_term=URL"
            "&utm_content=Top+10+Flyer"
        )

        self.assertEqual(target_url, expected_url)


if __name__ == "__main__":
    unittest.main()
