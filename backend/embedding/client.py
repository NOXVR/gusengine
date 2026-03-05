# backend/embedding/client.py
# V10 TEI embedding client with thread-safe pool management
import asyncio
import os
import httpx
import logging
import threading
from typing import Optional

logger = logging.getLogger(__name__)

# AUDIT FIX (P10-17): Read TEI_BASE_URL from env var — operator can point to
# external TEI server without editing backend code. Docker Compose sets the default.
TEI_BASE_URL = os.environ.get("TEI_BASE_URL", "http://tei:80")

# AUDIT FIX (P3-05): Persistent httpx client instead of per-call instantiation.
# During bulk ingestion (100K+ chunks), creating/destroying an HTTP client per
# embed call exhausts ephemeral ports and accumulates TIME_WAIT sockets.
_http_client: httpx.AsyncClient | None = None

# AUDIT FIX (P7-13 + DT-P9-01): Asyncio lock for pool flush serialization.
# P7-13: Without a lock, concurrent coroutines can double-close the httpx client.
# DT-P9-01: Deferred initialization — asyncio.Lock() at module scope crashes on
# Python 3.10+ because no event loop exists during import. Lazy init on first use.
_client_lock: asyncio.Lock | None = None
# AUDIT FIX (P10-04): Thread-safe double-checked locking for lazy asyncio.Lock init.
_client_lock_init = threading.Lock()


async def _get_client_lock() -> asyncio.Lock:
    global _client_lock
    if _client_lock is None:
        with _client_lock_init:
            if _client_lock is None:
                _client_lock = asyncio.Lock()
    return _client_lock


async def _flush_embed_client():
    """AUDIT FIX (P7-13): Serialized pool flush for concurrent failure safety."""
    lock = await _get_client_lock()
    async with lock:
        global _http_client
        if _http_client is not None and not _http_client.is_closed:
            await _http_client.aclose()
            _http_client = None


async def _get_client() -> httpx.AsyncClient:
    # AUDIT FIX (P10-02): Lock-protect client initialization. Without the lock,
    # _flush_embed_client() can close a client between the caller's _get_client()
    # return and their subsequent client.post() — causing use-after-close errors
    # during TEI crash recovery when concurrent embed requests are in-flight.
    lock = await _get_client_lock()
    async with lock:
        global _http_client
        if _http_client is None or _http_client.is_closed:
            # AUDIT FIX (P5-05): Explicit pool limits prevent unbounded connection growth
            # during bulk ingestion. 100 max connections is generous for single-TEI setups;
            # 20 max keepalive prevents idle socket accumulation.
            # AUDIT FIX (P6-08): Reduced timeout from 30s to 10s (connect: 5s) — fail-fast
            # on stale keep-alive connections after TEI container restart.
            _http_client = httpx.AsyncClient(
                timeout=httpx.Timeout(10.0, connect=5.0),
                limits=httpx.Limits(max_connections=100, max_keepalive_connections=20),
            )
        return _http_client


async def close_embed_client():
    """AUDIT FIX (P5-05 + P8-06): Graceful shutdown — close persistent httpx client.
    P8-06: Route through _client_lock to prevent race with _flush_embed_client()
    during concurrent shutdown + TEI failure."""
    lock = await _get_client_lock()
    async with lock:
        global _http_client
        if _http_client is not None and not _http_client.is_closed:
            await _http_client.aclose()
            _http_client = None


async def embed_text(
    text: str,
    base_url: str = TEI_BASE_URL,
) -> tuple[list[float], Optional[dict]]:
    """Generate dense and sparse embeddings via TEI.

    TEI's BGE-M3 model exposes:
      - POST /embed         → dense vectors (1024-dim)
      - POST /embed_sparse  → sparse vectors (token_id: weight pairs)

    IMPORTANT: TEI must be started with a model that supports sparse output.
    BGE-M3 supports this natively. Verify with:
      curl -s http://127.0.0.1:8080/info | python3 -c "import sys,json; print(json.load(sys.stdin))"
    The response should include "sparse" in the model's capabilities.

    Returns:
        (dense_vector, sparse_vector) where sparse_vector may be None
        if TEI version doesn't support /embed_sparse.
    """
    # AUDIT FIX (GP7-05): Wrap all TEI calls in connection-aware error handler.
    # After a TEI crash, httpx keeps dead TCP sockets in the connection pool.
    # Without flushing, each subsequent request hangs for 10s (P6-08 timeout),
    # fails, and the next request picks another dead socket — cycling through
    # the entire pool before recovery. Flushing forces fresh connections.
    # AUDIT FIX (P11-08): _get_client() moved inside try — constructor failure
    # now triggers pool flush instead of leaving corrupt state.
    try:
        client = await _get_client()
        # Dense embedding
        dense_response = await client.post(
            f"{base_url}/embed",
            json={"inputs": text},
        )
        dense_response.raise_for_status()
        dense_vector = dense_response.json()[0]  # List[float], 1024-dim

        # Sparse embedding
        sparse_vector = None
        try:
            sparse_response = await client.post(
                f"{base_url}/embed_sparse",
                json={"inputs": text},
            )
            sparse_response.raise_for_status()
            sparse_data = sparse_response.json()[0]  # List[{index, value}]
            sparse_vector = {
                "indices": [entry["index"] for entry in sparse_data],
                "values": [entry["value"] for entry in sparse_data],
            }
        except (httpx.HTTPStatusError, KeyError) as e:
            # TEI version may not support sparse; degrade to dense-only
            logger.warning(f"TEI /embed_sparse failed ({e}) — falling back to dense-only search")

        return dense_vector, sparse_vector
    except (httpx.ConnectError, httpx.ReadTimeout, RuntimeError) as e:
        # AUDIT FIX (GP7-05 + P7-13): TEI is down — flush dead sockets via
        # lock-protected helper to prevent race condition under concurrent failures.
        logger.warning(f"TEI connection failure ({type(e).__name__}) — flushing httpx pool")
        await _flush_embed_client()
        raise
