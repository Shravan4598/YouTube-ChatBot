"""
Setup configuration for the YouTube Chatbot RAG project.

This file enables packaging and installation of the project using:

    pip install -e .

Author:
    Shravan Kumar Pandey
"""

from pathlib import Path
from typing import List

from setuptools import find_packages, setup

PROJECT_NAME = "youtube-chatbot-rag"
VERSION = "1.0.0"
AUTHOR = "Shravan Kumar Pandey"
AUTHOR_EMAIL = "shravankumarpandey825412@gmail.com"
DESCRIPTION = (
    "Production-ready YouTube Chatbot using Retrieval-Augmented Generation (RAG), "
    "Google Gemini, LangChain, FAISS, and Streamlit."
)

BASE_DIR = Path(__file__).parent
README_PATH = BASE_DIR / "README.md"
REQUIREMENTS_PATH = BASE_DIR / "requirements.txt"


def get_requirements(file_path: Path) -> List[str]:
    """
    Read dependencies from requirements.txt.

    Args:
        file_path (Path): Path to the requirements file.

    Returns:
        List[str]: List of package requirements.
    """
    requirements: List[str] = []

    if not file_path.exists():
        return requirements

    with file_path.open(encoding="utf-8") as file:
        for line in file:
            dependency = line.strip()

            if (
                dependency
                and not dependency.startswith("#")
                and dependency != "-e ."
            ):
                requirements.append(dependency)

    return requirements


LONG_DESCRIPTION = (
    README_PATH.read_text(encoding="utf-8")
    if README_PATH.exists()
    else DESCRIPTION
)

setup(
    name=PROJECT_NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    install_requires=get_requirements(REQUIREMENTS_PATH),
    python_requires=">=3.10",
    license="Apache",
    keywords=[
        "Generative AI",
        "RAG",
        "LangChain",
        "Gemini",
        "FAISS",
        "YouTube",
        "LLM",
        "Streamlit",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: Apache License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)