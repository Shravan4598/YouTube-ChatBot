"""
Logging configuration for the YouTube Chatbot RAG application.

This module provides a centralized logger that writes logs to both
the console and a rotating log file.

Usage:
    from src.logger import get_logger

    logger = get_logger(__name__)
    logger.info("Application started")
"""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from src.config import settings
from src.constants import (
    LOGGER_NAME,
    LOG_FORMAT,
    DATE_FORMAT,
)

# ==============================================================================
# Log Directory
# ==============================================================================

LOG_DIR = Path(settings.LOG_PATH)
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "youtube_chatbot.log"


# ==============================================================================
# Logger Factory
# ==============================================================================

def get_logger(name: str = LOGGER_NAME) -> logging.Logger:
    """
    Return a configured logger instance.

    If the logger has already been created, the existing instance is
    returned without adding duplicate handlers.

    Args:
        name (str):
            Logger name.

    Returns:
        logging.Logger:
            Configured logger instance.
    """

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(settings.LOG_LEVEL.upper())

    formatter = logging.Formatter(
        fmt=LOG_FORMAT,
        datefmt=DATE_FORMAT,
    )

    # --------------------------------------------------------------------------
    # Console Handler
    # --------------------------------------------------------------------------

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # --------------------------------------------------------------------------
    # Rotating File Handler
    # --------------------------------------------------------------------------

    file_handler = RotatingFileHandler(
        filename=LOG_FILE,
        maxBytes=5 * 1024 * 1024,   # 5 MB
        backupCount=5,
        encoding="utf-8",
    )

    file_handler.setFormatter(formatter)

    # --------------------------------------------------------------------------
    # Add Handlers
    # --------------------------------------------------------------------------

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logger.propagate = False

    return logger