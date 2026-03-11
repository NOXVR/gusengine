# backend/routes/ingest_direct.py
# Direct text chunk ingestion endpoint — bypasses Docling for digital PDFs
import uuid
import logging
from fastapi import APIRouter
from pydantic import BaseModel
from backend.embedding.client import embed_text
from backend.ingestion.qdrant_setup import index_chunk
from backend.shared.clients import qdrant_ingest_client

router = APIRouter()
logger = logging.getLogger(__name__)


class ChunkPayload(BaseModel):
    text: str
    source: str
    page_numbers: list[int] = []
    headings: list[str] = []
    token_count: int = 0


class IngestChunksRequest(BaseModel):
    chunks: list[ChunkPayload]
    collection_name: str
    pdf_path_key: str  # Used for deterministic UUID generation


@router.post("/api/ingest-chunks")
async def ingest_chunks(req: IngestChunksRequest):
    """Ingest pre-extracted text chunks directly (bypass Docling).
    
    Accepts chunks with text/metadata, embeds via TEI, indexes in Qdrant.
    Used when text is extracted client-side (e.g., PyMuPDF for digital PDFs).
    """
    indexed = 0
    errors = []
    
    for i, chunk in enumerate(req.chunks):
        chunk_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"{req.pdf_path_key}_{i}"))
        
        try:
            dense_vector, sparse_vector = await embed_text(chunk.text)
            
            chunk_dict = {
                "text": chunk.text,
                "source": chunk.source,
                "page_numbers": chunk.page_numbers,
                "headings": chunk.headings,
                "token_count": chunk.token_count,
            }
            
            index_chunk(
                qdrant_ingest_client, chunk_dict, chunk_id,
                dense_vector, sparse_vector,
                collection_name=req.collection_name,
            )
            indexed += 1
        except Exception as e:
            errors.append(f"Chunk {i}: {str(e)[:100]}")
            logger.error(f"Failed to index chunk {i}: {e}")
            if len(errors) > 10:
                break  # Circuit breaker
    
    logger.info(f"Direct ingest: {indexed}/{len(req.chunks)} chunks indexed to {req.collection_name}")
    return {
        "status": "ok" if not errors else "partial",
        "indexed": indexed,
        "total": len(req.chunks),
        "errors": errors[:5],
    }
