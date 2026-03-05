# V10 FIX APPLICATION AUDIT REPORT

**Auditor:** Hostile Audit — Adversarial Stress Test
**Date:** 2026-02-24
**Scope:** 25 Fixes (FIX-01 through FIX-25) applied to `ARCHITECTURE_V10.md`
**Ground Truth:** `V10_FIX_LIST.md`

---

## SUMMARY TABLE

| Fix ID | Applied? | Correct? | Regression? | New Contradiction? | Complete? | Verdict |
|:-------|:---------|:---------|:------------|:-------------------|:----------|:--------|
| FIX-01 | ✅ | ✅ | ✅ | ⚠️ | ⚠️ | WARN |
| FIX-02 | ✅ | ✅ | ✅ | ✅ | ✅ | PASS |
| FIX-03 | ✅ | ✅ | ✅ | ✅ | ✅ | PASS |
| FIX-04 | ✅ | ✅ | ✅ | ✅ | ⚠️ | WARN |
| FIX-05 | ✅ | ✅ | ✅ | ✅ | ✅ | PASS |
| FIX-06 | ✅ | ✅ | ✅ | ✅ | ✅ | PASS |
| FIX-07 | ✅ | ⚠️ | ✅ | ✅ | ⚠️ | WARN |
| FIX-08 | ✅ | ✅ | ⚠️ | ⚠️ | ⚠️ | WARN |
| FIX-09 | ✅ | ✅ | ✅ | ✅ | ✅ | PASS |
| FIX-10 | ✅ | ✅ | ✅ | ✅ | ✅ | PASS |
| FIX-11 | ✅ | ✅ | ⚠️ | ❌ | ❌ | FAIL |
| FIX-12 | ✅ | ✅ | ✅ | ✅ | ✅ | PASS |
| FIX-13 | ✅ | ✅ | ✅ | ✅ | ✅ | PASS |
| FIX-14 | ✅ | ✅ | ✅ | ✅ | ✅ | PASS |
| FIX-15 | ✅ | ✅ | ✅ | ✅ | ✅ | PASS |
| FIX-16 | ✅ | ✅ | ✅ | ✅ | ✅ | PASS |
| FIX-17 | ✅ | ✅ | ✅ | ✅ | ✅ | PASS |
| FIX-18 | ✅ | ✅ | ✅ | ✅ | ✅ | PASS |
| FIX-19 | ✅ | ✅ | ✅ | ✅ | ✅ | PASS |
| FIX-20 | ✅ | ✅ | ✅ | ✅ | ✅ | PASS |
| FIX-21 | ✅ | ✅ | ✅ | ✅ | ✅ | PASS |
| FIX-22 | ⚠️ | ❌ | ❌ | ❌ | ❌ | FAIL |
| FIX-23 | ✅ | ✅ | ✅ | ✅ | ✅ | PASS |
| FIX-24 | ✅ | ✅ | ✅ | ✅ | ✅ | PASS |
| FIX-25 | ✅ | ✅ | ✅ | ✅ | ✅ | PASS |

**Totals:** 18 PASS / 5 WARN / 2 FAIL

---

## PER-FIX DETAILED AUDIT

### FIX-01: Docker network `internal` contradiction — WARN

**Applied?** YES. Both locations modified.

- L136: CAUTION box updated to `"internal: true — containers cannot initiate outbound internet connections. Published ports bound to 127.0.0.1 still accept host connections via iptables DNAT."` ✅
- L295: `internal: true   # TRIAD FIX (OP-1): Air-gap enforcement — blocks container egress. 127.0.0.1 port bindings still work via iptables DNAT.` ✅

**Correct?** YES. The semantics are correct.

**Regression?** NO.

**New Contradiction?** MINOR. The CAUTION box at L136 specifically mentions `127.0.0.1` published ports. However, the frontend container at L276–277 publishes on `0.0.0.0` (no `127.0.0.1` prefix): `"443:443"` and `"80:80"`. This is *correct* behavior (the frontend must be externally accessible), but the CAUTION box's wording implies *only* `127.0.0.1`-bound ports work with `internal: true`. All published ports work — the CAUTION box is technically incomplete, not wrong.

