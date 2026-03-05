# V10 Phase 10 — Fix List

**Source:** Phase 10 Hostile Audit (Opus)
**Total Valid Findings:** 17 (3 withdrawn by auditor)
**Subtractive:** 0

---

## CRITICAL (3) — Apply one at a time

| ID | Type | Summary | Verified |
|:---|:-----|:--------|:---------|
| P10-09 | `[ADDITIVE]` | Missing `import asyncio` in `ingest.py` — `/api/cleanup` DOA | ✅ Line 1069 |
| P10-02 | `[ADDITIVE]` | Lock-protect `_get_client()` — client use-after-close | ✅ Line 806 |
| P10-03 | `[ADDITIVE]` | Lock-protect `_get_llm_client()` — same pattern | ✅ Line 1871 |

## SIGNIFICANT (10) — Apply 3 at a time

| ID | Type | Summary | Verified |
|:---|:-----|:--------|:---------|
| P10-14 | `[CORRECTIVE]` | Wire `_RESPONSE_BUDGET_TOKENS` to `generate_response(max_tokens=)` | ✅ Line 1441 |
| P10-17 | `[CORRECTIVE]` | `TEI_BASE_URL` — read from env var | ✅ Line 778 |
| P10-18 | `[CORRECTIVE]` | `VLLM_BASE_URL` — read from env var | ✅ Line 1840 |
| P10-05 | `[CORRECTIVE]` | Snapshot restore path: `/qdrant/storage/snapshots/` → `/qdrant/snapshots/` | ✅ Line 2303 |
| P10-07 | `[CORRECTIVE]` | `LockedTokenizer.__getattr__` must acquire lock | ✅ Line 497 |
| P10-16 | `[ADDITIVE]` | Separate `QdrantClient` instances for search vs ingest | ✅ Line 658 |
| P10-21 | `[CORRECTIVE]` | Relax `\n\n\n` stop sequence to `\n\n\n\n\n` | ✅ Line 1933 |
| P10-01 | `[CORRECTIVE]` | Budget diagram missing INJECTION_OVERHEAD line item | ✅ Line 1802 |
| P10-11 | `[CORRECTIVE]` | Validator missing `INJECTION_OVERHEAD=15` | ✅ Line 2219 |
| P10-04 | `[CORRECTIVE]` | Thread-safe lazy lock init via `threading.Lock` | ✅ Lines 789,1856 |
| P10-06 | `[CORRECTIVE]` | Add Nginx HTTP→HTTPS redirect (option C) | ✅ Line 319 |
| P10-20 | `[ADDITIVE]` | Thread-safe failure manifest writes | ✅ Line 1040 |

## MINOR (4)

| ID | Type | Summary | Verified |
|:---|:-----|:--------|:---------|
| P10-12 | `[CORRECTIVE]` | Tribal knowledge table: `26,318` → `26,203` | ✅ Line 2168 |
| P10-15 | `[CORRECTIVE]` | `hybrid_search` default `top_k=20` → `60` | ✅ Line 1534 |
| P10-19 | `[CORRECTIVE]` | Remove deprecated `version: "3.8"` | ✅ Line 143 |
| P10-10 | `[ADDITIVE]` | Consolidate `models` import in ingest.py | ✅ |

## REJECTED / DEFERRED (3)

| ID | Reason |
|:---|:-------|
| P10-08 | Code clarity only — `index_chunk()` already handles empty sparse. Not a bug. |
| P10-13 | `load_ledger()` disk I/O acceptable for single-user prototype. Defer. |
| P10-22 | `ensure_qdrant_collection()` race impossible with single Uvicorn worker. Defer. |

## DEEP THINK AUDITOR (6 → 5 new)

| ID | Severity | Type | Summary | Status |
|:---|:---------|:-----|:--------|:-------|
| DT-P10-01 | CRITICAL | `[CORRECTIVE]` | `asyncio.Semaphore` module-level crash (same as DT-P9-01 for locks) | ✅ Applied |
| DT-P10-02 | CRITICAL | `[CORRECTIVE]` | Response budget desync → DUPLICATE of P10-14 | ⏭️ Skipped |
| DT-P10-03 | CRITICAL | `[CORRECTIVE]` | Cleanup protocol: BEFORE re-ingestion, not after (UUID5 deletes new chunks) | ✅ Applied |
| DT-P10-04 | SIGNIFICANT | `[CORRECTIVE]` | ChatML orphan strip bypassed when token budget under 8000 | ✅ Applied |
| DT-P10-05 | SIGNIFICANT | `[CORRECTIVE]` | Explicit `tokenize()`/`__call__()` wrappers (strengthens P10-07) | ✅ Applied |
| DT-P10-06 | SIGNIFICANT | `[CORRECTIVE]` | Lazy generator iteration escapes `try/except` quarantine | ✅ Applied |
