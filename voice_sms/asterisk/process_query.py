#!/usr/bin/env python3
"""
voice-sms/asterisk/process_query.py
Asterisk AGI script — bridges phone call to Legal AI FastAPI backend.

Called by Asterisk after recording the caller's voice question.
Steps:
  1. Read audio file path + language from Asterisk
  2. POST audio to FastAPI /voice/query endpoint
  3. Save TTS reply audio for Asterisk to play back

Install: pip install requests
"""

import sys
import os
import requests
from pathlib import Path

FASTAPI_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


def agi_read():
    """Read Asterisk AGI environment variables."""
    env = {}
    while True:
        line = sys.stdin.readline().strip()
        if not line:
            break
        if ":" in line:
            key, val = line.split(":", 1)
            env[key.strip()] = val.strip()
    return env


def agi_send(command: str):
    """Send command to Asterisk."""
    sys.stdout.write(command + "\n")
    sys.stdout.flush()
    return sys.stdin.readline().strip()


def main():
    # Read AGI vars
    agi_env = agi_read()

    # Args passed from dialplan: UNIQUEID LANG
    args     = sys.argv[1:] if len(sys.argv) > 1 else []
    uniqueid = args[0] if len(args) > 0 else agi_env.get("agi_uniqueid", "unknown")
    language = args[1] if len(args) > 1 else "auto"

    audio_path = f"/tmp/legal_query_{uniqueid}.wav"
    reply_path = f"/tmp/legal_reply_{uniqueid}.mp3"

    if not Path(audio_path).exists():
        agi_send(f'VERBOSE "Audio file not found: {audio_path}" 1')
        sys.exit(1)

    # POST to FastAPI voice endpoint
    try:
        with open(audio_path, "rb") as f:
            resp = requests.post(
                f"{FASTAPI_URL}/voice/query",
                files={"audio": ("query.wav", f, "audio/wav")},
                data={"language": language},
                timeout=60,
            )
        resp.raise_for_status()
        data = resp.json()

        # Download TTS audio reply
        tts_url = data.get("tts_audio_url")
        if tts_url:
            tts_resp = requests.get(f"{FASTAPI_URL}{tts_url}", timeout=30)
            Path(reply_path).write_bytes(tts_resp.content)
            agi_send(f'VERBOSE "TTS saved: {reply_path}" 1')
        else:
            agi_send('VERBOSE "No TTS URL in response" 1')

    except Exception as e:
        agi_send(f'VERBOSE "FastAPI call failed: {e}" 1')
        sys.exit(1)


if __name__ == "__main__":
    main()