**Complete?** MINOR GAP. See contradiction above.

---

### FIX-02: Embedding generation code — PASS

**Applied?** YES. Three new sections inserted.

- TEI Embedding Client at L570–631 (`embed_text()` function) ✅
- Ingestion Orchestration at L633–667 (`ingest_pdf()` function) ✅
- Query-time embedding note at L670–674 ✅

**Correct?** YES. Verified:
- `/embed` for dense, `/embed_sparse` for sparse ✅
- Sparse vector format conversion `[{index, value}]` → `{indices: [...], values: [...]}` matches Qdrant's `SparseVector` expectation ✅
- `embed_text()` is async, `parse_and_chunk()` is sync — correctly handled via `await embed_text()` inside the async `ingest_pdf()` ✅
- Query-time note at L672 matches function signature ✅
- `hybrid_search()` at L696–700 accepts `query_dense: list[float]` and `query_sparse: dict` — compatible with `embed_text()` output ✅

**Improvement over fix spec:** Architecture version adds module-level `import logging` and `logger` (L578–581) instead of the fix spec's inline `import logging` inside the except block. This is cleaner. Also adds `IngestionError` import and explicit docstring about error propagation. Also adds `logger.info()` on successful indexing (L665).

**Regression?** NO.
**New Contradiction?** NO.
**Complete?** YES.

---

### FIX-03: Missing model volume mount in `gusengine` — PASS

**Applied?** YES. L242: `- ./storage/models:/app/models:ro` present in gusengine volumes. ✅

**Correct?** YES. Path matches `AutoTokenizer.from_pretrained("/app/models/Qwen2.5-32B-Instruct-AWQ")` at L383.

**Regression?** NO.
**New Contradiction?** NO.
**Complete?** YES.

---

### FIX-04: EasyOCR runtime download violates air-gap — WARN

**Applied?** YES. All four locations modified.

- Pre-download script at L317–330 ✅
- Volume mount at L243: `- ./storage/easyocr_models:/app/.EasyOCR/model:ro` ✅
- Env var at L248: `EASYOCR_MODULE_PATH=/app/.EasyOCR` ✅
- `download_enabled=False` at L395 ✅

**Correct?** MOSTLY. Path consistency verified:
- Host pre-download writes to `./storage/easyocr_models` (L325) → volume mount source matches ✅
- Container mount target `/app/.EasyOCR/model` → env var `EASYOCR_MODULE_PATH=/app/.EasyOCR` → parent dir correct ✅

**UNVERIFIED:** `download_enabled=False` as a parameter of Docling's `EasyOcrOptions`. I cannot confirm this parameter exists in the Docling Python API. The fix spec included it, so the architecture correctly applied it, but if `EasyOcrOptions` does not accept `download_enabled`, this will raise a `TypeError` at import time.

**Deviation from fix spec:** The fix spec used `./storage/models/easyocr:/root/.EasyOCR/model:ro` and `EASYOCR_MODULE_PATH=/root/.EasyOCR`. The architecture uses `./storage/easyocr_models:/app/.EasyOCR/model:ro` and `/app/.EasyOCR`. The architecture's paths are internally consistent and arguably better (using `/app` prefix instead of `/root`), but deviate from the fix spec.

**Regression?** NO.
**New Contradiction?** NO.
**Complete?** WARN — `download_enabled=False` is UNVERIFIED.

---

### FIX-05: `validate_ledger.py` uses container paths but runs on host — PASS

**Applied?** YES. L1058–1070 shows env var fallback pattern.

**Correct?** YES. The architecture improves on the fix spec by defaulting to the *host* path `./storage/models/Qwen2.5-32B-Instruct-AWQ` (L1063) instead of the container path `/app/models/...`. Since `validate_ledger.py` is primarily a host tool, this is a better default. Also includes `local_files_only=True` per FIX-13.

**Deviation:** Fix spec's explicit usage comment (`# Host usage: TOKENIZER_MODEL_PATH=...`) is not present, but L1057 has `# TRIAD FIX (DT-4): Uses env var with fallback — runs on host OR in container` which captures the intent.

**Regression?** NO.
**New Contradiction?** NO.
**Complete?** YES.

---

