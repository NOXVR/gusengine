# V10 Phase 7 Audit — Fix List & Verdict

**Report:** V10 HOSTILE ARCHITECTURE AUDIT — PHASE 7 (SYSTEMIC DESIGN ANALYSIS)
**Findings:** 8 total
**Prior cumulative fix count:** 95

---

## Finding-by-Finding Analysis

### P7-01: Thread-Safety Lock is Bypassed (Dead Code) ✅ CONFIRMED — CORRECTIVE

**Severity:** CRITICAL
**Verdict: HAS MERIT — apply fix**

**Evidence:** `count_tokens()` is defined at line 644 of `ARCHITECTURE_V10.md` with `_TOKENIZER_LOCK` at line 642. However, ALL call sites bypass it:
- Line 1077: `len(TOKENIZER.encode(user_query))` — chat handler
- Line 1433: `len(TOKENIZER.encode(SEPARATOR))` — context builder
- Line 1451: `len(TOKENIZER.encode(header + "\n\n"))` — context builder

The P6-06 fix added the wrapper but never migrated the call sites. The lock provides zero protection.

**Fix:** Replace all `len(TOKENIZER.encode(...))` with `count_tokens(...)` and import from shared module.

---

### P7-02: Unbudgeted ChatML Framing Tokens Overflow ✅ CONFIRMED — CORRECTIVE

**Severity:** CRITICAL
**Verdict: HAS MERIT — apply fix**

**Evidence:** The budget math at lines 1405-1410 sums raw string token counts:
```
available = max_context_tokens - system_prompt_tokens - ledger_tokens
            - response_budget - chat_history_tokens - user_query_tokens
```

But `generate_response()` (lines 1549-1557) assembles messages into a ChatML-formatted prompt where vLLM injects `<|im_start|>role\n...<|im_end|>\n` framing per message (~4-5 tokens each). With ~12 messages, that's ~60-75 unbudgeted tokens. When the budget is exactly saturated (worst case), the final prompt exceeds `--max-model-len 32768`.

**Fix:** Add `FRAMEWORK_OVERHEAD = 100` deduction in `build_context()`. This is a safe, conservative buffer for ChatML framing + header glue.

---

### P7-03: MIN_RAG_FLOOR Override Fabricates Tokens ✅ CONFIRMED — CORRECTIVE

**Severity:** CRITICAL
**Verdict: HAS MERIT — apply fix (modified)**

**Evidence:** Lines 1414-1419:
```python
if available < MIN_RAG_FLOOR:
    ...
    available = MIN_RAG_FLOOR
```

This overrides a negative or insufficient budget to 5000, authorizing context extraction that physically exceeds the context window. While the default `max_context_tokens=32768` with all guards active prevents `available` from going negative, the architecture provides no protection if `max_context_tokens` is ever reduced (e.g., for a smaller model or hardware profile).

**Fix:** Change from silent override to rejection — raise an error that chat.py catches as PHASE_ERROR. This is safer than silently inflating the budget.

**Note on the auditor's proof:** The auditor's scenario uses `MAX_CONTEXT_TOKENS = 16384` which is NOT the current deployment configuration. Under the ACTUAL config (32768), the guards prevent `available` from going negative. However, the fix is still warranted as defensive programming — the current behavior is a latent bomb.

---

### P7-04: Missing Circuit Breaker in Ingestion Loop ✅ CONFIRMED — ADDITIVE

**Severity:** CRITICAL
**Verdict: HAS MERIT — apply fix**

**Evidence:** Lines 871-874:
```python
except Exception as e:
    failed_count += 1
    logger.warning(f"Chunk {i}/{len(chunks)} failed for {pdf_path}: {e} — skipping")
    continue
```

When TEI or Qdrant dies, `ConnectError` returns instantly (~1ms). The loop burns through all remaining chunks at CPU speed, discarding hours of OCR work. A 200-chunk PDF is fully skipped in ~200ms.

**Fix:** Add consecutive failure counter with threshold of 5. After 5 consecutive failures, raise `IngestionError` to abort and write to manifest. This preserves the per-chunk error tolerance while preventing cascade burn-through.

---

