"""
Embedding model module for the YouTube Chatbot RAG application.

This module provides a singleton wrapper around Google's embedding model
used for generating vector embeddings.

Author:
    Shravan Kumar Pandey
"""

from __future__ import annotations

from langchain_core.embeddings import Embeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from src.config import settings
from src.exception import handle_exception
from src.logger import get_logger

logger = get_logger(__name__)


class EmbeddingModel:
    """
    Singleton wrapper for Google Generative AI Embeddings.
    """

    _instance: GoogleGenerativeAIEmbeddings | None = None

    @classmethod
    def get_embedding_model(cls) -> Embeddings:
        """
        Return a singleton embedding model instance.

        Returns:
            Embeddings:
                Configured GoogleGenerativeAIEmbeddings instance.

        Raises:
            YouTubeChatbotException:
                If initialization fails.
        """

        try:

            if cls._instance is None:

                logger.info(
                    "Initializing embedding model: %s",
                    settings.EMBEDDING_MODEL,
                )

                cls._instance = GoogleGenerativeAIEmbeddings(
                    model=settings.EMBEDDING_MODEL,
                    google_api_key=settings.GOOGLE_API_KEY,
                )

                logger.info(
                    "Embedding model initialized successfully."
                )

            return cls._instance

        except Exception as e:

            raise handle_exception(
                "Failed to initialize embedding model.",
                e,
            ) from e

    @classmethod
    def model_name(cls) -> str:
        """
        Return embedding model name.

        Returns:
            str
        """
        return settings.EMBEDDING_MODEL

    @classmethod
    def reset(cls) -> None:
        """
        Reset the singleton instance.

        Useful for testing.
        """

        cls._instance = None

        logger.info(
            "Embedding model instance has been reset."
        )