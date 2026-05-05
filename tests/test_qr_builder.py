"""Tests for PrettySlack QR artifact building."""

from io import BytesIO
import unittest

from PIL import Image

from prettyslack.qr_builder import build_pretty_link_url, build_qr_artifacts


class TestQrBuilder(unittest.TestCase):
    """Validate QR artifact generation behavior."""

    def setUp(self):
        """Create reusable QR builder inputs for tests."""
        self.pretty_link_hostname = "cng.bio"
        self.slug = "CN25_Why_QR"

    def test_builds_pretty_link_url_from_hostname_and_slug(self):
        """Build the public PrettyLink URL encoded into the QR code."""
        pretty_link_url = build_pretty_link_url(
            self.pretty_link_hostname,
            self.slug,
        )

        self.assertEqual(pretty_link_url, "https://cng.bio/CN25_Why_QR")

    def test_builds_pretty_link_url_from_https_hostname(self):
        """Accept a hostname that already includes an HTTPS scheme."""
        pretty_link_url = build_pretty_link_url(
            "https://cng.bio",
            self.slug,
        )

        self.assertEqual(pretty_link_url, "https://cng.bio/CN25_Why_QR")

    def test_builds_image_artifacts(self):
        """Return image bytes and content metadata for later upload."""
        result = build_qr_artifacts(
            self.pretty_link_hostname,
            self.slug,
        )

        artifacts = result["artifacts"]

        self.assertEqual(result["pretty_link_url"], "https://cng.bio/CN25_Why_QR")
        self.assertEqual(artifacts["image_svg"]["filename"], "CN25_Why_QR.svg")
        self.assertEqual(
            artifacts["image_png"]["filename"],
            "CN25_Why_QR.png",
        )
        self.assertEqual(
            artifacts["image_jpeg"]["content_type"],
            "image/jpeg",
        )
        self.assertTrue(artifacts["image_svg"]["data"].startswith(b"<svg"))
        self.assertTrue(artifacts["image_png"]["data"].startswith(b"\x89PNG"))
        self.assertTrue(artifacts["image_jpeg"]["data"].startswith(b"\xff\xd8"))

    def test_builds_raster_artifacts_at_or_above_minimum_size(self):
        """Render sample PNG and JPEG artifacts at least as large as the prior baseline."""
        result = build_qr_artifacts(
            self.pretty_link_hostname,
            self.slug,
        )

        png_image = Image.open(BytesIO(result["artifacts"]["image_png"]["data"]))
        jpeg_image = Image.open(BytesIO(result["artifacts"]["image_jpeg"]["data"]))

        self.assertEqual(png_image.size[0], png_image.size[1])
        self.assertEqual(jpeg_image.size[0], jpeg_image.size[1])
        self.assertGreaterEqual(png_image.size[0], 500)
        self.assertGreaterEqual(jpeg_image.size[0], 500)

    def test_can_build_selected_formats(self):
        """Allow callers to request only the artifacts they need."""
        result = build_qr_artifacts(
            self.pretty_link_hostname,
            self.slug,
            image_formats=("svg",),
        )

        self.assertEqual(list(result["artifacts"]), ["image_svg"])

    def test_rejects_unsupported_formats(self):
        """Reject unknown image formats explicitly."""
        with self.assertRaises(ValueError):
            build_qr_artifacts(
                self.pretty_link_hostname,
                self.slug,
                image_formats=("webp",),
            )


if __name__ == "__main__":
    unittest.main()
