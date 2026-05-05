"""Build PrettySlack QR image artifacts."""

from io import BytesIO
from urllib.parse import urlsplit, urlunsplit

import qrcode
from qrcode.image.svg import SvgPathImage


IMAGE_FORMATS = {
    "svg": {
        "metadata_key": "image_svg",
        "extension": "svg",
        "content_type": "image/svg+xml",
    },
    "png": {
        "metadata_key": "image_png",
        "extension": "png",
        "content_type": "image/png",
    },
    "jpeg": {
        "metadata_key": "image_jpeg",
        "extension": "jpg",
        "content_type": "image/jpeg",
    },
}


DEFAULT_FORMATS = ("svg", "png", "jpeg")


def build_qr_artifacts(
    pretty_link_hostname,
    slug,
    image_formats=DEFAULT_FORMATS,
):
    """Build QR image bytes for a PrettyLink hostname and slug."""
    pretty_link_url = build_pretty_link_url(pretty_link_hostname, slug)
    qr_code = _build_qr_code(pretty_link_url)
    artifacts = {}

    for image_format in image_formats:
        format_details = _format_details(image_format)
        metadata_key = format_details["metadata_key"]

        artifacts[metadata_key] = {
            "filename": f"{slug}.{format_details['extension']}",
            "content_type": format_details["content_type"],
            "data": _render_qr_image(qr_code, image_format),
        }

    return {
        "pretty_link_url": pretty_link_url,
        "artifacts": artifacts,
    }


def build_pretty_link_url(pretty_link_hostname, slug):
    """Build the public PrettyLink URL encoded into the QR code."""
    if "://" not in pretty_link_hostname:
        pretty_link_hostname = f"https://{pretty_link_hostname}"

    parts = urlsplit(pretty_link_hostname)
    clean_slug = slug.strip("/")

    return urlunsplit((
        "https",
        parts.netloc,
        f"/{clean_slug}",
        "",
        "",
    ))


def _build_qr_code(target_url):
    qr_code = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=15,
        border=4,
    )
    qr_code.add_data(target_url)
    qr_code.make(fit=True)
    return qr_code


def _render_qr_image(qr_code, image_format):
    if image_format == "svg":
        image = qr_code.make_image(image_factory=SvgPathImage)
        return image.to_string()

    image = qr_code.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()

    if image_format == "png":
        image.save(buffer, format="PNG")
    elif image_format == "jpeg":
        image.convert("RGB").save(buffer, format="JPEG")
    else:
        raise ValueError(f"Unsupported QR image format: {image_format}")

    return buffer.getvalue()


def _format_details(image_format):
    try:
        return IMAGE_FORMATS[image_format]
    except KeyError as exc:
        raise ValueError(f"Unsupported QR image format: {image_format}") from exc
