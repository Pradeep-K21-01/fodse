"""
voice_sms/text_to_speech.py
Multilingual Text-to-Speech using gTTS (Google TTS).
Supports: English, Tamil, Hindi, Malayalam

Install: pip install gTTS playsound
"""

import os
import uuid
from pathlib import Path
from gtts import gTTS
from ai.utils.language_detector import get_tts_language_code

OUTPUT_DIR = Path(os.getenv("TTS_OUTPUT_DIR", "/tmp/tts_audio"))
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def synthesize(
    text: str,
    language: str = "english",
    slow: bool = False,
    save_path: str = None,
) -> str:

    lang_code = get_tts_language_code(language)

    tts = gTTS(text=text, lang=lang_code, slow=slow)

    if not save_path:
        filename = f"tts_{uuid.uuid4().hex[:8]}.mp3"
        save_path = str(OUTPUT_DIR / filename)

    tts.save(save_path)
    print(f"[TTS] Audio saved → {save_path} (lang: {language})")
    return save_path


def synthesize_for_sms_reply(text: str, language: str) -> str:
    short_text = text[:200] + ("..." if len(text) > 200 else "")
    return synthesize(short_text, language, slow=False)


def synthesize_bytes(text: str, language: str = "english") -> bytes:
    import io
    lang_code = get_tts_language_code(language)
    tts = gTTS(text=text, lang=lang_code, slow=False)
    buf = io.BytesIO()
    tts.write_to_fp(buf)
    buf.seek(0)
    return buf.read()


GREETINGS = {
    "english":   "Welcome to the Legal AI Assistant. Please ask your legal question after the beep.",
    "tamil":     "சட்ட AI உதவியாளரில் வரவேற்கிறோம். கீழே உங்கள் சட்ட கேள்வியை கேளுங்கள்.",
    "hindi":     "लीगल AI असिस्टेंट में आपका स्वागत है। कृपया बीप के बाद अपना कानूनी प्रश्न पूछें।",
    "malayalam": "ലീഗൽ AI അസിസ്റ്റന്റിലേക്ക് സ്വാഗതം. ബീപ്പിന് ശേഷം നിങ്ങളുടെ നിയമ ചോദ്യം ചോദിക്കുക.",
}


def get_ivr_greeting(language: str = "english") -> str:
    text = GREETINGS.get(language, GREETINGS["english"])
    return synthesize(text, language, slow=True)