### FIX-06: Frontend container missing Nginx config volume mount — PASS

**Applied?** YES. L281: `- ./config/nginx.conf:/etc/nginx/conf.d/default.conf:ro` ✅

**Correct?** YES. The architecture improves on the fix spec by mounting to `/etc/nginx/conf.d/default.conf` instead of `/etc/nginx/nginx.conf`. This is better practice — it injects a server block config without overriding the main `nginx.conf`, preserving Nginx's default `include conf.d/*.conf` directive.

**Regression?** NO.
**New Contradiction?** NO.
**Complete?** YES.

---

### FIX-07: Upload blocking regex targets dead AnythingLLM endpoint — WARN

**Applied?** YES, but with deviation. L1132 updated to reference `/api/ingest` blocking.

**Correct?** DEVIATION. The fix spec explicitly said to RETAIN the legacy `/api/v1/document/(upload|create-folder)` regex for "defense-in-depth" and ADD the new `/api/ingest` rule. The architecture at L1132 instead says the old regex "is no longer relevant" and only documents the new rule: `location /api/ingest { deny all; }`.

The fix spec text:
> - `/api/v1/document/(upload|create-folder)` (legacy V9, retained for defense-in-depth)
> - `/api/ingest` (V10 FastAPI ingestion endpoint)

The architecture text:
> Old AnythingLLM regex `/api/v1/document/(upload|create-folder)` is no longer relevant. New rule: `location /api/ingest { deny all; }`

**Impact:** Low. The old endpoint no longer exists in V10, so removing it has no security impact. But it deviates from the fix spec's defense-in-depth intent.

**Regression?** NO.
**Complete?** PARTIAL — defense-in-depth retention skipped.

---

### FIX-08: RRF 40% threshold is mathematically incoherent — WARN

**Applied?** YES. All three locations modified.

- L701: `min_score_ratio: float = 0.70` ✅
- L709: Docstring updated ✅
- L739–744: Comment block updated with RRF math explanation ✅

**Correct?** YES. Code is correct.

**Regression?** YES — cascading neglect.

**New Contradiction?** YES. The V10 changelog at **L40** still says:
```
Relevance threshold: Fixed 0.50 → Dynamic 40% of top score
```
This should now read `70%` (or "70% of top RRF score"). This changelog entry was NOT updated to reflect FIX-08's change from 40% to 70%.

**Complete?** PARTIAL — changelog not updated.

---

### FIX-09: Live Qdrant backup via tar = corruption risk — PASS

**Applied?** YES. L1159–1172. Backup strategy updated with Qdrant snapshot API first, tar excluding `storage/qdrant/`, and IMPORTANT callout box. ✅

**Correct?** YES. The cron command at L1167 correctly chains: (1) Qdrant snapshot, (2) stop gusengine, (3) tar with `--exclude=storage/qdrant`, (4) restart. ✅

**Regression?** NO.
**New Contradiction?** NO.
**Complete?** YES.

---

### FIX-10: VMDK daemon "PRESERVED UNCHANGED" contradiction — PASS

**Applied?** YES. L483–487 now reads "PRESERVED WITH TARGETED MODIFICATIONS" with the three changes enumerated. ✅

**Correct?** YES. Matches fix spec intent.
**Regression?** NO.
**New Contradiction?** NO.
**Complete?** YES.

---

### FIX-11: Ledger token cap contradictory across locations — FAIL

**Applied?** YES at primary locations:

- L253: `LEDGER_MAX_TOKENS=2550` ✅
- L842: Budget diagram shows `~2,550 tokens` for ledger ✅
- L845: Budget diagram shows `~26,318 tokens` for RAG ✅
- L1047: Tribal knowledge table shows `3,000 (adjusted: 2,550)` for ledger ✅
- L1072–1074: Validator shows `RAW_CAP = 3000`, `SAFETY_FACTOR = 0.85`, `ADJUSTED_CAP = int(RAW_CAP * SAFETY_FACTOR)  # = 2550` ✅
- L1081: Validator comment updated: `(count <= 2550)` ✅

**HOWEVER — THREE CASCADING FAILURES:**

