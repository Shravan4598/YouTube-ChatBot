"""
Text utility functions for the YouTube Chatbot RAG project.
"""

from __future__ import annotations

import re
from typing import Iterable, Any

from langchain_core.documents import Document

from src.logger import get_logger

logger = get_logger(__name__)


def clean_text(text: str) -> str:
    """Clean transcript text."""

    if not text:
        return ""

    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\n+", "\n", text)

    return text.strip()


def join_transcript(
    transcript: Iterable[Any],
    separator: str = " "
) -> str:
    """
    Join transcript segments into a single string.

    Supports both:
    - youtube-transcript-api < 1.0
    - youtube-transcript-api >= 1.0
    """

    if not transcript:
        return ""

    texts = []

    for segment in transcript:

        # Old API (dict)
        if isinstance(segment, dict):
            texts.append(segment.get("text", ""))

        # New API (FetchedTranscriptSnippet)
        elif hasattr(segment, "text"):
            texts.append(segment.text)

        else:
            logger.warning(
                "Unknown transcript segment type: %s",
                type(segment),
            )

    joined_text = separator.join(texts)

    logger.info(
        "Joined %d transcript segments.",
        len(texts),
    )

    return clean_text(joined_text)


def remove_duplicate_lines(text: str) -> str:
    seen = set()
    unique_lines = []

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        if line not in seen:
            seen.add(line)
            unique_lines.append(line)

    return "\n".join(unique_lines)


def format_documents(
    documents: Iterable[Document],
) -> str:

    context = "\n\n".join(
        doc.page_content.strip()
        for doc in documents
    )

    logger.info(
        "Formatted retrieved documents."
    )

    return context


def truncate_text(
    text: str,
    max_length: int = 300,
) -> str:

    text = clean_text(text)

    if len(text) <= max_length:
        return text

    return text[: max_length - 3] + "..."


def remove_empty_lines(text: str) -> str:

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    return "\n".join(lines)


def normalize_whitespace(text: str) -> str:

    return re.sub(r"\s+", " ", text).strip()


def chunk_statistics(text: str) -> dict[str, int]:

    cleaned = clean_text(text)

    return {
        "characters": len(cleaned),
        "words": len(cleaned.split()),
        "lines": len(cleaned.splitlines()),
    }