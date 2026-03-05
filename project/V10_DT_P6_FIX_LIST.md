# V10 Deep Think Phase 6 — Fix List

**Baseline Frozen:** `ARCHITECTURE_V10_PRE_DTP6_FROZEN.md`
**Cumulative Fix Count Before:** 92

---

## SIGNIFICANT (2 fixes)

### DT-P6-02 — TEI Token Limit Ordering: Embed Before Validation `[CORRECTIVE]`
- **Source:** Deep Think P6 Dim 4
- **What:** Step 3 embeds the user query via TEI (8192-token hardware limit) BEFORE Step 5's `MAX_USER_QUERY_TOKENS = 10000` cap fires. A 9500-token query crashes TEI before the length check. The mechanic gets a generic "search system unavailable" error instead of "query too long."
- **Fix:** (1) Move the `user_query_tokens` calculation and `MAX_USER_QUERY_TOKENS` guard ABOVE Step 3's embed call. (2) Reduce `MAX_USER_QUERY_TOKENS` from 10000 to 8000 to align with TEI's hardware limit.

### DT-P6-05 — Dense-Only Dynamic Ratio Over-Filters Relevant Chunks `[CORRECTIVE]`
- **Source:** Deep Think P6 Dim 3
- **What:** The dynamic ratio threshold `top_score * 0.70` was calibrated for RRF's tight [0.012, 0.016] range. In cosine space (0.3-1.0), a top score of 0.90 sets threshold at 0.63, discarding chunks scoring 0.60 which are still highly relevant.
- **Fix:** Disable ratio threshold in dense-only mode: `effective_ratio = min_score_ratio if len(prefetch_list) >= 2 else 0.0`

---

## CRITICAL (1 fix)

### DT-P6-03 — validate_ledger.py Exception Handler Doesn't Catch RuntimeError `[CORRECTIVE]`
- **Source:** Deep Think P6 Dim 4
- **What:** DT-P5-06 changed the tokenizer init from `SystemExit` to `RuntimeError`. But `validate_ledger.py` (line 1798) catches only `ImportError`. RuntimeError does NOT inherit from ImportError — the host-side validator crashes instantly, breaking the tribal knowledge pipeline.
- **Fix:** Change `except ImportError:` to `except (ImportError, RuntimeError):` at line 1798.

---

## ALREADY COVERED (3 findings)

### DT-P6-01 → Covered by Opus P6-01 (budget desync PHASE_ERROR guard)
### DT-P6-06 → Covered by Opus P6-02 (if→while orphan strip)
### DT-P6-07 → Covered by Opus P6-03 (double-write manifest guard)

---

## DEFERRED (1 finding)

### DT-P6-04 — Sequential Await Bottleneck in Ingestion → `DEFERRED — concurrency redesign, not audit fix scope`
