"""
Text splitter module for the YouTube Chatbot RAG application.

This module is responsible for splitting documents into smaller chunks
before generating embeddings.

Author:
    Shravan Kumar Pandey
"""

from __future__ import annotations

from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config import settings
from src.exception import handle_exception
from src.logger import get_logger
from src.utils.validators import validate_chunk_parameters

logger = get_logger(__name__)


class DocumentSplitter:
    """
    Splits LangChain documents into smaller chunks.
    """

    def __init__(
        self,
        chunk_size: int | None = None,
        chunk_overlap: int | None = None,
    ) -> None:

        self.chunk_size = chunk_size or settings.CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or settings.CHUNK_OVERLAP

        validate_chunk_parameters(
            self.chunk_size,
            self.chunk_overlap,
        )

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=[
                "\n\n",
                "\n",
                ". ",
                "? ",
                "! ",
                ", ",
                " ",
                "",
            ],
            keep_separator=True,
            add_start_index=True,
        )

        logger.info(
            "DocumentSplitter initialized (chunk_size=%d, overlap=%d)",
            self.chunk_size,
            self.chunk_overlap,
        )

    def split_documents(
        self,
        documents: List[Document],
    ) -> List[Document]:

        try:

            if not documents:
                raise ValueError("No documents provided.")

            chunks = self.text_splitter.split_documents(documents)

            logger.info(
                "Split %d document(s) into %d chunk(s).",
                len(documents),
                len(chunks),
            )

            return chunks

        except Exception as e:

            raise handle_exception(
                "Failed to split documents.",
                e,
            ) from e

    def split_text(
        self,
        text: str,
    ) -> List[str]:

        try:

            text = text.strip()

            if not text:
                raise ValueError("Input text is empty.")

            chunks = self.text_splitter.split_text(text)

            logger.info(
                "Split text into %d chunk(s).",
                len(chunks),
            )

            return chunks

        except Exception as e:

            raise handle_exception(
                "Failed to split text.",
                e,
            ) from e

    @property
    def configuration(self) -> dict:

        return {
            "chunk_size": self.chunk_size,
            "chunk_overlap": self.chunk_overlap,
            "splitter": self.__class__.__name__,
        }