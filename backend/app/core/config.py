"""
backend/app/core/config.py
Central configuration — reads from .env file.

Install: pip install python-dotenv
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # App
    APP_NAME: str = "Legal AI Assistant"
    DEBUG: bool   = os.getenv("DEBUG", "false").lower() == "true"

    # CORS — allow React dev server
    ALLOWED_ORIGINS: list = [
        "http://localhost:5173",   # Vite dev server
        "http://localhost:3000",   # fallback
        "*",                       # remove in production
    ]

    # Qdrant
    QDRANT_URL: str      = os.getenv("QDRANT_URL", "http://localhost:6333")

    # Gemini
    GEMINI_API_KEY: str  = os.getenv("GEMINI_API_KEY", "")

    # Ollama / Phi-3
    OLLAMA_URL: str      = os.getenv("OLLAMA_URL", "http://localhost:11434")
    LLM_MODE: str        = os.getenv("LLM_MODE", "auto")

    # Whisper
    WHISPER_MODEL: str   = os.getenv("WHISPER_MODEL", "small")

    # TTS
    TTS_OUTPUT_DIR: str  = os.getenv("TTS_OUTPUT_DIR", "/tmp/tts_audio")

    # File upload
    UPLOAD_DIR: str      = os.getenv("UPLOAD_DIR", "/tmp/uploads")
    MAX_FILE_SIZE_MB: int = 20

settings = Settings()