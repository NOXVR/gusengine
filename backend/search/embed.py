# backend/search/embed.py
# BGE-M3 embedding via TEI
import os
import logging
import httpx

logger = logging.getLogger(__name__)

TEI_BASE_URL = os.environ.get("TEI_BASE_URL", "http://tei:80")

# Persistent httpx client singleton
_embed_client: httpx.AsyncClient | None = None


async def _get_client() -> httpx.AsyncClient:
    global _embed_client
    if _embed_client is None or _embed_client.is_closed:
        _embed_client = httpx.AsyncClient(
            base_url=TEI_BASE_URL,
            timeout=60.0,
        )
    return _embed_client


async def embed_text(text: str) -> dict:
    """Embed text using TEI (BGE-M3).

    Returns dict with:
    - dense: list[float] (1024-dim)
    - sparse: dict with indices/values (or None if TEI doesn't return sparse)
    """
    client = await _get_client()
    try:
        # TEI /embed endpoint for dense vectors
        response = await client.post("/embed", json={
            "inputs": text,
            "truncate": True,
        })
        response.raise_for_status()
        dense = response.json()[0]  # TEI returns list of embeddings

        # TEI /embed_sparse endpoint for sparse vectors
        sparse = None
        try:
            sparse_response = await client.post("/embed_sparse", json={
                "inputs": text,
                "truncate": True,
            })
            sparse_response.raise_for_status()
            sparse_data = sparse_response.json()[0]
            if sparse_data:
                sparse = {
                    "indices": [item["index"] for item in sparse_data],
                    "values": [item["value"] for item in sparse_data],
                }
        except Exception as e:
            logger.warning(f"Sparse embedding failed (degraded mode): {e}")

        return {"dense": dense, "sparse": sparse}
    except Exception as e:
        logger.error(f"TEI embedding failed: {e}")
        raise