### P7-05: Chat Embedding Starvation via Unbounded Semaphore ✅ CONFIRMED — CORRECTIVE

**Severity:** SIGNIFICANT
**Verdict: HAS MERIT — apply fix**

**Evidence:** Line 1100:
```python
async with EMBED_SEMAPHORE:
    query_dense, query_sparse = await embed_text(user_query)
```

`async with EMBED_SEMAPHORE` blocks indefinitely. During bulk ingestion with TEI degradation, the 8 semaphore permits can be held for 10s each (P6-08 timeout). Chat requests queue behind ingestion for up to 250s, exceeding Nginx's 60s proxy timeout.

**Fix:** Use `asyncio.wait_for(EMBED_SEMAPHORE.acquire(), timeout=5.0)` with explicit release in a finally block. Timeout produces a PHASE_ERROR.

---

### P7-06: Volatile BackgroundTasks Erase Ingestion Queue ⚠️ CONDITIONAL MERIT — DEFERRED

**Severity:** SIGNIFICANT
**Verdict: DEFERRED — valid concern, but implementation scope exceeds corrective fix**

**Rationale:** This finding is architecturally valid — FastAPI's BackgroundTasks are volatile RAM structures. A container restart during a 20-60 hour ingestion window would lose the queue. However:

1. The V9 daemon is the source of truth for which PDFs need ingestion — it can re-trigger.
2. Implementing a durable queue (file-backed persistence + startup re-queue) is a significant feature addition, not a bug fix.
3. The `INGEST_SEMAPHORE(2)` already limits in-flight work to 2 PDFs at a time — the actual data at risk is 2 PDFs, not 500.
4. The failure manifest already records partial/failed ingestions for operator review.

**Recommendation:** Track as a V10.1 enhancement, not a Phase 7 fix.

---

### P7-07: Idempotent Upsert Orphans Stale Chunks ✅ CONFIRMED — ADDITIVE

**Severity:** SIGNIFICANT
**Verdict: HAS MERIT — apply fix**

**Evidence:** The ingestion loop at lines 838-870 upserts chunks with deterministic UUID5 IDs. If a PDF shrinks on re-ingestion (brakes_v1.pdf: 100 chunks → brakes_v2.pdf: 60 chunks), chunks 60-99 from the old version persist in Qdrant and pollute search results with obsolete diagnostic data.

**Fix:** Before the ingestion loop, delete all existing points for the same source PDF using Qdrant's filter-based deletion. The auditor's proposed fix using `FieldCondition(key="payload.source", ...)` is correct in principle but should use the metadata key from the actual architecture (likely `source` in the indexed payload).

---

### P7-08: Hardcoded Model Contract Violation ✅ CONFIRMED — CORRECTIVE

**Severity:** MINOR
**Verdict: HAS MERIT — apply fix**

**Evidence:** Line 1563:
```python
"model": "Qwen2.5-32B-Instruct-AWQ",
```

This string is hardcoded in `generate_response()`. The Docker compose environment variable `VLLM_MODEL` can define the model name, but the backend ignores it.

**Fix:** Read from environment variable with fallback to current value:
```python
VLLM_MODEL = os.environ.get("VLLM_MODEL", "Qwen2.5-32B-Instruct-AWQ")
```

---

## Summary

| Finding | Severity | Verdict | Classification |
|:--------|:---------|:--------|:---------------|
| P7-01 | CRITICAL | **APPLY** | [CORRECTIVE] |
| P7-02 | CRITICAL | **APPLY** | [CORRECTIVE] |
| P7-03 | CRITICAL | **APPLY** | [CORRECTIVE] |
| P7-04 | CRITICAL | **APPLY** | [ADDITIVE] |
| P7-05 | SIGNIFICANT | **APPLY** | [CORRECTIVE] |
| P7-06 | SIGNIFICANT | **DEFERRED** | [ADDITIVE] |
| P7-07 | SIGNIFICANT | **APPLY** | [ADDITIVE] |
| P7-08 | MINOR | **APPLY** | [CORRECTIVE] |

**Actionable fixes: 7** (P7-01 through P7-05, P7-07, P7-08)
**Deferred: 1** (P7-06 — volatile queue, scope too large for corrective fix)
**New cumulative fix count after application: 102**
