"""
Validation utilities for the YouTube Chatbot RAG application.

This module contains reusable validation functions used throughout
the application.

Author:
    Shravan Kumar Pandey
"""

from __future__ import annotations

from pathlib import Path

from langchain_core.documents import Document

from src.config import settings
from src.exception import handle_exception
from src.logger import get_logger
from src.utils.youtube import is_valid_youtube_url

logger = get_logger(__name__)


def validate_google_api_key() -> bool:
    """
    Validate the Google Gemini API key.

    Returns:
        bool:
            True if valid.

    Raises:
        YouTubeChatbotException:
            If the API key is missing.
    """
    try:
        if not settings.GOOGLE_API_KEY.strip():
            raise ValueError(
                "GOOGLE_API_KEY is missing in the .env file."
            )

        logger.info("Google API key validation successful.")
        return True

    except Exception as e:
        raise handle_exception(
            "Google API key validation failed.",
            e,
        ) from e


def validate_youtube_url(url: str) -> bool:
    """
    Validate a YouTube URL.

    Args:
        url:
            YouTube URL.

    Returns:
        bool

    Raises:
        YouTubeChatbotException
    """

    try:

        if not url:
            raise ValueError("YouTube URL cannot be empty.")

        if not is_valid_youtube_url(url):
            raise ValueError("Invalid YouTube URL.")

        logger.info("YouTube URL validation successful.")

        return True

    except Exception as e:
        raise handle_exception(
            "YouTube URL validation failed.",
            e,
        ) from e


def validate_question(question: str) -> bool:
    """
    Validate the user's question.

    Args:
        question:
            User question.

    Returns:
        bool
    """

    try:

        if not question:
            raise ValueError("Question cannot be empty.")

        if len(question.strip()) < 3:
            raise ValueError(
                "Question is too short."
            )

        logger.info("Question validation successful.")

        return True

    except Exception as e:
        raise handle_exception(
            "Question validation failed.",
            e,
        ) from e


def validate_documents(
    documents: list[Document],
) -> bool:
    """
    Validate LangChain documents.

    Args:
        documents:
            List of Document objects.

    Returns:
        bool
    """

    try:

        if not documents:
            raise ValueError(
                "No documents available."
            )

        logger.info(
            "%d documents validated successfully.",
            len(documents),
        )

        return True

    except Exception as e:
        raise handle_exception(
            "Document validation failed.",
            e,
        ) from e


def validate_vector_store(path: Path) -> bool:
    """
    Validate the FAISS vector store directory.

    Args:
        path:
            Path to FAISS directory.

    Returns:
        bool
    """

    try:

        if not path.exists():
            raise FileNotFoundError(
                f"Vector store not found: {path}"
            )

        logger.info(
            "Vector store validation successful."
        )

        return True

    except Exception as e:
        raise handle_exception(
            "Vector store validation failed.",
            e,
        ) from e


def validate_transcript(transcript: str) -> bool:
    """
    Validate transcript text.

    Args:
        transcript:
            Transcript text.

    Returns:
        bool
    """

    try:

        if not transcript:
            raise ValueError(
                "Transcript is empty."
            )

        if len(transcript.strip()) < 20:
            raise ValueError(
                "Transcript is too short."
            )

        logger.info(
            "Transcript validation successful."
        )

        return True

    except Exception as e:
        raise handle_exception(
            "Transcript validation failed.",
            e,
        ) from e


def validate_chunk_parameters(
    chunk_size: int,
    chunk_overlap: int,
) -> bool:
    """
    Validate text splitter parameters.

    Args:
        chunk_size:
            Chunk size.

        chunk_overlap:
            Chunk overlap.

    Returns:
        bool
    """

    try:

        if chunk_size <= 0:
            raise ValueError(
                "Chunk size must be greater than zero."
            )

        if chunk_overlap < 0:
            raise ValueError(
                "Chunk overlap cannot be negative."
            )

        if chunk_overlap >= chunk_size:
            raise ValueError(
                "Chunk overlap must be smaller than chunk size."
            )

        logger.info(
            "Chunk configuration validated."
        )

        return True

    except Exception as e:
        raise handle_exception(
            "Chunk configuration validation failed.",
            e,
        ) from e


def validate_top_k(top_k: int) -> bool:
    """
    Validate retriever top-k value.

    Args:
        top_k:
            Number of retrieved documents.

    Returns:
        bool
    """

    try:

        if top_k <= 0:
            raise ValueError(
                "TOP_K must be greater than zero."
            )

        logger.info("TOP_K validation successful.")

        return True

    except Exception as e:
        raise handle_exception(
            "TOP_K validation failed.",
            e,
        ) from e