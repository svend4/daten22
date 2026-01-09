"""
RAG System Configuration for MBTI Documentation
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project Paths
ROOT_DIR = Path(__file__).parent.parent
DOCS_DIR = ROOT_DIR / "docs"
TYPES_DIR = ROOT_DIR / "types"
RAG_DIR = ROOT_DIR / "rag"
DATA_DIR = RAG_DIR / "data"
CHROMA_DIR = DATA_DIR / "chroma_db"

# Ensure directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
CHROMA_DIR.mkdir(parents=True, exist_ok=True)

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Model Configuration
EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
)
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-3.5-turbo")

# ChromaDB Configuration
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "mbti_docs")

# Document Processing
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))

# Search Configuration
TOP_K_RESULTS = int(os.getenv("TOP_K_RESULTS", "5"))

# Language
LANGUAGE = os.getenv("LANGUAGE", "russian")

# Supported File Types
SUPPORTED_EXTENSIONS = [".md", ".txt"]

# Prompts
SYSTEM_PROMPT = """Ты - эксперт по типологии личности MBTI и соционике.
Используй предоставленный контекст из документации для ответа на вопросы пользователя.

Правила:
1. Отвечай только на основе предоставленного контекста
2. Если информации недостаточно, честно скажи об этом
3. Используй примеры из документации
4. Будь конкретным и структурированным
5. Для технических терминов давай пояснения

Контекст:
{context}

Вопрос: {question}

Ответ:"""

QA_PROMPT_TEMPLATE = """На основе следующего контекста ответь на вопрос пользователя.

Контекст:
{context}

Вопрос: {question}

Детальный ответ на русском языке:"""