**Failure 1 (SIGNIFICANT): Code comment in `build_context()` NOT updated.**
L800–802:
```python
# Default (chat_history_tokens=0): 32768 - 900 - 2000 - 2000 = 27,868 tokens for RAG
# Typical case (with ~1000 chat history): 26,868 tokens — see budget diagram below
# This is ~16.8× the V9 budget of 1,600 tokens
```
The fix spec (FIX-11 at its L396–402) required this to be changed to:
```python
# available ≈ 32768 - 900 - 2550 - 2000 - 0 = 27,318 tokens for RAG
# With chat history (~1000): 26,318 tokens ≈ 16.4× the V9 budget
```
**The comment still uses the OLD ledger value of 2000, yielding wrong math (27,868 instead of 27,318; 26,868 instead of 26,318; 16.8× instead of ~16.4×).** This is exactly the Cascading Neglect anti-pattern.

**Failure 2 (SIGNIFICANT): Budget diagram multiplier NOT updated.**
L854: `Improvement: 16.8× more context for diagnostic reasoning`

Correct math: 26,318 / 1,600 = **16.45×**, which should display as `~16.4×`.
The `16.8×` value corresponds to the old `26,868 / 1,600 = 16.79×`.

**Failure 3 (SIGNIFICANT): Tribal Knowledge comparison table RAG budget NOT updated.**
L1048: `| RAG budget | ~1,600 | ~26,868 |`

Should be `~26,318` (matches the budget diagram at L845). The old value `26,868` was computed with the 2000 ledger cap.

**Token Budget Verification (independent):**
```
32,768 (total)
 - 900 (system prompt)
 - 2,550 (ledger, adjusted cap)
 - 1,000 (chat history, typical)
 - 2,000 (response budget)
= 26,318 tokens for RAG ← CORRECT in diagram at L845
= 26,318 / 1,600 = 16.45× ← NOT reflected in L854 or L802
```

---

### FIX-12: IDF double-weighting on BGE-M3 sparse vectors — PASS

**Applied?** YES. Both locations modified.

- L540: `modifier=None,  # BGE-M3 sparse output is pre-weighted...` ✅
- L521–524: Import cleaned — `Modifier` removed ✅

**Correct?** YES.
**Regression?** NO.
**New Contradiction?** NO.
**Complete?** YES.

---

### FIX-13: Air-gap violations via AutoTokenizer and Docling Hub calls — PASS

**Applied?** YES. All locations modified.

- L254–255: `HF_HUB_OFFLINE=1` and `TRANSFORMERS_OFFLINE=1` added to gusengine env ✅
- L384–385: `local_files_only=True` in parser.py tokenizer ✅
- L774–775: `local_files_only=True` in context_builder.py tokenizer ✅
- L1068–1069: `local_files_only=True` in validate_ledger.py tokenizer ✅

**Correct?** YES. `local_files_only=True` with `trust_remote_code=True` works — the former prevents network requests while the latter allows executing locally-cached custom Python code. ✅

**Regression?** NO.
**New Contradiction?** NO.
**Complete?** YES.

---

### FIX-14: `parse_and_chunk()` has zero error handling — PASS

**Applied?** YES. Full error handling applied at L406–478.

- `IngestionError` class defined at L406–408 ✅
- `try/except` around `converter.convert()` at L427–432 ✅
- `doc is None` check at L435–437 ✅
- `try/except` around `chunker.chunk()` at L445–449 ✅
- Empty chunk filter at L454–455: `if not text or not text.strip(): continue` ✅
- Docstring updated with `Raises: IngestionError` at L420–422 ✅

**Correct?** YES. `IngestionError` is raised on all three failure paths (converter crash, empty document, chunker crash). The orchestration at L637 imports `IngestionError` and lets it propagate — this is by design (caller decides quarantine behavior).

**Note on `import logging` inside function body (L424):** Python caches module imports, so this works. Unconventional but not a bug. The fix spec explicitly placed it there.

**Note on `list(chunker.chunk(doc))` (L446):** Materializes the full iterator. For the prototype corpus (514 PDFs, ~2,442 pages), individual PDFs are small enough that this is safe. At scale (250K pages in a single PDF), this could OOM. Acceptable for prototype scope.

