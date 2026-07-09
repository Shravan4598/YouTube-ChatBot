"""
Google Gemini LLM wrapper for the YouTube Chatbot RAG application.

This module provides a singleton wrapper around the
ChatGoogleGenerativeAI model.

Author:
    Shravan Kumar Pandey
"""

from __future__ import annotations

from langchain_google_genai import ChatGoogleGenerativeAI

from src.config import settings
from src.exception import handle_exception
from src.logger import get_logger

logger = get_logger(__name__)


class GeminiLLM:
    """
    Singleton wrapper for Google Gemini LLM.
    """

    _instance: ChatGoogleGenerativeAI | None = None

    @classmethod
    def get_llm(cls) -> ChatGoogleGenerativeAI:
        """
        Return a singleton Gemini model.
        """

        try:

            if cls._instance is None:

                logger.info(
                    "Initializing Gemini model: %s",
                    settings.GEMINI_MODEL,
                )

                cls._instance = ChatGoogleGenerativeAI(
                    model=settings.GEMINI_MODEL,
                    google_api_key=settings.GOOGLE_API_KEY,
                    temperature=settings.TEMPERATURE,
                    max_output_tokens=settings.MAX_OUTPUT_TOKENS,
                    top_p=settings.GEMINI_TOP_P,
                    top_k=settings.GEMINI_TOP_K,
                    timeout=settings.REQUEST_TIMEOUT,
                    max_retries=settings.MAX_RETRIES,
                )

                logger.info(
                    "Gemini initialized successfully."
                )

            return cls._instance

        except Exception as e:

            raise handle_exception(
                "Failed to initialize Gemini model.",
                e,
            ) from e

    @classmethod
    def reset(cls) -> None:
        """
        Reset singleton instance.
        """

        cls._instance = None

        logger.info(
            "Gemini singleton reset."
        )

    @classmethod
    def model_name(cls) -> str:
        """
        Return model name.
        """

        return settings.GEMINI_MODEL

    @classmethod
    def model_info(cls) -> dict:
        """
        Return model configuration.
        """

        return {
            "model": settings.GEMINI_MODEL,
            "temperature": settings.TEMPERATURE,
            "max_output_tokens": settings.MAX_OUTPUT_TOKENS,
            "top_p": settings.GEMINI_TOP_P,
            "top_k": settings.GEMINI_TOP_K,
            "timeout": settings.REQUEST_TIMEOUT,
            "max_retries": settings.MAX_RETRIES,
        }