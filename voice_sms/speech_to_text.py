"""
voice_sms/speech_to_text.py
Multilingual Speech-to-Text using OpenAI Whisper.
Supports: English, Tamil, Hindi, Malayalam

Install: pip install openai-whisper torch soundfile
Run: python -m voice_sms.speech_to_text
"""

import os
import whisper
import tempfile
from pathlib import Path
from ai.utils.language_detector import get_whisper_language_code


# Model sizes: tiny | base | small | medium | large
# Recommended: 'small' — good balance of speed + accuracy
WHISPER_MODEL_SIZE = os.getenv("WHISPER_MODEL", "small")

_model = None


def get_whisper_model():
    """Load Whisper model once (singleton pattern)."""
    global _model
    if _model is None:
        print(f"[Whisper] Loading '{WHISPER_MODEL_SIZE}' model ...")
        _model = whisper.load_model(WHISPER_MODEL_SIZE)
        print("[Whisper] Ready ✅")
    return _model


def transcribe_audio(audio_path: str, language: str = "auto") -> dict:
    """
    Transcribe audio file to text.

    Args:
        audio_path : path to .wav / .mp3 / .ogg file
        language   : 'auto' | 'english' | 'tamil' | 'hindi' | 'malayalam'

    Returns:
        dict with:
            text
            detected_language
            whisper_language_code
            duration_seconds
    """

    model = get_whisper_model()

    # Convert our language name → Whisper language code
    whisper_lang = None if language == "auto" else get_whisper_language_code(language)

    options = {
        "fp16": False,  # safer for CPU
    }

    if whisper_lang:
        options["language"] = whisper_lang

    result = model.transcribe(audio_path, **options)

    transcript = result["text"].strip()
    detected_lang_code = result.get("language", "en")

    # Map Whisper code → our language names
    code_to_lang = {
        "en": "english",
        "ta": "tamil",
        "hi": "hindi",
        "ml": "malayalam",
    }

    detected_lang = code_to_lang.get(detected_lang_code, "english")

    return {
        "text": transcript,
        "detected_language": detected_lang,
        "whisper_language_code": detected_lang_code,
        "duration_seconds": result.get("duration", 0),
    }


def transcribe_bytes(audio_bytes: bytes, language: str = "auto") -> dict:
    """
    Transcribe raw audio bytes (API upload / IVR call).
    """

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name

    try:
        return transcribe_audio(tmp_path, language)
    finally:
        Path(tmp_path).unlink(missing_ok=True)