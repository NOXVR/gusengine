# backend/search/hybrid_search.py
# V10 SPEC: Hybrid dense + sparse search with Qdrant native RRF fusion
import logging
from qdrant_client import QdrantClient
from qdrant_client.models import (
    SparseVector, FusionQuery, Fusion, Prefetch,
)

logger = logging.getLogger(__name__)


def hybrid_search(
    client: QdrantClient,
    query_dense: list[float],
    query_sparse: dict | None,  # AUDIT FIX (OP-P11-06): None when TEI sparse degrades
    top_k: int = 60,  # AUDIT FIX (P10-15): was 20, starves RAG budget (DT-P9-05)
    min_score_ratio: float = 0.70,
    min_absolute_score: float = 0.011,  # AUDIT FIX (P2-14): lowered from 0.013 — 0.013 rejected valid single-signal RRF matches (~0.0125)
    collection_name: str = "fsm_corpus",  # V10 FIREWALL: Vehicle-scoped collection
) -> list[dict]:
    """Execute hybrid dense + sparse search with RRF fusion.

    Args:
        query_dense: Dense embedding vector from BGE-M3
        query_sparse: Sparse vector from BGE-M3 (indices + values)
        top_k: Number of candidates from each signal before fusion
        min_score_ratio: Keep chunks scoring >= this fraction of top RRF score
        min_absolute_score: Absolute RRF score floor — discard ALL results if
            top score is below this value (handles off-topic queries)
        collection_name: Qdrant collection to search (vehicle-scoped firewall)

    Returns:
        List of chunks sorted by RRF score, filtered by dynamic threshold
    """
    # Qdrant native RRF fusion via query API
    # AUDIT FIX (DT-8): Build prefetch list conditionally. Qdrant's Rust backend
    # rejects empty SparseVector arrays with HTTP 400.
    prefetch_list = [
        Prefetch(
            query=query_dense,
            using="dense",
            limit=top_k,
        ),
    ]

    if query_sparse and query_sparse.get("indices"):
        prefetch_list.append(
            Prefetch(
                query=SparseVector(
                    indices=query_sparse["indices"],
                    values=query_sparse["values"],
                ),
                using="sparse",
                limit=top_k,
            )
        )
    else:
        logger.warning("Sparse vector unavailable — falling back to dense-only search")

    # AUDIT FIX (DT-P4-02): Qdrant requires ≥2 prefetch queries for RRF fusion.
    # When TEI sparse degrades, conditionally use direct query for fallback.
    if len(prefetch_list) >= 2:
        results = client.query_points(
            collection_name=collection_name,
            prefetch=prefetch_list,
            query=FusionQuery(fusion=Fusion.RRF),
            limit=top_k,
        )
    else:
        # Dense-only fallback — no fusion needed
        results = client.query_points(
            collection_name=collection_name,
            query=prefetch_list[0].query,
            using="dense",
            limit=top_k,
        )

    if not results.points:
        return []

    # AUDIT FIX (P5-04 + P6-04): Mode-adaptive absolute score floor.
    # RRF scores cluster in [0.0125, 0.0164] — 0.013 catches off-topic queries.
    # Dense cosine scores range [0, 1] — for BGE-M3, random-pair similarity
    # clusters at 0.25–0.45. P6-04 raised dense floor to 0.50.
    effective_min_absolute = min_absolute_score if len(prefetch_list) >= 2 else 0.50
    top_score = results.points[0].score
    if top_score < effective_min_absolute:
        logger.warning(
            f"Top score {top_score:.4f} below absolute floor {effective_min_absolute} "
            f"({'RRF' if len(prefetch_list) >= 2 else 'dense-only'} mode) — discarding all results"
        )
        return []

    # AUDIT FIX (DT-P8-07): Multiplicative ratios are DISABLED for BOTH modes.
    # RRF mode: A 0.70 ratio discards ALL single-signal matches, turning
    # hybrid search into a strict intersection. Rely on absolute floor + top_k.
    # Dense-only mode: Cosine scores range widely (0.3–1.0). A 0.70 ratio
    # brutally discards chunks that are still highly relevant.
    effective_ratio = 0.0  # AUDIT FIX (DT-P8-07)
    threshold = top_score * effective_ratio

    filtered = []
    for point in results.points:
        # AUDIT FIX (DT-P8-04): Apply absolute floor to EVERY chunk, not just top score.
        if point.score >= threshold and point.score >= effective_min_absolute:
            filtered.append({
                "text": point.payload["text"],
                "source": point.payload["source"],
                "page_numbers": point.payload["page_numbers"],
                "headings": point.payload["headings"],
                "token_count": point.payload["token_count"],
                "score": point.score,
            })

    # AUDIT FIX (GP7-11): Telemetry for threshold calibration.
    if not filtered and results.points:
        top_rejected = results.points[0].score
        logger.warning(
            f"SEARCH FILTER SUPPRESSION: {len(results.points)} chunks found but "
            f"all below threshold {threshold:.4f}. Top rejected score: {top_rejected:.4f}. "
            f"Consider adjusting min_absolute_score if this recurs."
        )

    return filtered
