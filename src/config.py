"""
Configuration module for the YouTube Chatbot RAG application.

This module centralizes all application settings, loads environment
variables, validates configuration, and creates required project
directories.

Author:
    Shravan Kumar Pandey
"""

from pathlib import Path

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# ==============================================================================
# Load Environment Variables
# ==============================================================================

load_dotenv()

# ==============================================================================
# Project Directories
# ==============================================================================

BASE_DIR = Path(__file__).resolve().parent.parent

ASSETS_DIR = BASE_DIR / "assets"
CACHE_DIR = BASE_DIR / "cache"
LOGS_DIR = BASE_DIR / "logs"
VECTOR_STORE_DIR = BASE_DIR / "vector_store"

for directory in (
    ASSETS_DIR,
    CACHE_DIR,
    LOGS_DIR,
    VECTOR_STORE_DIR,
):
    directory.mkdir(parents=True, exist_ok=True)


# ==============================================================================
# Application Settings
# ==============================================================================

class Settings(BaseSettings):
    """
    Application configuration loaded from the .env file.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ------------------------------------------------------------------
    # Google Gemini
    # ------------------------------------------------------------------

    GOOGLE_API_KEY: str = Field(...)

    GEMINI_MODEL: str = Field(
        default="gemini-2.5-flash"
    )

    EMBEDDING_MODEL: str = Field(
    default="models/gemini-embedding-001"
)

    # ------------------------------------------------------------------
    # LLM Parameters
    # ------------------------------------------------------------------

    TEMPERATURE: float = Field(default=0.3)

    MAX_OUTPUT_TOKENS: int = Field(default=2048)

    GEMINI_TOP_P: float = Field(default=0.95)

    GEMINI_TOP_K: int = Field(default=40)

    REQUEST_TIMEOUT: int = Field(default=120)

    MAX_RETRIES: int = Field(default=3)

    # ------------------------------------------------------------------
    # Text Splitter
    # ------------------------------------------------------------------

    CHUNK_SIZE: int = Field(default=1000)

    CHUNK_OVERLAP: int = Field(default=200)

    # ------------------------------------------------------------------
    # Retriever
    # ------------------------------------------------------------------

    RETRIEVER_TOP_K: int = Field(default=4)

    SEARCH_TYPE: str = Field(default="similarity")

    # ------------------------------------------------------------------
    # Transcript Languages
    # ------------------------------------------------------------------

    TRANSCRIPT_LANGUAGES: list[str] = Field(
    default_factory=lambda: [
        "hi",
        "en",
        "en-US",
        "en-GB",
    ]
    )

    # ------------------------------------------------------------------
    # Streamlit
    # ------------------------------------------------------------------

    PAGE_TITLE: str = Field(
        default="YouTube Chatbot"
    )

    PAGE_ICON: str = Field(
        default="🎥"
    )

    LAYOUT: str = Field(
        default="wide"
    )

    # ------------------------------------------------------------------
    # Paths
    # ------------------------------------------------------------------

    VECTOR_STORE_PATH: Path = VECTOR_STORE_DIR

    CACHE_PATH: Path = CACHE_DIR

    LOG_PATH: Path = LOGS_DIR

    # ------------------------------------------------------------------
    # Logging
    # ------------------------------------------------------------------

    LOG_LEVEL: str = Field(
        default="INFO"
    )


settings = Settings()