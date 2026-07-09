"""
Application-wide constants for the YouTube Chatbot RAG project.

This module contains constants that are used throughout the application.
Avoid hardcoding values in other modules.
"""

from pathlib import Path

# ==============================================================================
# Project Information
# ==============================================================================

PROJECT_NAME = "YouTube Chatbot RAG"

PROJECT_VERSION = "1.0.0"

AUTHOR = "Shravan Kumar Pandey"

AUTHOR_EMAIL = "shravankumarpandey825412@gmail.com"

LICENSE = "MIT"

DESCRIPTION = (
    "Production-ready YouTube Chatbot using "
    "Google Gemini, LangChain, FAISS, and Streamlit."
)

# ==============================================================================
# Directory Names
# ==============================================================================

ASSETS_DIR_NAME = "assets"

CACHE_DIR_NAME = "cache"

LOGS_DIR_NAME = "logs"

VECTOR_STORE_DIR_NAME = "vector_store"

DATA_DIR_NAME = "data"

# ==============================================================================
# YouTube
# ==============================================================================

SUPPORTED_YOUTUBE_DOMAINS = (
    "youtube.com",
    "www.youtube.com",
    "m.youtube.com",
    "youtu.be",
)

SUPPORTED_TRANSCRIPT_LANGUAGES = [
    "hi",
    "en",
]

# ==============================================================================
# Text Splitter
# ==============================================================================

DEFAULT_CHUNK_SIZE = 1000

DEFAULT_CHUNK_OVERLAP = 200

# ==============================================================================
# Retriever
# ==============================================================================

DEFAULT_TOP_K = 4

SEARCH_TYPE = "similarity"

# ==============================================================================
# Vector Store
# ==============================================================================

VECTOR_STORE_FOLDER = "faiss_index"

FAISS_INDEX_NAME = "index"

METADATA_FILE = "metadata.pkl"

# ==============================================================================
# Prompt
# ==============================================================================

SYSTEM_PROMPT = """
You are an intelligent AI assistant.

Answer the user's question ONLY using the provided context.

If the answer is not available in the context, politely say:

'I couldn't find the answer in the provided video transcript.'

Guidelines:

- Give accurate answers.
- Be concise.
- Explain clearly.
- Do not hallucinate.
- If possible, answer in the same language as the user's question.

Context:
{context}

Question:
{question}

Answer:
"""

# ==============================================================================
# Streamlit
# ==============================================================================

PAGE_TITLE = "🎥 YouTube Chatbot"

PAGE_ICON = "🎥"

LAYOUT = "wide"

SIDEBAR_STATE = "expanded"

# ==============================================================================
# Chat Messages
# ==============================================================================

WELCOME_MESSAGE = """
👋 Welcome to the YouTube Chatbot!

Paste a YouTube video URL.

The application will:

• Extract transcript

• Create embeddings

• Build a FAISS vector database

• Answer your questions using Google Gemini.
"""

EMPTY_CHAT_MESSAGE = (
    "Please process a YouTube video before asking questions."
)

PROCESSING_MESSAGE = (
    "Processing video..."
)

SUCCESS_MESSAGE = (
    "Video processed successfully."
)

# ==============================================================================
# Error Messages
# ==============================================================================

INVALID_URL_ERROR = (
    "Please enter a valid YouTube URL."
)

INVALID_VIDEO_ID_ERROR = (
    "Unable to extract the YouTube Video ID."
)

TRANSCRIPT_NOT_FOUND_ERROR = (
    "Transcript is unavailable for this video."
)

VECTOR_STORE_ERROR = (
    "Vector store has not been created."
)

EMPTY_QUESTION_ERROR = (
    "Please enter your question."
)

GOOGLE_API_KEY_ERROR = (
    "GOOGLE_API_KEY is missing. Please check your .env file."
)

# ==============================================================================
# Logging
# ==============================================================================

LOGGER_NAME = "youtube_chatbot"

LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)s | "
    "%(filename)s | "
    "%(funcName)s | "
    "%(lineno)d | "
    "%(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# ==============================================================================
# Streamlit Session Keys
# ==============================================================================

SESSION_MESSAGES = "messages"

SESSION_VECTOR_STORE = "vector_store"

SESSION_RETRIEVER = "retriever"

SESSION_CHAT_HISTORY = "chat_history"

SESSION_VIDEO_URL = "video_url"

SESSION_TRANSCRIPT = "transcript"

SESSION_PROCESSED = "processed"

# ==============================================================================
# File Names
# ==============================================================================

CHAT_HISTORY_FILE = "chat_history.json"

TRANSCRIPT_CACHE_FILE = "transcript_cache.json"

# ==============================================================================
# Default Paths
# ==============================================================================

ROOT_DIR = Path(__file__).resolve().parent.parent

ASSETS_PATH = ROOT_DIR / ASSETS_DIR_NAME

CACHE_PATH = ROOT_DIR / CACHE_DIR_NAME

LOGS_PATH = ROOT_DIR / LOGS_DIR_NAME

VECTOR_STORE_PATH = ROOT_DIR / VECTOR_STORE_DIR_NAME