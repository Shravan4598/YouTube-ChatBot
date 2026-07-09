"""
Streamlit frontend for YouTube Chatbot.

Author:
    Shravan Kumar Pandey
"""

from __future__ import annotations

import streamlit as st

from src.config import settings
from src.pipeline.rag_pipeline import RAGPipeline
from src.logger import get_logger


def main():
    logger = get_logger(__name__)

    # --------------------------------------------------------
    # Page Configuration
    # --------------------------------------------------------
    st.set_page_config(
        page_title=settings.PAGE_TITLE,
        page_icon=settings.PAGE_ICON,
        layout=settings.LAYOUT,
        initial_sidebar_state="expanded",
    )

    # --------------------------------------------------------
    # Custom CSS
    # --------------------------------------------------------
    st.markdown(
        """
        <style>
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
        header { visibility: hidden; }

        .block-container {
            padding-top: 1rem;
            padding-bottom: 2rem;
            padding-left: 2rem;
            padding-right: 2rem;
        }

        .main-title {
            font-size: 40px;
            font-weight: bold;
            text-align: center;
            margin-bottom: 5px;
        }

        .sub-title {
            font-size: 18px;
            text-align: center;
            color: gray;
            margin-bottom: 30px;
        }

        .chat-user {
            padding: 15px;
            background: #1E88E5;
            border-radius: 10px;
            margin-top: 15px;
            margin-bottom: 10px;
            color: white;
        }

        .chat-bot {
            padding: 15px;
            background: #262730;
            border-radius: 10px;
            margin-bottom: 20px;
            color: white;
        }

        .stButton>button {
            width: 100%;
            height: 3em;
            font-size: 16px;
            font-weight: bold;
            border-radius: 10px;
        }

        .stTextInput>div>div>input {
            border-radius: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # Session State
    # --------------------------------------------------------
    if "pipeline" not in st.session_state:
        st.session_state.pipeline = None

    if "video_loaded" not in st.session_state:
        st.session_state.video_loaded = False

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "youtube_url" not in st.session_state:
        st.session_state.youtube_url = ""

    # --------------------------------------------------------
    # Helper Functions
    # --------------------------------------------------------
    def initialize_pipeline():
        if st.session_state.pipeline is None:
            logger.info("Initializing RAG Pipeline")
            st.session_state.pipeline = RAGPipeline()

    def clear_chat():
        st.session_state.chat_history = []

    def add_chat(question: str, answer: str):
        st.session_state.chat_history.append(
            {
                "question": question,
                "answer": answer,
            }
        )

    # --------------------------------------------------------
    # Header
    # --------------------------------------------------------
    st.markdown(
        '<div class="main-title">🎥 YouTube Chatbot</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sub-title">Ask questions from any YouTube '
        "video's transcript using Google Gemini + RAG</div>",
        unsafe_allow_html=True,
    )

    # ==========================================================
    # Sidebar
    # ==========================================================
    with st.sidebar:
        st.title("⚙️ Settings")
        st.markdown("---")

        st.markdown("### 📹 YouTube Video")

        youtube_url = st.text_input(
            label="YouTube URL",
            placeholder="https://www.youtube.com/watch?v=...",
            value=st.session_state.youtube_url,
        )

        process_video = st.button("🚀 Process Video", type="primary")

        st.markdown("---")
        st.markdown("### 💬 Chat")

        clear_history = st.button("🗑 Clear Chat")

        if clear_history:
            clear_chat()
            st.success("Chat history cleared.")

        st.markdown("---")
        st.markdown("### 📊 Status")

        if st.session_state.video_loaded:
            st.success("✅ Video Ready")
        else:
            st.warning("⚠️ No video loaded")

        st.markdown("---")
        st.markdown(
            """
            ### 🤖 Model

            **LLM**
            Google Gemini

            **Embeddings**
            Google Embedding-004

            **Vector Database**
            FAISS

            **Framework**
            LangChain
            """
        )

    # ==========================================================
    # Process Video
    # ==========================================================
    if process_video:
        if youtube_url.strip() == "":
            st.error("Please enter a YouTube URL.")
            st.stop()

        try:
            initialize_pipeline()

            with st.spinner("📥 Downloading transcript..."):
                st.session_state.pipeline.build(youtube_url)

            st.session_state.youtube_url = youtube_url
            st.session_state.video_loaded = True

            st.success("Video processed successfully!")
            logger.info("Video processed successfully.")

        except Exception as e:
            logger.exception(e)
            st.session_state.video_loaded = False
            st.error(str(e))

    # ==========================================================
    # Main Area
    # ==========================================================
    left_col, right_col = st.columns([3, 1])

    with left_col:
        st.subheader("💬 Ask Questions")

        question = st.text_input(
            label="Ask a question about the video",
            label_visibility="collapsed",
            placeholder="Ask anything about this video...",
        )

        ask_button = st.button("Ask", type="primary")

    with right_col:
        st.metric(
            label="Conversation",
            value=len(st.session_state.chat_history),
        )

        if st.session_state.video_loaded:
            st.metric(label="Pipeline", value="Ready")
        else:
            st.metric(label="Pipeline", value="Not Ready")

    st.markdown("---")

    # ==========================================================
    # Generate Response
    # ==========================================================
    if ask_button:
        if not st.session_state.video_loaded:
            st.warning("Please process a YouTube video first.")

        elif question.strip() == "":
            st.warning("Please enter a question.")

        else:
            try:
                with st.spinner("🤖 Gemini is thinking..."):
                    answer = st.session_state.pipeline.ask(question)

                add_chat(question, answer)
                st.rerun()

            except Exception as e:
                logger.exception(e)
                st.error(str(e))

    # ==========================================================
    # Chat History
    # ==========================================================
    if st.session_state.chat_history:
        st.subheader("💬 Conversation")

        for idx, chat in enumerate(
            reversed(st.session_state.chat_history), start=1
        ):
            with st.container():
                st.markdown(
                    f"""
                    <div class="chat-user">
                    <b>🙋 You</b><br><br>
                    {chat["question"]}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.markdown(
                    f"""
                    <div class="chat-bot">
                    <b>🤖 Gemini</b><br><br>
                    {chat["answer"]}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                col1, col2, col3 = st.columns([1, 1, 6])

                with col1:
                    if st.button("📋", key=f"copy_{idx}", help="Copy Answer"):
                        st.code(chat["answer"])

                with col2:
                    if st.button(
                        "❌", key=f"delete_{idx}", help="Delete Conversation"
                    ):
                        original_index = len(st.session_state.chat_history) - idx

                        if 0 <= original_index < len(st.session_state.chat_history):
                            st.session_state.chat_history.pop(original_index)

                        st.rerun()

                st.markdown("<br>", unsafe_allow_html=True)

    else:
        st.info(
            """
            Welcome!

            Steps:
            1. Paste a YouTube URL.
            2. Click **Process Video**.
            3. Ask questions about the video.

            Supported Languages:
            - English
            - Hindi
            - Auto-generated subtitles
            """
        )

    


if __name__ == "__main__":
    main()