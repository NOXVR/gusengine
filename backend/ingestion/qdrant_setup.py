# backend/ingestion/qdrant_setup.py
# Qdrant collection creation and chunk indexing
# V10 SPEC: Hybrid dense + sparse vectors with conditional sparse handling
from qdrant_client import QdrantClient, models  # AUDIT FIX (DT-P9-02): models needed for PointStruct
from qdrant_client.models import (
    VectorParams, SparseVectorParams, Distance,
    SparseIndexParams,
)


def create_collection(client: QdrantClient, collection_name: str = "fsm_corpus"):
    """Create Qdrant collection with hybrid dense + sparse vectors."""
    client.create_collection(
        collection_name=collection_name,
        vectors_config={
            "dense": VectorParams(
                size=1024,           # BGE-M3 dense dimension
                distance=Distance.COSINE,
                on_disk=False,       # Keep in RAM for speed
            )
        },
        sparse_vectors_config={
            "sparse": SparseVectorParams(
                index=SparseIndexParams(on_disk=False),
                modifier=None,  # BGE-M3 sparse output is pre-weighted (SPLADE-like); no additional IDF needed
            )
        },
    )


def index_chunk(client: QdrantClient, chunk: dict, chunk_id: str,
                dense_vector: list[float], sparse_vector: dict | None):
    """Index a single chunk with both dense and sparse vectors."""
    # AUDIT FIX (DT-P8-06): Conditionally construct vector dict.
    # When TEI degrades, sparse_vector is None or {"indices":[], "values":[]}.
    # Qdrant's Rust backend rejects empty SparseVector arrays with HTTP 400,
    # crashing the entire ingestion pipeline via the circuit breaker.
    vector_data = {"dense": dense_vector}
    if sparse_vector and sparse_vector.get("indices"):
        vector_data["sparse"] = {
            "indices": sparse_vector["indices"],
            "values": sparse_vector["values"],
        }
    # AUDIT FIX (DT-P9-02): Use models.PointStruct instead of raw dict.
    # qdrant-client >= 1.7.0 enforces Pydantic validation.
    # Raw dicts crash with ValidationError or AttributeError, halting ingestion.
    client.upsert(
        collection_name="fsm_corpus",
        points=[models.PointStruct(
            id=chunk_id,
            vector=vector_data,
            payload={
                "text": chunk["text"],
                "source": chunk["source"],
                "page_numbers": chunk["page_numbers"],
                "headings": chunk["headings"],
                "token_count": chunk["token_count"],
            }
        )]
    )
