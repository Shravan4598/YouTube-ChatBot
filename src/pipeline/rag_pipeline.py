"""
RAG pipeline for the YouTube Chatbot.

This module orchestrates the complete Retrieval-Augmented Generation (RAG)
workflow.

Pipeline:
    YouTube URL
        │
        ▼
    Transcript Loader
        │
        ▼
    Document Splitter
        │
        ▼
    Embedding Model
        │
        ▼
    FAISS Vector Store
        │
        ▼
    Retriever
        │
        ▼
    RAG Chain
        │
        ▼
    Response

Author:
    Shravan Kumar Pandey
"""

from __future__ import annotations

from langchain_core.runnables import Runnable

from src.chains.rag_chain import RAGChain
from src.exception import handle_exception
from src.loaders.youtube_loader import YouTubeTranscriptLoader
from src.logger import get_logger
from src.preprocess.splitter import DocumentSplitter
from src.retriever.retriever import RetrieverService
from src.utils.validators import (
    validate_question,
    validate_youtube_url,
)
from src.vectorstore.faiss_store import FAISSVectorStore

logger = get_logger(__name__)


class RAGPipeline:
    """
    Complete YouTube RAG Pipeline.
    """

    def __init__(self) -> None:
        """
        Initialize all pipeline components.
        """

        logger.info("Initializing RAG Pipeline...")

        self.loader = YouTubeTranscriptLoader()
        self.splitter = DocumentSplitter()
        self.vector_store = FAISSVectorStore()

        self.chain: Runnable | None = None

        logger.info("RAG Pipeline initialized successfully.")

    # ------------------------------------------------------------------
    # Build Pipeline
    # ------------------------------------------------------------------

    def build(self, youtube_url: str) -> None:
        """
        Build the RAG pipeline for a YouTube video.
        """

        try:

            validate_youtube_url(youtube_url)

            logger.info("Loading transcript...")

            documents = self.loader.load(youtube_url)

            logger.info(
                "Loaded %d document(s).",
                len(documents),
            )

            logger.info("Splitting documents...")

            chunks = self.splitter.split_documents(documents)

            logger.info(
                "Created %d chunk(s).",
                len(chunks),
            )

            logger.info("Creating FAISS vector store...")

            vector_db = self.vector_store.create(chunks)

            logger.info("Saving FAISS vector store...")

            self.vector_store.save(vector_db)

            logger.info("Creating retriever...")

            retriever = RetrieverService(
                vector_store=vector_db,
            ).get_retriever()

            logger.info("Building RAG chain...")

            self.chain = RAGChain(retriever).build()

            logger.info("RAG Pipeline built successfully.")

        except Exception as e:

            raise handle_exception(
                "Failed to build RAG pipeline.",
                e,
            ) from e

    # ------------------------------------------------------------------
    # Ask Question
    # ------------------------------------------------------------------

    def ask(self, question: str) -> str:
        """
        Ask a question about the processed YouTube video.
        """

        try:

            validate_question(question)

            if self.chain is None:
                raise RuntimeError(
                    "Pipeline has not been built. "
                    "Call build() first."
                )

            logger.info("Processing question...")

            response = self.chain.invoke(question)

            logger.info("Question answered successfully.")

            if isinstance(response, str):
                return response

            if isinstance(response, dict):

                if "answer" in response:
                    return response["answer"]

                if "output" in response:
                    return response["output"]

                if "result" in response:
                    return response["result"]

            return str(response)

        except Exception as e:

            raise handle_exception(
                "Failed to process question.",
                e,
            ) from e

    # ------------------------------------------------------------------
    # Reset
    # ------------------------------------------------------------------

    def reset(self) -> None:
        """
        Reset the pipeline.
        """

        self.chain = None

        logger.info("Pipeline reset successfully.")

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    @property
    def is_ready(self) -> bool:
        """
        Check whether the pipeline is ready.
        """

        return self.chain is not None