"""
backend/app/api/routes/voice.py
POST /voice/query  — Receive audio, transcribe with Whisper,
                     run legal AI, return TTS audio URL.

Called by:
  - React frontend (VoiceInput.jsx)
  - Asterisk AGI script (process_query.py)
"""

import os
import uuid
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from app.schemas.response import VoiceResponse
from app.core.config import settings

router = APIRouter()

TTS_DIR = Path(settings.TTS_OUTPUT_DIR)
TTS_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/query", response_model=VoiceResponse, summary="Voice legal question")
async def voice_query(
    audio:    UploadFile = File(...),
    language: str        = Form(default="auto"),
):
    """
    Upload a voice recording (.wav / .mp3).
    Returns transcription + legal answer + TTS audio file URL.
    """
    # Validate audio type
    allowed = {".wav", ".mp3", ".ogg", ".webm", ".m4a"}
    ext = Path(audio.filename).suffix.lower()
    if ext not in allowed:
        raise HTTPException(status_code=400, detail=f"Unsupported audio format: {ext}")

    # Save audio to temp file
    audio_bytes = await audio.read()
    tmp_id      = uuid.uuid4().hex
    tmp_path    = Path(f"/tmp/voice_query_{tmp_id}{ext}")
    tmp_path.write_bytes(audio_bytes)

    try:
        # 1. Transcribe with Whisper
        from voice_sms.speech_to_text import transcribe_audio
        stt_result = transcribe_audio(str(tmp_path), language=language)

        transcript    = stt_result["text"]
        detected_lang = stt_result["detected_language"]

        if not transcript.strip():
            raise HTTPException(status_code=422, detail="Could not transcribe audio. Please speak clearly.")

        # 2. Run AI engine
        from app.services.query_service import ask_legal_question
        result = ask_legal_question(
            question = transcript,
            language = detected_lang,
            channel  = "voice",
        )

        answer     = result["translated_answer"]
        model_used = result["model_used"]

        # 3. Generate TTS response
        tts_filename = f"reply_{tmp_id}.mp3"
        tts_path     = TTS_DIR / tts_filename

        from voice_sms.text_to_speech import synthesize
        synthesize(answer, language=detected_lang, save_path=str(tts_path))

        tts_url = f"/voice/audio/{tts_filename}"

        return VoiceResponse(
            transcript        = transcript,
            detected_language = detected_lang,
            answer            = result["answer"],
            translated_answer = answer,
            tts_audio_url     = tts_url,
            model_used        = model_used,
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Voice processing failed: {str(e)}")
    finally:
        tmp_path.unlink(missing_ok=True)


@router.get("/audio/{filename}", summary="Download TTS audio file")
async def get_audio(filename: str):
    """Serve TTS audio file generated from voice query."""
    audio_path = TTS_DIR / filename
    if not audio_path.exists():
        raise HTTPException(status_code=404, detail="Audio file not found.")
    return FileResponse(str(audio_path), media_type="audio/mpeg")
