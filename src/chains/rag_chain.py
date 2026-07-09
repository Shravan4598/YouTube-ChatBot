"""
RAG Chain for the YouTube Chatbot.

This module builds the complete Retrieval-Augmented Generation (RAG)
pipeline using LangChain Expression Language (LCEL).

Pipeline:
    User Question
          │
          ▼
      Retriever
          │
          ▼
 Retrieved Documents
          │
          ▼
   Format Context
          │
          ▼
   Prompt Template
          │
          ▼
     Gemini LLM
          │
          ▼
   Output Parser
          │
          ▼
     Final Response

Author:
    Shravan Kumar Pandey
"""

from __future__ import annotations

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    Runnable,
    RunnablePassthrough,
)

from src.exception import handle_exception
from src.llm.gemini_model import GeminiLLM
from src.logger import get_logger
from src.prompts.prompt_template import PromptTemplateFactory
from src.utils.text import format_documents

logger = get_logger(__name__)


class RAGChain:
    """
    Factory class for creating the RAG chain.
    """

    def __init__(self, retriever) -> None:
        """
        Initialize the RAG chain.
        """

        self.retriever = retriever
        self.prompt = PromptTemplateFactory.get_rag_prompt()
        self.llm = GeminiLLM.get_llm()
        self.output_parser = StrOutputParser()

        self._chain: Runnable | None = None

        logger.info("RAGChain initialized.")

    # ------------------------------------------------------------------
    # Build
    # ------------------------------------------------------------------

    def build(self) -> Runnable:
        """
        Build the LCEL RAG chain.
        """

        try:

            if self._chain is None:

                self._chain = (
                    {
                        "context": self.retriever | format_documents,
                        "question": RunnablePassthrough(),
                    }
                    | self.prompt
                    | self.llm
                    | self.output_parser
                )

                logger.info(
                    "RAG chain built successfully."
                )

            return self._chain

        except Exception as e:

            raise handle_exception(
                "Failed to build RAG chain.",
                e,
            ) from e

    # ------------------------------------------------------------------
    # Invoke
    # ------------------------------------------------------------------

    def invoke(
        self,
        question: str,
    ) -> str:
        """
        Execute the RAG chain.
        """

        try:

            logger.info("Executing RAG chain.")

            response = self.build().invoke(question)

            logger.info(
                "Response generated successfully."
            )

            return str(response)

        except Exception as e:

            raise handle_exception(
                "Failed to execute RAG chain.",
                e,
            ) from e