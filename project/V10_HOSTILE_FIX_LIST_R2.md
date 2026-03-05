# V10 Hostile Audit Fix List — Phase 2 (Opus)

**Source:** `V10_HOSTILE_AUDIT_R2_OPUS.md`
**Baseline Frozen:** `ARCHITECTURE_V10_PRE_PHASE2_FROZEN.md`
**Date:** 2026-02-24

---

## Classification Summary

| Type | Count | Notes |
|:-----|:-----:|:------|
| `[ADDITIVE]` | 6 | New imports, new parameters, new code blocks |
| `[CORRECTIVE]` | 8 | Fix values, logic, wording |
| `[SUBTRACTIVE]` | 0 | None |

✅ All 14 pass the pre-application checklist. No deletions.

---

## MINOR Fixes (4)

### P2-11 `[ADDITIVE]` — Path traversal validation in `/api/ingest`
Add `os.path.realpath()` validation and `.pdf` extension check to ingest route.

### P2-12 `[ADDITIVE]` — System prompt file error handling
Replace bare `open()` at module import with existence check + explicit `SystemExit`.

### P2-13 `[CORRECTIVE]` — GPU util table stale value
Update vLLM config table: `0.85` → `0.75` to match Docker Compose.

### P2-14 `[CORRECTIVE]` — Raise `min_absolute_score` from dead `0.005` to `0.013`
Current value can never trigger (RRF minimum is 0.0125). Raise to 0.013.

---

## SIGNIFICANT Fixes (6)

### P2-05 `[CORRECTIVE]` — Always include RETRIEVED DOCUMENTS header
In `generate_response()`, add `else` branch with `[No documents retrieved]` placeholder so RETRIEVAL_FAILURE triggers.

### P2-06 `[ADDITIVE]` — Background ingestion error wrapper
Add `ingest_pdf_background()` wrapper with try/except that logs failures and writes to a failure manifest.

### P2-07 `[ADDITIVE]` — Add `logger` to `search.py`
Add `import logging` + `logger = logging.getLogger(__name__)` to search module.

### P2-08 `[CORRECTIVE]` — UUID `.hex` → `str()` format + type annotation fix
Change `uuid5(...).hex` to `str(uuid5(...))` for proper hyphenated UUID. Fix `index_chunk` type hint `int` → `str`.

### P2-09 `[ADDITIVE]` — Complete `renderGusResponse()` with PHASE_D, RETRIEVAL_FAILURE, text input toggle
Add missing state handling branches and textInputEl toggle logic.

### P2-10 `[CORRECTIVE]` — Add missing fields to PHASE_ERROR JSON responses
Add `requires_input`, `answer_path_prompts`, `source_citations`, `intersecting_subsystems` to all 3 error handlers.

---

## CRITICAL Fixes (4)

### P2-01 `[CORRECTIVE]` — Add `user_query_tokens` to budget math
Add new parameter to `build_context()` and deduct from available tokens.

### P2-02 `[CORRECTIVE]` — Physically truncate chat_history array (oldest-first eviction)
Add eviction loop in `chat()` handler before passing history to `generate_response()`.

### P2-03 `[ADDITIVE]` — Import/share TOKENIZER in chat.py
Add `from backend.inference.context import TOKENIZER` (or create shared module).

### P2-04 `[ADDITIVE]` — Define and share `qdrant_client` instance
Add shared client instantiation and import in both chat.py and ingest.py.
