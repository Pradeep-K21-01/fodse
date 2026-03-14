"""
backend/app/core/security.py
Basic API key security middleware (optional but scaffolded).
Currently open — enable API_KEY_REQUIRED=true in .env to protect routes.
"""

import os
from fastapi import Header, HTTPException
from app.core.config import settings


API_KEY_REQUIRED = os.getenv("API_KEY_REQUIRED", "false").lower() == "true"
API_KEY          = os.getenv("API_KEY", "legal-ai-dev-key")


async def verify_api_key(x_api_key: str = Header(default=None)):
    """
    Optional API key check.
    Add header:  X-API-Key: your_key
    to any request when API_KEY_REQUIRED=true.
    """
    if not API_KEY_REQUIRED:
        return  # open access in dev mode
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key.")