**Regression?** NO.
**New Contradiction?** NO.
**Complete?** YES.

---

### FIX-15: Multiple system messages may misbehave with Qwen2.5 — PASS

**Applied?** YES. L893–901 shows single system message with context appended.

```python
system_content = system_prompt
if context:
    system_content += f"\n\nRETRIEVED DOCUMENTS:\n\n{context}"

messages = [
    {"role": "system", "content": system_content},
]
```

**Correct?** YES. Context is appended to the single system message string. No second system-role message.

**Note:** The system message can now be very long (900 prompt + 26,318 RAG tokens). vLLM handles this correctly via PagedAttention — the chat template produces one `<|im_start|>system\n...<|im_end|>` block regardless of length.

**Regression?** NO.
**New Contradiction?** NO.
**Complete?** YES.

---

### FIX-16: `awq_marlin` quantization kernels for vLLM performance — PASS

**Applied?** YES. L167–168:
```yaml
--quantization awq_marlin
--dtype float16
```

**Correct?** YES. `awq_marlin` requires explicit `--dtype float16`. Both present. Compatible with `--tensor-parallel-size 2`. ✅

**Note on VRAM:** Marlin kernels may have slightly different memory overhead than GEMM kernels, but the difference is negligible relative to the 17.5 GB headroom. The VRAM budget table remains valid.

**Note on availability:** `awq_marlin` was introduced in vLLM v0.3.x and is well-established by 2026. UNVERIFIED against the exact `vllm/vllm-openai:latest` image tag, but expected to be present.

**Regression?** NO.
**New Contradiction?** NO.
**Complete?** YES.

---

### FIX-17: `table_structure_options` passed as dict instead of Pydantic model — PASS

**Applied?** YES.

- L374: `TableStructureOptions` added to import ✅
- L398: `table_structure_options=TableStructureOptions(mode=TableFormerMode.ACCURATE)` ✅

**Correct?** YES.
**Regression?** NO.
**New Contradiction?** NO.
**Complete?** YES.

---

### FIX-18: Citation `page` field type changed string→int without noting schema break — PASS

**Applied?** YES via Option 2 (keep integer, add note).

- L979: JSON example retains `"page": 3` (integer) ✅
- L1003: Note added: `"one schema adaptation: page field in source_citations is now an integer instead of V9's string "N/A" — renderCitation() handles both types via loose comparison"` ✅

**Correct?** YES. JavaScript loose comparison `citation.page !== "N/A"` will correctly handle integer `3` — it is not equal to `"N/A"` in either loose or strict mode. The note accurately documents the change.

**Regression?** NO.
**New Contradiction?** NO.
**Complete?** YES.

---

### FIX-19: Missing `import os` in `parser.py` — PASS

**Applied?** YES. L378: `import os` present in parser imports. ✅

**Correct?** YES. `os.path.basename(pdf_path)` at L472 now has its import.
**Regression?** NO.
**New Contradiction?** NO.
**Complete?** YES.

---

### FIX-20: Unused imports in `search.py` — PASS

**Applied?** YES. L692–694:
```python
from qdrant_client.models import (
    SparseVector, FusionQuery, Fusion, Prefetch,
)
```
`SearchRequest`, `NamedVector`, `NamedSparseVector`, and `Query` all removed. ✅

**Correct?** YES. `SparseVector` is used at L724. `FusionQuery`, `Fusion`, `Prefetch` are used at L718–732. All retained imports are used.

**Regression?** NO.
**New Contradiction?** NO.
**Complete?** YES.

---

### FIX-21: PDF.js downloaded from unofficial GitHub fork — PASS

**Applied?** YES. L335–340: npm pack method with official registry.
```bash
cd ./frontend && npm pack pdfjs-dist@4.0.379 && \
  tar xzf pdfjs-dist-4.0.379.tgz && ...
```

**Correct?** YES. Uses npm registry (verifiable checksums) instead of `github.com/nicbarker/pdfjs-dist`. ✅

**Regression?** NO.
**New Contradiction?** NO.
**Complete?** YES.

---

### FIX-22: Code comment "27,868" contradicts budget diagram "26,868" — FAIL

