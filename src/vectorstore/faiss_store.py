"""
FAISS vector store module for the YouTube Chatbot RAG application.

This module is responsible for:

- Creating a FAISS vector database
- Saving the vector database
- Loading an existing vector database
- Providing a retriever
- Managing persistence

Author:
    Shravan Kumar Pandey
"""

from __future__ import annotations

from pathlib import Path
from typing import List

from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStore
from langchain_community.vectorstores import FAISS

from src.config import settings
from src.embeddings.embedding_model import EmbeddingModel
from src.exception import handle_exception
from src.logger import get_logger

logger = get_logger(__name__)


class FAISSVectorStore:
    """
    Wrapper class for LangChain FAISS vector store.
    """

    def __init__(
        self,
        persist_directory: Path | None = None,
    ) -> None:
        """
        Initialize FAISS vector store.

        Args:
            persist_directory:
                Directory where the FAISS index will be saved.
        """

        self.persist_directory = (
            Path(persist_directory)
            if persist_directory
            else Path(settings.VECTOR_STORE_PATH)
        )

        self.persist_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.embedding_model = (
            EmbeddingModel.get_embedding_model()
        )

        logger.info(
            "FAISS storage directory: %s",
            self.persist_directory,
        )

    # ------------------------------------------------------------------
    # Create
    # ------------------------------------------------------------------

    def create(
        self,
        documents: List[Document],
    ) -> FAISS:
        """
        Create a FAISS vector store.

        Args:
            documents:
                List of LangChain documents.

        Returns:
            FAISS vector store.
        """

        try:

            if not documents:
                raise ValueError(
                    "No documents provided."
                )

            logger.info(
                "Creating FAISS vector store..."
            )

            vector_store = FAISS.from_documents(
                documents=documents,
                embedding=self.embedding_model,
            )

            logger.info(
                "FAISS vector store created successfully."
            )

            return vector_store

        except Exception as e:

            raise handle_exception(
                "Failed to create FAISS vector store.",
                e,
            ) from e

    # ------------------------------------------------------------------
    # Save
    # ------------------------------------------------------------------

    def save(
        self,
        vector_store: FAISS,
    ) -> None:
        """
        Save FAISS index locally.

        Args:
            vector_store:
                FAISS vector store.
        """

        try:

            logger.info(
                "Saving FAISS vector store..."
            )

            vector_store.save_local(
                str(self.persist_directory)
            )

            logger.info(
                "Vector store saved successfully."
            )

        except Exception as e:

            raise handle_exception(
                "Failed to save FAISS vector store.",
                e,
            ) from e

    # ------------------------------------------------------------------
    # Load
    # ------------------------------------------------------------------

    def load(self) -> FAISS:
        """
        Load an existing FAISS vector store.

        Returns:
            FAISS vector store.
        """

        try:

            if not self.exists():
                raise FileNotFoundError(
                    f"No FAISS index found in {self.persist_directory}"
                )

            logger.info(
                "Loading FAISS vector store..."
            )

            vector_store = FAISS.load_local(
                folder_path=str(self.persist_directory),
                embeddings=self.embedding_model,
                allow_dangerous_deserialization=True,
            )

            logger.info(
                "FAISS vector store loaded successfully."
            )

            return vector_store

        except Exception as e:

            raise handle_exception(
                "Failed to load FAISS vector store.",
                e,
            ) from e

    # ------------------------------------------------------------------
    # Exists
    # ------------------------------------------------------------------

    def exists(self) -> bool:
        """
        Check whether a FAISS index exists.

        Returns:
            True if the vector store exists.
        """

        index_file = self.persist_directory / "index.faiss"
        metadata_file = self.persist_directory / "index.pkl"

        return (
            index_file.exists()
            and metadata_file.exists()
        )

    # ------------------------------------------------------------------
    # Retriever
    # ------------------------------------------------------------------

    def as_retriever(
        self,
        vector_store: VectorStore,
        search_type: str = "similarity",
        k: int | None = None,
    ):
        """
        Convert vector store into a retriever.

        Args:
            vector_store:
                FAISS vector store.

            search_type:
                similarity | mmr

            k:
                Number of retrieved chunks.

        Returns:
            LangChain Retriever.
        """

        try:

            retriever = vector_store.as_retriever(
                search_type=search_type,
                search_kwargs={
                    "k": k or settings.RETRIEVER_TOP_K
                },
            )

            logger.info(
                "Retriever created successfully."
            )

            return retriever

        except Exception as e:

            raise handle_exception(
                "Failed to create retriever.",
                e,
            ) from e

    # ------------------------------------------------------------------
    # Delete
    # ------------------------------------------------------------------

    def delete(self) -> None:
        """
        Delete the saved FAISS index.
        """

        try:

            if not self.persist_directory.exists():
                return

            for file in self.persist_directory.iterdir():
                if file.is_file():
                    file.unlink()

            logger.info(
                "FAISS vector store deleted."
            )

        except Exception as e:

            raise handle_exception(
                "Failed to delete vector store.",
                e,
            ) from e