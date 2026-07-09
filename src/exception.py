"""
Custom exception module for the YouTube Chatbot RAG application.

This module defines a reusable application-specific exception that
captures detailed debugging information including:

- File name
- Function name
- Line number
- Original exception

Author:
    Shravan Kumar Pandey
"""

from __future__ import annotations

import traceback
from typing import Optional

from src.logger import get_logger

logger = get_logger(__name__)


class YouTubeChatbotException(Exception):
    """
    Base exception class for the YouTube Chatbot application.

    Attributes:
        message (str):
            Human-readable error message.

        original_exception (Exception | None):
            Original exception that caused this error.
    """

    def __init__(
        self,
        message: str,
        original_exception: Optional[Exception] = None,
    ) -> None:
        """
        Initialize the custom exception.

        Args:
            message:
                Custom error message.

            original_exception:
                Original exception, if any.
        """
        self.message = message
        self.original_exception = original_exception

        super().__init__(self.__str__())

    def __str__(self) -> str:
        """
        Return a detailed error message.

        Returns:
            str
        """

        if self.original_exception is None:
            return self.message

        tb = traceback.extract_tb(
            self.original_exception.__traceback__
        )[-1]

        return (
            f"\n"
            f"Error Message : {self.message}\n"
            f"Exception     : {type(self.original_exception).__name__}\n"
            f"File          : {tb.filename}\n"
            f"Function      : {tb.name}\n"
            f"Line          : {tb.lineno}\n"
            f"Reason        : {self.original_exception}"
        )


def handle_exception(
    message: str,
    exception: Exception,
) -> YouTubeChatbotException:
    """
    Log and wrap an exception.

    Args:
        message:
            Custom message.

        exception:
            Original exception.

    Returns:
        YouTubeChatbotException
    """

    app_exception = YouTubeChatbotException(
        message=message,
        original_exception=exception,
    )

    logger.exception(app_exception)

    return app_exception