**Applied?** The fix spec says: "Already handled by FIX-11, which updates the comment to reflect the corrected ledger cap of 2,550." However, **FIX-11's code comment update was NOT applied.** See FIX-11 Failure 1 above.

L800–802 still reads:
```python
# Default (chat_history_tokens=0): 32768 - 900 - 2000 - 2000 = 27,868 tokens for RAG
# Typical case (with ~1000 chat history): 26,868 tokens — see budget diagram below
# This is ~16.8× the V9 budget of 1,600 tokens
```

This should read (per FIX-11 spec):
```python
# available ≈ 32768 - 900 - 2550 - 2000 - 0 = 27,318 tokens for RAG
# With chat history (~1000): 26,318 tokens ≈ 16.4× the V9 budget
```

**Verdict:** FAIL — the entire purpose of FIX-22 (resolving the comment/diagram contradiction) was NOT achieved because FIX-11's comment update was skipped.

---

### FIX-23: CPU OCR time estimate may be 2–6× too optimistic — PASS

**Applied?** YES. L679: `"estimated time is 20-60 hours"` with `"1-3 minutes/page with EasyOCR on CPU for faded/handwritten content"`. ✅

**Correct?** YES. Matches fix spec.
**Regression?** NO.
**New Contradiction?** NO.
**Complete?** YES.

---

### FIX-24: Missing `PYTORCH_CUDA_ALLOC_CONF` for VRAM stability — PASS

**Applied?** YES. L157: `- PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` ✅

**Correct?** YES. In vLLM environment block, immediately after `NVIDIA_VISIBLE_DEVICES=all`.
**Regression?** NO.
**New Contradiction?** NO.
**Complete?** YES.

---

### FIX-25: DOMPurify claim contradicts "PRESERVED UNCHANGED" renderGusResponse — PASS

**Applied?** YES. Both locations modified.

- L999: DOMPurify described as `"V10 ADDITION"` with V9 FROZEN reference ✅
- L1003: Changed from "PRESERVED UNCHANGED" to `"PRESERVED"` with explanation `"core logic unchanged; DOMPurify sanitization added as V10 hardening"` — the actual text combines this with FIX-18's schema adaptation note ✅

**Correct?** YES. The contradiction is resolved — DOMPurify is documented as a V10 addition, not a V9 preserve.
**Regression?** NO.
**New Contradiction?** NO.
**Complete?** YES.

---

## CROSS-CUTTING ANALYSIS

### A. Token Budget Coherence — FAIL

**Verification:**

| Check | Expected | Actual (Line) | Status |
|:------|:---------|:--------------|:-------|
| `LEDGER_MAX_TOKENS=2550` in env | 2550 | 2550 (L253) | ✅ |
| Budget diagram ledger | ~2,550 | ~2,550 (L842) | ✅ |
| Budget diagram RAG | ~26,318 | ~26,318 (L845) | ✅ |
| `build_context()` comment | 2550, 27,318, 26,318, ~16.4× | 2000, 27,868, 26,868, 16.8× (L800–802) | ❌ |
| Budget diagram multiplier | ~16.4× | 16.8× (L854) | ❌ |
| Tribal Knowledge table RAG | ~26,318 | ~26,868 (L1048) | ❌ |
| Validator `remaining` comment | (count <= 2550) | (count <= 2550) (L1081) | ✅ |

**Independent math:**
```
32768 - 900 - 2550 - 1000 (chat) - 2000 = 26,318 (with chat history)
32768 - 900 - 2550 - 0 (no chat) - 2000 = 27,318 (default/no chat)
26,318 / 1,600 = 16.45× ≈ 16.4× (NOT 16.8×)
```

**Impact:** An implementer reading the `build_context()` comment (L800–802) will believe the ledger cap is 2000 tokens and the RAG budget is 27,868 tokens. The actual env var says 2550 and the budget diagram says 26,318. This is a direct contradiction within the same section of code. At minimum it causes confusion; at worst, an implementer calibrates their ledger using the wrong budget.

---

### B. Air-Gap Coherence — PASS (with one UNVERIFIED item)

