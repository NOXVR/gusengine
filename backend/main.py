# backend/main.py
# V10 SPEC: FastAPI application with startup/shutdown hooks
import asyncio
import logging
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from backend.shared.clients import qdrant_ingest_client, qdrant_search_client
from backend.ingestion.qdrant_setup import create_collection
from backend.routes import health, chat, ingest, upload, ledger

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="GusEngine",
    description="Closed-Loop Automotive Diagnostic RAG Engine",
    version="10.0.0-prototype",
)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Prototype: allow all. Production: restrict to frontend origin.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(health.router)
app.include_router(chat.router)
app.include_router(ingest.router)
app.include_router(upload.router)
app.include_router(ledger.router)

# Static file serving for PDFs (used by frontend citation modal)
_PDF_DIR = os.environ.get("ALLOWED_PDF_DIR", os.path.join(os.path.dirname(os.path.dirname(__file__)), "storage", "pdfs"))
if os.path.isdir(_PDF_DIR):
    app.mount("/pdfs", StaticFiles(directory=_PDF_DIR), name="pdfs")


# Prototype frontend serving
FRONTEND_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "prototype.html")


@app.get("/")
async def serve_frontend():
    """Serve the prototype frontend."""
    if os.path.isfile(FRONTEND_PATH):
        return FileResponse(FRONTEND_PATH, media_type="text/html")
    return {"message": "Frontend not found. Use /docs for API documentation."}


@app.get("/api/stats")
async def stats():
    """Return Qdrant collection stats for the frontend."""
    try:
        info = qdrant_search_client.get_collection("fsm_corpus")
        points = info.points_count
        # Count distinct sources
        from qdrant_client import models
        import asyncio
        sources = set()
        offset = None
        while True:
            result = qdrant_search_client.scroll(
                collection_name="fsm_corpus",
                limit=1000,
                offset=offset,
                with_payload=["source"],
                with_vectors=False,
            )
            batch, next_offset = result
            for p in batch:
                src = p.payload.get("source", "")
                if src:
                    sources.add(src)
            if next_offset is None:
                break
            offset = next_offset
        return {"points": points, "sources": len(sources)}
    except Exception as e:
        return {"points": 0, "sources": 0, "error": str(e)}


# AUDIT FIX (P3-03): Collection auto-creation at startup.
@app.on_event("startup")
async def ensure_qdrant_collection():
    """Create collection if it doesn't exist. Retry on transient failure."""
    # AUDIT FIX (P5-08): Extended from 5→10 attempts with 60s cap to outlast large persistence loads.
    for attempt in range(10):
        try:
            qdrant_ingest_client.get_collection("fsm_corpus")
            logger.info("Qdrant collection 'fsm_corpus' verified.")
            return
        except Exception:
            try:
                create_collection(qdrant_ingest_client)
                logger.info("Qdrant collection 'fsm_corpus' created.")
                return
            except Exception as e:
                wait = min(2 ** attempt, 60)  # Cap at 60 seconds per wait
                logger.warning(f"Qdrant not ready (attempt {attempt+1}/10): {e}")
                await asyncio.sleep(wait)
    logger.critical("FATAL: Could not verify/create Qdrant collection after 10 attempts (~5 min).")
    raise SystemExit("Qdrant collection setup failed — aborting startup.")


# AUDIT FIX (P5-05): Graceful shutdown — close persistent httpx connections.
@app.on_event("shutdown")
async def cleanup_clients():
    """Close persistent httpx clients and thread pools to prevent leaks."""
    from backend.embedding.client import close_embed_client
    from backend.inference.llm import _flush_llm_client
    from backend.routes.chat import _SEARCH_POOL

    await close_embed_client()
    # AUDIT FIX (P9-03): Close LLM httpx client on shutdown.
    await _flush_llm_client()
    # AUDIT FIX (P9-09): Shut down search thread pool. Non-blocking (wait=False)
    # so blocked Qdrant HTTP calls don't delay container exit.
    _SEARCH_POOL.shutdown(wait=False)
    # AUDIT FIX (P10-30): Close Qdrant clients to prevent TCP socket leak.
    await asyncio.to_thread(qdrant_search_client.close)
    await asyncio.to_thread(qdrant_ingest_client.close)
    logger.info("All httpx clients, thread pools, and Qdrant clients closed.")
