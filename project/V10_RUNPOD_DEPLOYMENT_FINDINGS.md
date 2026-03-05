# V10 RunPod Deployment Findings — Proposed Architecture Additions

> **Date:** 2026-03-01
> **Context:** First full deployment of V10 prototype on RunPod (A100-80GB). 514 PDFs ingested over ~12 hours. These findings represent operational gaps discovered during live deployment that should be integrated into ARCHITECTURE_V10.md.

---

## 1. Qdrant File Descriptor Limit (CRITICAL)

**Discovery:** Qdrant deadlocked during bulk ingestion (~74 failures). Root cause: default `ulimit -n 1024` is insufficient. Qdrant opens file descriptors per shard segment; with 500+ PDFs generating 4,000+ points across 8 segments, the fd limit was exhausted.

**Fix Applied:** `ulimit -n 65535` on the pod.

**Architecture Addition Required:**

```yaml
# docker-compose.yml — Qdrant service
qdrant:
  ulimits:
    nofile:
      soft: 65535
      hard: 65535
```

Also add to `start_all.sh` if used outside Docker:
```bash
ulimit -n 65535
```

---

## 2. Pipeline Throttling for Bulk Ingestion (CRITICAL)

**Discovery:** Running ingestion with `INGEST_SEMAPHORE=2` and `EMBED_SEMAPHORE=8` overwhelmed Qdrant, causing it to become unresponsive and lose ~674 indexed points.

**Fix Applied (pipeline.py):**
- `INGEST_SEMAPHORE`: 2 → 1 (sequential PDF processing)
- `EMBED_SEMAPHORE`: 8 → 4
- Added 250ms `asyncio.sleep` after each successful Qdrant upsert

**Architecture Addition Required:** These throttle values should be the permanent defaults in `pipeline.py`, not the original values. The throughput cost (~79s/PDF vs ~30s) is acceptable given zero failures vs 74 failures.

---

## 3. `/api/stats` Source Count Pagination (BUG FIX)

**Discovery:** Frontend showed "219 Sources" instead of 500. The `/api/stats` endpoint used `scroll(limit=500)` which only read the first 500 points out of 4,115. Sources from the remaining points were never counted.

**Fix Applied (main.py):** Replaced single scroll with paginated loop using `offset`/`next_offset` to iterate all points.

**Architecture Addition Required:** Update the `/api/stats` code block in ARCHITECTURE_V10.md to use the paginated version.

---

## 4. Illustration-Only PDF Handling (DOCUMENTATION)

**Discovery:** 14 of 514 PDFs produced zero extractable text. All are illustration/drawing-only files (parts diagrams, wiring harness drawings, reference drawings). Docling OCR correctly identifies them as having no textual content.

**Known Blanks:**
- `*-990 Illustrated Table *.pdf` (parts illustrations)
- `*-990 Illustrations *.pdf` (system illustrations)
- `54.1-112.7 Main Wiring Harness.pdf`
- `61.1-050 Frame Floor Reference Drawing.pdf`
- `88.1-1 Fenders, Bumpers, Engine Hood, Radiator Shell.pdf`

**Architecture Addition Required:** Document this as expected behavior. These PDFs contain diagnostic value only as visual references — they will be addressed when the frontend PDF viewer citation display is implemented (V10 dual-layer architecture).

---

## 5. Volume PDF Deduplication (QUALITY)

**Discovery:** The corpus contains both individual section PDFs AND compilation volumes (e.g., `91_92_Electrical_volume_1.pdf` = 385 chunks, `00_Maintenance_Service_volume_1.pdf` = 166 chunks). These volumes contain duplicate content from individual section PDFs, wasting RAG budget on redundant chunks during search.

**Architecture Addition Required:** Either:
- (a) Exclude volume PDFs from ingestion if all constituent sections exist as individual PDFs, OR
- (b) Implement deduplication at the chunk level via content hashing before indexing

---

## 6. GPU Memory Management After Crash (OPERATIONAL)

**Discovery:** After killing/restarting vLLM, orphaned `VLLM::EngineCore` processes can retain GPU memory allocation, preventing new instances from starting. Requires manual `kill -9` of orphaned CUDA processes.

**Architecture Addition Required:** Add to operational runbook:
```bash
# Clear orphaned GPU processes after vLLM crash
nvidia-smi | grep -i "vllm\|python" | awk '{print $5}' | xargs -r kill -9
```

---

## 7. Corpus Statistics (BASELINE)

Final ingestion metrics for the 514-PDF Mercedes FSM corpus:

| Metric | Value |
|:-------|:------|
| Total PDFs | 514 |
| Successfully indexed | 500 |
| Legitimate blanks | 14 |
| Total Qdrant points | 4,115 |
| Total tokens indexed | 808,472 |
| Avg chunks per PDF | 8.2 |
| Avg tokens per chunk | 196 |
| Largest source | `91_92_Electrical_volume_1.pdf` (385 chunks) |
| Ingestion time (throttled) | ~12 hours |
| Qdrant segments | 8 |
