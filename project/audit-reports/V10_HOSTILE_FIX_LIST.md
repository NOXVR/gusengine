# V10 Hostile Audit Fix List — Opus Round 1

**Source:** `V10_HOSTILE_AUDIT_R1_OPUS.md`
**Baseline Frozen:** `ARCHITECTURE_V10_PRE_HOSTILE_AUDIT_FROZEN.md`
**Date:** 2026-02-24

---

## Classification Summary

| Type | Count | Notes |
|:-----|:------|:------|
| `[ADDITIVE]` | 10 | Add missing error handling, guardrails, healthchecks |
| `[CORRECTIVE]` | 3 | Fix existing values/comments |
| `[SUBTRACTIVE]` | **0** | ✅ No deletions required |

---

## MINOR (1 fix) — Apply first

### FIX-H01 `[CORRECTIVE]`
**Source:** Finding #10 | **Severity:** MINOR
**Summary:** `build_context()` comment says "Default" but uses `ledger_tokens=2550`, which isn't the function's default (default is 0).
**Fix:** Change "Default" to "Typical (with ledger)" in comment at L807.

---

## SIGNIFICANT (5 fixes) — Apply in batches of 3

### FIX-H02 `[CORRECTIVE]`
**Source:** Finding #1 | **Severity:** SIGNIFICANT
**Summary:** `--gpu-memory-utilization 0.85` leaves only 1.1 GB on GPU 0 after TEI. Tight.
**Fix:** Reduce to `0.80` for safer headroom.

### FIX-H03 `[ADDITIVE]`
**Source:** Finding #2 | **Severity:** SIGNIFICANT
**Summary:** No Docker healthchecks. `depends_on` without `condition: service_healthy` means gusengine starts before dependencies are ready.
**Fix:** Add `healthcheck` blocks to vLLM, TEI, Qdrant. Add `condition: service_healthy` to gusengine's depends_on.

### FIX-H04 `[ADDITIVE]`
**Source:** Finding #7 | **Severity:** SIGNIFICANT
**Summary:** Ledger injection into prompt is undefined — `load_ledger()` exists but where it enters message assembly is unspecified.
**Fix:** Show complete chat handler assembly showing where ledger content goes.

### FIX-H05 `[ADDITIVE]`
**Source:** Finding #8 | **Severity:** SIGNIFICANT
**Summary:** No absolute relevance threshold — `min_score_ratio=0.70` is relative only. Off-topic queries always return irrelevant chunks.
**Fix:** Add `min_absolute_score` parameter to `hybrid_search()`.

### FIX-H06 `[CORRECTIVE]`
**Source:** Finding #9 | **Severity:** SIGNIFICANT
**Summary:** `index_chunk()` uses synchronous `client.upsert()` inside async `ingest_pdf()` — blocks event loop during bulk ingestion.
**Fix:** Wrap `index_chunk()` call in `asyncio.to_thread()`.

### FIX-H07 `[CORRECTIVE]`
**Source:** Finding #11 | **Severity:** SIGNIFICANT
**Summary:** Context header token overhead hardcoded at 20 but actual headers vary. Budget can overshoot.
**Fix:** Compute actual header token count with TOKENIZER instead of hardcoding.

### FIX-H08 `[ADDITIVE]`
**Source:** Finding #13 | **Severity:** SIGNIFICANT
**Summary:** DOMPurify integration mandated but implementation code not shown.
**Fix:** Include actual DOMPurify calls in `renderGusResponse()` code.

---

## CRITICAL (5 fixes) — Apply one at a time

### FIX-H09 `[ADDITIVE]`
**Source:** Finding #3 | **Severity:** CRITICAL
**Summary:** No `try/except` around `embed_text()` in chat path — TEI crash returns raw 500.
**Fix:** Wrap chat handler's embed call in error handling that returns structured JSON error.

### FIX-H10 `[ADDITIVE]`
**Source:** Finding #4 | **Severity:** CRITICAL
**Summary:** No `try/except` around `hybrid_search()` — Qdrant 404 on missing collection returns raw 500.
**Fix:** Add error handling; return `RETRIEVAL_FAILURE` JSON to frontend.

### FIX-H11 `[ADDITIVE]`
**Source:** Finding #5 | **Severity:** CRITICAL
**Summary:** No runtime RAG budget floor in `build_context()` — minimum exists only in ledger validator.
**Fix:** Add runtime floor check and warning log when budget is below minimum.

### FIX-H12 `[ADDITIVE]`
**Source:** Finding #6 | **Severity:** CRITICAL
**Summary:** No chat history truncation — unbounded growth → budget exhaustion → false RETRIEVAL_FAILURE.
**Fix:** Add max chat history cap with oldest-turn eviction.

### FIX-H13 `[ADDITIVE]`
**Source:** Finding #12 | **Severity:** CRITICAL
**Summary:** `generate_response()` has no `try/except` — vLLM OOM/timeout returns raw 500.
**Fix:** Catch timeout and HTTP errors, return PHASE_ERROR JSON.

---

## Pre-Application Checklist Results

All 13 fixes checked:
- [x] No fix deletes any function or method
- [x] No fix deletes any class or module
- [x] No fix deletes any Docker service, volume, or network
- [x] No fix deletes any security control
- [x] No fix reduces capability of an existing system
- [x] No fix replaces a working component with nothing
- [x] No fix contradicts a V9 heritage component

✅ **All 13 fixes pass the pre-application checklist. Safe to apply.**
