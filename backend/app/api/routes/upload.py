"""
backend/app/api/routes/upload.py
POST /upload/pdf  — Upload a new legal PDF and ingest into Qdrant.

Allows users to upload their own legal documents (FIR copy, contract, etc.)
and ask questions about them.
"""

import os
import uuid
import sys
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schemas.response import UploadResponse
from app.core.config import settings

router = APIRouter()

UPLOAD_DIR = Path(settings.UPLOAD_DIR)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Max file size: 20 MB
MAX_BYTES = settings.MAX_FILE_SIZE_MB * 1024 * 1024


@router.post("/pdf", response_model=UploadResponse, summary="Upload a legal PDF")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF legal document.
    It will be converted to text, chunked, and added to the vector database
    so you can ask questions about it immediately.
    """
    # Validate file type
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    # Read and validate size
    content = await file.read()
    if len(content) > MAX_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Max size: {settings.MAX_FILE_SIZE_MB} MB"
        )

    # Save file with unique name
    safe_name  = f"{uuid.uuid4().hex}_{file.filename}"
    save_path  = UPLOAD_DIR / safe_name
    save_path.write_bytes(content)

    # Process through ingestion pipeline
    try:
        chunks_added = _ingest_uploaded_pdf(save_path)
        return UploadResponse(
            filename     = file.filename,
            status       = "success",
            chunks_added = chunks_added,
            message      = f"Document ingested successfully. {chunks_added} chunks added to knowledge base.",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")


def _ingest_uploaded_pdf(pdf_path: Path) -> int:
    """
    Run the full ingestion pipeline on a single uploaded PDF.
    Returns number of chunks added to Qdrant.
    """
    import pdfplumber
    import uuid as _uuid
    from sentence_transformers import SentenceTransformer
    from qdrant_client import QdrantClient
    from qdrant_client.models import PointStruct

    # 1. Extract text
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text and text.strip():
                pages.append(text.strip())
    full_text = "\n\n".join(pages)

    # 2. Chunk (500 words, 50 overlap)
    words  = full_text.split()
    chunks = []
    step   = 450
    for i in range(0, len(words), step):
        chunk = " ".join(words[i : i + 500])
        if chunk.strip():
            chunks.append(chunk.strip())

    if not chunks:
        raise ValueError("No text could be extracted from the PDF.")

    # 3. Embed
    model   = SentenceTransformer("BAAI/bge-small-en-v1.5")
    vectors = model.encode(chunks, normalize_embeddings=True).tolist()

    # 4. Upload to Qdrant
    client = QdrantClient(url=settings.QDRANT_URL)
    points = [
        PointStruct(
            id      = str(_uuid.uuid4()),
            vector  = vectors[i],
            payload = {
                "text":   chunks[i],
                "law":    f"Uploaded: {pdf_path.name}",
                "source": pdf_path.stem,
                "chunk_id": i,
            }
        )
        for i in range(len(chunks))
    ]
    client.upsert(collection_name="legal_docs", points=points)
    return len(chunks)
