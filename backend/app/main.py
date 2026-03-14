"""
backend/app/main.py
FastAPI application entry point.

Run: uvicorn app.main:app --reload --port 8000
Docs: http://localhost:8000/docs
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import query, upload, voice, lawyer
from app.core.config import settings

app = FastAPI(
    title       = "Legal AI Assistant API",
    description = "Multilingual Indian Legal AI — Tamil · Hindi · Malayalam · English",
    version     = "1.0.0",
    docs_url    = "/docs",
    redoc_url   = "/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins     = settings.ALLOWED_ORIGINS,
    allow_credentials = True,
    allow_methods     = ["*"],
    allow_headers     = ["*"],
)

app.include_router(query.router,  prefix="/query",  tags=["Query"])
app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(voice.router,  prefix="/voice",  tags=["Voice"])
app.include_router(lawyer.router, prefix="/lawyer", tags=["Lawyer"])

@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "app": "Legal AI Assistant", "docs": "/docs"}

@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}