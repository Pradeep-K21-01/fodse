"""
backend/app/schemas/response.py
Pydantic response models for all API routes.
"""

from pydantic import BaseModel
from typing import Optional, List


class SourceItem(BaseModel):
    law:          str
    text_preview: str


class LawyerAdvice(BaseModel):
    specialization: str
    suggestion:     str
    legal_aid:      dict


class QueryResponse(BaseModel):
    query_language:    str
    english_query:     str
    answer:            str
    translated_answer: str
    model_used:        str
    sources:           List[SourceItem]
    lawyer_advice:     LawyerAdvice
    is_fraud:          bool
    channel:           str


class UploadResponse(BaseModel):
    filename:    str
    status:      str
    chunks_added: int
    message:     str


class VoiceResponse(BaseModel):
    transcript:        str
    detected_language: str
    answer:            str
    translated_answer: str
    tts_audio_url:     Optional[str]
    model_used:        str


class LawyerResponse(BaseModel):
    specialization: str
    suggestion:     str
    legal_aid:      dict