| Check | Status |
|:------|:-------|
| `internal: true` allows inter-container traffic? | ✅ Docker bridge internal networks allow container-to-container via Docker DNS |
| `EASYOCR_MODULE_PATH` matches volume mount? | ✅ Env: `/app/.EasyOCR`, mount: `:/app/.EasyOCR/model:ro` |
| `download_enabled=False` is real Docling API? | ⚠️ UNVERIFIED — cannot confirm against Docling source |
| `local_files_only=True` + `trust_remote_code=True` compatible? | ✅ Former blocks network, latter allows local custom code execution |
| Any remaining runtime internet code paths? | ✅ None found. `HF_HUB_OFFLINE=1`, `TRANSFORMERS_OFFLINE=1`, `local_files_only=True` on all tokenizers, `download_enabled=False` on EasyOCR, `internal: true` on Docker network |

**Impact:** If `download_enabled` is not a valid `EasyOcrOptions` parameter, the Docling converter initialization will crash with `TypeError`. This would be caught immediately on first startup.

---

### C. Embedding Pipeline Coherence — PASS

| Check | Status |
|:------|:-------|
| `embed_text()` uses `/embed` and `/embed_sparse`? | ✅ (L606–608, L616–618) |
| Sparse format conversion TEI→Qdrant? | ✅ `[{index, value}]` → `{indices: [...], values: [...]}` (L622–625) |
| `ingest_pdf()` connects parse→embed→index? | ✅ (L651–663) |
| Async/sync mixing handled? | ✅ `parse_and_chunk()` sync, `embed_text()` async with `await`, `ingest_pdf()` is async |
| Query-time embedding matches `embed_text()`? | ✅ (L672–673) |
| `hybrid_search()` accepts correct vector format? | ✅ `query_dense: list[float]`, `query_sparse: dict` (L697–699) |

---

### D. Error Handling Chain — PASS

| Check | Status |
|:------|:-------|
| `IngestionError` raised on all failure paths? | ✅ Converter failure (L432), empty doc (L437), chunker failure (L449) |
| `import logging` inside function body safe? | ✅ Python caches imports; unconventional but functional |
| `list(chunker.chunk(doc))` OOM risk? | ⚠️ MINOR — safe for prototype (514 PDFs). At scale, switch to streaming. |
| Empty chunk filter handles edge cases? | ✅ `if not text or not text.strip()` catches None, empty string, whitespace-only |
| `ingest_pdf()` catches or propagates `IngestionError`? | ✅ Propagates by design — documented in docstring (L649) |

---

### E. Docker Compose Consistency — PASS

| Check | Status |
|:------|:-------|
| YAML validity after all modifications? | ✅ Structure is consistent (proper indentation, syntax) |
| Volume mount path consistency? | ✅ `./storage/models` in vLLM (L154) and gusengine (L242) |
| Frontend Nginx config mount exists in YAML? | ✅ L281: `./config/nginx.conf:/etc/nginx/conf.d/default.conf:ro` |
| All containers on `gus_internal`? | ✅ vLLM (L176), TEI (L203), Qdrant (L222), gusengine (L261), frontend (L284) |
| `internal: true` compatible with frontend published ports? | ✅ Docker `internal` flag only blocks container-initiated egress, not published port DNAT |

---

### F. Inference Fix Coherence — PASS

| Check | Status |
|:------|:-------|
| Single long system message handled by vLLM? | ✅ PagedAttention handles arbitrary-length messages |
| `awq_marlin` requires `--dtype float16`? | ✅ Both present (L167–168) |
| `awq_marlin` compatible with TP=2? | ✅ Marlin kernels support tensor parallelism |
| VRAM budget still valid? | ✅ Marlin kernel overhead is negligible vs 17.5GB headroom |
| `awq_marlin` in vLLM Docker image? | ⚠️ UNVERIFIED against exact `latest` tag, but available since vLLM v0.3.x |

---

## FINDINGS TABLE

