# backend/shared/clients.py
# Shared service client singletons
import os
from qdrant_client import QdrantClient

# AUDIT FIX (P10-16): Separate QdrantClient instances for search and ingest.
# httpx.Client (used internally by synchronous QdrantClient) is NOT thread-safe.
# Chat dispatches hybrid_search via _SEARCH_POOL (ThreadPoolExecutor) and ingestion
# dispatches index_chunk via asyncio.to_thread() — both use different OS threads.
# A single shared instance risks corrupted HTTP connection state.
qdrant_search_client = QdrantClient(url=os.environ.get("QDRANT_URL", "http://qdrant:6333"))
qdrant_ingest_client = QdrantClient(url=os.environ.get("QDRANT_URL", "http://qdrant:6333"))
# Legacy alias retained for backward compatibility in routes that import by old name
qdrant_client = qdrant_search_client
# AUDIT FIX (P11-15): Client separation documentation.
# IMPORTANT: qdrant_search_client is for read-only operations (hybrid_search).
# qdrant_ingest_client is for write operations (index_chunk, create_collection, delete).
# Never swap them — httpx.Client is not thread-safe across pool boundaries.
