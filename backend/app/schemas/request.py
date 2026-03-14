"""
backend/app/schemas/request.py
Pydantic request models for all API routes.
"""

from pydantic import BaseModel, Field
from typing import Optional


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=2000,
                          example="What happens if a cheque bounces?")
    language: str = Field(default="auto",
                          description="auto | english | tamil | hindi | malayalam")
    channel:  str = Field(default="chat",
                          description="chat | voice | sms")


class LawyerSearchRequest(BaseModel):
    query:    str            = Field(..., example="I need a divorce lawyer in Chennai")
    city:     Optional[str]  = Field(default=None, example="Chennai")
    language: str            = Field(default="english")
