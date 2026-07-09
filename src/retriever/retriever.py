"""
Retriever service for the YouTube Chatbot RAG application.

This module provides a reusable abstraction over LangChain retrievers.

Features:
- Similarity Search
- Max Marginal Relevance (MMR)
- Configurable Top-K
- Metadata filtering support (future)
- Logging
- Exception handling

Author:
    Shravan Kumar Pandey
"""

from __future__ import annotations

from typing import List, Optional

from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_core.vectorstores import VectorStore

from src.config import settings
from src.exception import handle_exception
from src.logger import get_logger

logger = get_logger(__name__)


class RetrieverService:
    """
    Service class for creating and using retrievers.
    """

    VALID_SEARCH_TYPES = {
        "similarity",
        "mmr",
        "similarity_score_threshold",
    }

    def __init__(
        self,
        vector_store: VectorStore,
        search_type: str = "similarity",
        top_k: Optional[int] = None,
    ) -> None:
        """
        Initialize the retriever service.
        """

        self.vector_store = vector_store
        self.search_type = (
            search_type
            if search_type in self.VALID_SEARCH_TYPES
            else "similarity"
        )

        self.top_k = top_k or settings.RETRIEVER_TOP_K

        self._retriever: BaseRetriever | None = None

        logger.info(
            "Retriever initialized (search_type=%s, top_k=%d)",
            self.search_type,
            self.top_k,
        )

    # ------------------------------------------------------------------
    # Build Retriever
    # ------------------------------------------------------------------

    def get_retriever(self) -> BaseRetriever:
        """
        Create or return the cached LangChain retriever.
        """

        try:

            if self._retriever is None:

                self._retriever = self.vector_store.as_retriever(
                    search_type=self.search_type,
                    search_kwargs={
                        "k": self.top_k,
                    },
                )

                logger.info(
                    "Retriever created successfully."
                )

            return self._retriever

        except Exception as e:

            raise handle_exception(
                "Failed to create retriever.",
                e,
            ) from e

    # ------------------------------------------------------------------
    # Retrieve Documents
    # ------------------------------------------------------------------

    def retrieve(
        self,
        query: str,
    ) -> List[Document]:
        """
        Retrieve relevant documents.
        """

        try:

            documents = self.get_retriever().invoke(query)

            logger.info(
                "Retrieved %d document(s).",
                len(documents),
            )

            return documents

        except Exception as e:

            raise handle_exception(
                "Failed to retrieve documents.",
                e,
            ) from e

    # ------------------------------------------------------------------
    # Update Search Configuration
    # ------------------------------------------------------------------

    def update_search(
        self,
        *,
        search_type: Optional[str] = None,
        top_k: Optional[int] = None,
    ) -> None:
        """
        Update retrieval configuration.
        """

        if (
            search_type is not None
            and search_type in self.VALID_SEARCH_TYPES
        ):
            self.search_type = search_type

        if top_k is not None:
            self.top_k = top_k

        # Force recreation with new settings
        self._retriever = None

        logger.info(
            "Retriever configuration updated (search_type=%s, top_k=%d)",
            self.search_type,
            self.top_k,
        )

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------

    @property
    def configuration(self) -> dict:
        """
        Return retriever configuration.
        """

        return {
            "search_type": self.search_type,
            "top_k": self.top_k,
        }