| # | Severity | Fix ID(s) | Summary | Evidence (Line #) | Recommended Fix |
|:--|:---------|:----------|:--------|:-------------------|:----------------|
| 1 | **SIGNIFICANT** | FIX-11, FIX-22 | `build_context()` comment still uses old ledger cap 2000, showing wrong RAG budget (27,868/26,868) and wrong multiplier (16.8×) | L800–802 | Replace with: `# available ≈ 32768 - 900 - 2550 - 2000 - 0 = 27,318 tokens for RAG` / `# With chat history (~1000): 26,318 tokens ≈ 16.4× the V9 budget` |
| 2 | **SIGNIFICANT** | FIX-11 | Budget diagram multiplier not updated | L854 | Change `16.8×` → `~16.4×` |
| 3 | **SIGNIFICANT** | FIX-11 | Tribal Knowledge comparison table RAG budget not updated | L1048 | Change `~26,868` → `~26,318` |
| 4 | **MINOR** | FIX-08 | V10 Changelog still says "Dynamic 40% of top score" | L40 | Change to `Dynamic 70% of top RRF score` |
| 5 | **MINOR** | FIX-07 | Legacy defense-in-depth regex dropped instead of retained | L1132 | Add: `Legacy V9 regex /api/v1/document/(upload|create-folder) retained for defense-in-depth.` |
| 6 | **MINOR** | FIX-01 | CAUTION box implies only `127.0.0.1` ports work with `internal: true` — frontend uses `0.0.0.0` | L136 | Add: `Non-localhost published ports (e.g., frontend 443/80) also function normally.` |
| 7 | **MINOR** | FIX-04 | `download_enabled=False` in `EasyOcrOptions` is UNVERIFIED against Docling API | L395 | Verify against Docling source. If invalid, remove parameter and rely on `EASYOCR_MODULE_PATH` + `internal: true` network to prevent downloads. |

---

## VRAM BUDGET VERIFICATION (Independent)

```
Component                              VRAM (GB)
────────────────────────────────────────────────
Qwen2.5-32B-AWQ weights (4-bit)         ~18.0
KV Cache @ 32K tokens                     ~8.0
  (64 layers × 8 KV heads × 128 dim
   × 32768 tokens × 2 (K+V) × 2 bytes
   = 8,192 MB)
vLLM overhead                             ~2.0
BGE-M3 (568M params, FP16)               ~2.0
TEI overhead                              ~0.5
────────────────────────────────────────────────
TOTAL                                    ~30.5 GB (64% of 48 GB)
HEADROOM                                 ~17.5 GB ✅
```

This matches the architecture's table at L100–112. No fix modified the VRAM budget, so no regression expected. Confirmed.

---

## AUDITOR INTEGRITY CHECKS

1. ☑ I did NOT recommend removing any pre-existing code or infrastructure
2. ☑ I did NOT recommend replacing the technology stack
3. ☑ Every finding references a specific fix ID (FIX-01 through FIX-25)
4. ☑ I independently verified the token budget math (see Section A and Finding #1)
5. ☑ I independently verified the VRAM budget math (see above)
6. ☑ Every finding has exact line numbers from ARCHITECTURE_V10.md
7. ☑ I checked for cascading effects between fixes (FIX-11→FIX-22 cascade identified)
8. ☑ I flagged UNVERIFIED API signatures: `download_enabled` (EasyOcrOptions), `awq_marlin` (vLLM latest tag)

---

## FINAL VERDICT

### **APPROVED WITH CONDITIONS**

The engineer applied 22 of 25 fixes correctly. Three fixes have issues:

- **FIX-11:** Applied at primary locations but created three cascading contradictions due to missed secondary locations (code comment, multiplier, tribal knowledge table). This is a textbook "Cascading Neglect" anti-pattern.
- **FIX-22:** Declared as "handled by FIX-11" but FIX-11's comment update was never applied, so FIX-22's purpose was never achieved.
- **FIX-08:** Applied correctly in code but the changelog was not updated to reflect the threshold change.

**Required patches before approval:**
1. Fix `build_context()` comment at L800–802 (Finding #1)
2. Fix budget multiplier at L854 (Finding #2)
3. Fix Tribal Knowledge table RAG budget at L1048 (Finding #3)

**Recommended patches (non-blocking):**
4. Update changelog threshold at L40 (Finding #4)
5. Retain legacy regex in security section (Finding #5)
6. Clarify CAUTION box re: non-localhost published ports (Finding #6)
7. Verify `download_enabled` parameter against Docling source (Finding #7)

---

**END OF AUDIT REPORT**
