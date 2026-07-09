"""
YouTube transcript loader.

This module is responsible for:

1. Validating YouTube URLs
2. Extracting the Video ID
3. Downloading transcripts
4. Supporting multilingual transcripts
5. Returning LangChain Documents

Author:
    Shravan Kumar Pandey
"""

from __future__ import annotations

from typing import List

from langchain_core.documents import Document
from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound,
)

from src.config import settings
from src.exception import handle_exception
from src.logger import get_logger
from src.utils.text import clean_text, join_transcript
from src.utils.youtube import extract_video_id
from src.utils.validators import (
    validate_transcript,
    validate_youtube_url,
)

logger = get_logger(__name__)


class YouTubeTranscriptLoader:
    """
    Production-ready YouTube transcript loader.
    """

    def __init__(self) -> None:
        self.languages = settings.TRANSCRIPT_LANGUAGES

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _fetch_transcript(
        self,
        video_id: str,
    ) -> tuple[list[dict], str]:
        """
        Fetch transcript.

        Priority:
        1. Preferred languages
        2. Auto-generated transcript
        """

        api = YouTubeTranscriptApi()

        transcript_list = api.list(video_id)

        # ------------------------------------------------------------
        # Preferred languages
        # ------------------------------------------------------------

        for language in self.languages:
            try:
                transcript = transcript_list.find_transcript([language])

                logger.info(
                    "Transcript found in language: %s",
                    language,
                )

                return list(transcript.fetch()), language

            except Exception:
                continue

        # ------------------------------------------------------------
        # Auto-generated transcript
        # ------------------------------------------------------------

        for transcript in transcript_list:
            if transcript.is_generated:

                logger.info(
                    "Using generated transcript (%s).",
                    transcript.language_code,
                )

                return (
                    list(transcript.fetch()),
                    transcript.language_code,
                )

        raise NoTranscriptFound(
            video_id,
            self.languages,
            transcript_list,
        )

    # ------------------------------------------------------------------
    # Public
    # ------------------------------------------------------------------

    def load(self, youtube_url: str) -> List[Document]:
        """
        Load transcript from a YouTube URL.

        Args:
            youtube_url:
                YouTube URL.

        Returns:
            List[Document]
        """

        try:

            validate_youtube_url(youtube_url)

            video_id = extract_video_id(youtube_url)

            logger.info(
                "Extracted Video ID: %s",
                video_id,
            )

            transcript, language = self._fetch_transcript(video_id)

            logger.info(
                "Transcript fetched successfully (%s).",
                language,
            )

            transcript_text = join_transcript(transcript)

            transcript_text = clean_text(transcript_text)

            validate_transcript(transcript_text)

            logger.info(
                "Transcript loaded successfully."
            )

            return [
                Document(
                    page_content=transcript_text,
                    metadata={
                        "source": youtube_url,
                        "video_id": video_id,
                        "language": language,
                        "document_type": "youtube_transcript",
                    },
                )
            ]

        except (
            TranscriptsDisabled,
            NoTranscriptFound,
        ) as e:

            raise handle_exception(
                "Transcript is unavailable for this video.",
                e,
            ) from e

        except Exception as e:

            raise handle_exception(
                "Failed to load YouTube transcript.",
                e,
            ) from e