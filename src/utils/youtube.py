"""
Utility functions for working with YouTube URLs.

This module provides helper functions to:

- Validate YouTube URLs
- Extract YouTube video IDs
- Normalize URLs
- Detect Shorts videos
- Detect Live videos

Author:
    Shravan Kumar Pandey
"""

from __future__ import annotations

from urllib.parse import parse_qs, urlparse

from src.exception import handle_exception
from src.logger import get_logger

logger = get_logger(__name__)

# ==============================================================================
# Supported Hosts
# ==============================================================================

SUPPORTED_HOSTS = {
    "youtube.com",
    "www.youtube.com",
    "m.youtube.com",
    "music.youtube.com",
    "youtu.be",
}

# ==============================================================================
# Validation
# ==============================================================================


def is_valid_youtube_url(url: str) -> bool:
    """
    Validate a YouTube URL.
    """

    if not url:
        return False

    url = url.strip()

    try:
        parsed = urlparse(url)

        if parsed.scheme not in ("http", "https"):
            return False

        if parsed.netloc.lower() not in SUPPORTED_HOSTS:
            return False

        if parsed.netloc.lower() == "youtu.be":
            return len(parsed.path.strip("/")) > 0

        if parsed.path == "/watch":
            query = parse_qs(parsed.query)
            return "v" in query

        if parsed.path.startswith("/shorts/"):
            return True

        if parsed.path.startswith("/embed/"):
            return True

        if parsed.path.startswith("/live/"):
            return True

        return False

    except Exception:
        return False


# ==============================================================================
# Video ID Extraction
# ==============================================================================


def extract_video_id(url: str) -> str:
    """
    Extract YouTube video ID.
    """

    try:

        if not is_valid_youtube_url(url):
            raise ValueError("Invalid YouTube URL.")

        parsed = urlparse(url)

        host = parsed.netloc.lower()

        if host == "youtu.be":
            video_id = parsed.path.strip("/")

        elif parsed.path == "/watch":
            video_id = parse_qs(parsed.query)["v"][0]

        elif parsed.path.startswith("/embed/"):
            video_id = parsed.path.split("/")[2]

        elif parsed.path.startswith("/shorts/"):
            video_id = parsed.path.split("/")[2]

        elif parsed.path.startswith("/live/"):
            video_id = parsed.path.split("/")[2]

        else:
            raise ValueError("Unsupported YouTube URL.")

        video_id = video_id.strip()

        if not video_id:
            raise ValueError("Unable to extract video ID.")

        logger.info("Video ID extracted successfully.")

        return video_id

    except Exception as e:

        raise handle_exception(
            "Failed to extract YouTube Video ID.",
            e,
        ) from e


# ==============================================================================
# URL Normalization
# ==============================================================================


def normalize_youtube_url(url: str) -> str:
    """
    Convert any supported YouTube URL to a canonical watch URL.
    """

    video_id = extract_video_id(url)

    normalized = (
        f"https://www.youtube.com/watch?v={video_id}"
    )

    logger.info("URL normalized successfully.")

    return normalized


# ==============================================================================
# Shorts Detection
# ==============================================================================


def is_shorts_url(url: str) -> bool:
    """
    Check whether the URL is a Shorts URL.
    """

    return "/shorts/" in url


# ==============================================================================
# Live Detection
# ==============================================================================


def is_live_url(url: str) -> bool:
    """
    Check whether the URL is a Live URL.
    """

    return "/live/" in url