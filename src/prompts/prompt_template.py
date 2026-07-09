"""
Prompt templates for the YouTube Chatbot RAG application.

This module defines reusable prompt templates used by the RAG pipeline.

Author:
    Shravan Kumar Pandey
"""

from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate

from src.logger import get_logger

logger = get_logger(__name__)


class PromptTemplateFactory:
    """
    Factory class for creating prompt templates.
    """

    @staticmethod
    def get_rag_prompt() -> ChatPromptTemplate:
        """
        Create the RAG prompt template.
        """

        logger.info("Creating RAG prompt template.")

        return ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
You are an intelligent AI assistant that answers questions ONLY from the provided YouTube transcript.

Instructions:

- Use ONLY the supplied transcript context.
- Never invent facts.
- Never use outside knowledge.
- If the answer is not available in the transcript, reply exactly:

"I couldn't find the answer in the provided video transcript."

- Keep answers accurate and concise.
- If appropriate, answer with bullet points.
- Preserve names, numbers, dates and code exactly.
- Answer in the same language as the user's question.
- If the question requires reasoning, reason only from the transcript.

Transcript Context:
--------------------
{context}
--------------------
""",
                ),
                (
                    "human",
                    "{question}",
                ),
            ]
        )

    @staticmethod
    def get_system_prompt() -> str:
        """
        Return only the system prompt.
        """

        return (
            "You are a helpful AI assistant. "
            "Answer ONLY from the supplied transcript."
        )

    @staticmethod
    def get_chat_prompt() -> ChatPromptTemplate:
        """
        Prompt template for general chat.
        """

        logger.info("Creating chat prompt.")

        return ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
You are a helpful AI assistant.
Answer politely and accurately.
""",
                ),
                (
                    "human",
                    "{question}",
                ),
            ]
        )