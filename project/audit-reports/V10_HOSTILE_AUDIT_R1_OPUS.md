# HOSTILE ARCHITECTURE AUDIT REPORT: V10

**AUDITOR:** Claude Opus 4.6 (Hostile Configuration)
**DATE:** 2026-02-24
**DOCUMENT UNDER AUDIT:** `ARCHITECTURE_V10.md` (1,315 lines)
**VERDICT:** ⛔ BLOCKED — 5 Critical Findings

---

## AUDITOR INTEGRITY CHECKLIST

1. ☑ I did NOT recommend removing any pre-existing code or infrastructure
2. ☑ Every finding is tagged `[ADDITIVE]`, `[CORRECTIVE]`, or `[SUBTRACTIVE]` with justification
3. ☑ I traced ALL 5 scenarios through the FULL pipeline
4. ☑ I checked ALL 8 failure modes
5. ☑ I independently computed the token budget math (shown below)
6. ☑ I independently computed the VRAM budget math (shown below)
7. ☑ Every finding has exact line numbers
8. ☑ I did NOT hallucinate API signatures — uncertainties marked UNVERIFIED
9. ☑ I checked the data format at EVERY pipeline boundary (→)
10. ☑ My findings are PROBLEMS, not suggestions for improvement

---

## INDEPENDENT MATH VERIFICATION

### VRAM Budget (Show Work)

**Qwen2.5-32B-AWQ weights:**
32B params × 4 bits / 8 bits-per-byte = 16 GB raw. With AWQ overhead and activation storage, ~18 GB. Architecture says ~18 GB (L104). ✅ CONFIRMED.

**KV Cache @ 32K context (per-token):**
64 layers × 8 KV heads (GQA) × 128 dim × 2 (K+V) × 2 bytes (FP16)
= 64 × 8 × 128 × 4 = 262,144 bytes = 0.25 MB/token
At 32,768 tokens: 0.25 MB × 32,768 = 8,192 MB = **8 GB**
Architecture says ~8 GB (L105, L118). ✅ CONFIRMED.

**BGE-M3:** 568M params × 2 bytes (FP16) ≈ 1.1 GB weights + runtime ≈ **~2 GB**. Architecture says ~2 GB (L108). ✅ CONFIRMED.

**Total:** 18 + 8 + 2 + 2.5 = **30.5 GB / 48 GB = 64%**. Architecture says 30.5 GB, 64% (L111). ✅ CONFIRMED.

**But:** vLLM `--gpu-memory-utilization 0.85` (L171) preallocates 0.85 × 24 GB = **20.4 GB per GPU**. On GPU 0, TEI needs ~2.5 GB. Remaining after both: 24 - 20.4 - 2.5 = **1.1 GB** for CUDA contexts and OS. This is feasible (~500 MB CUDA context typical) but dangerously tight. See Finding #1.

### Token Budget (Show Work)

**Default parameters (L786-791):**

| Component | Tokens | Source |
|:----------|-------:|:-------|
| `max_context_tokens` | 32,768 | L787 default |
| `system_prompt_tokens` | 900 | L788 default |
| `ledger_tokens` | **0** | **L789 default** |
| `response_budget` | 2,000 | L790 default |
| `chat_history_tokens` | 0 | L791 default |
| **Available for RAG** | **29,868** | 32768 - 900 - 0 - 2000 - 0 |

**Comment at L807 claims:** "Default (chat_history_tokens=0): 32768 - 900 - **2550** - 2000 = **27,318**"

⚠️ **DISCREPANCY:** The comment uses `ledger_tokens=2550`, but the function signature default is `ledger_tokens=0`. The 27,318 figure is only correct when the caller explicitly passes `ledger_tokens=2550`. With actual defaults, the RAG budget is 29,868. See Finding #10.

**With typical values (caller passes correct args):**
32,768 - 900 - 2,550 - 2,000 - 1,000 (chat history) = **26,318**. Architecture says ~26,318 (L808, L856). ✅ CONFIRMED — but ONLY when caller passes correct arguments.

**Minimum RAG floor:** Architecture specifies 20,000 (L1057, L1082). This is checked ONLY in `validate_ledger.py` (L1098), NOT in `build_context()`. See Finding #5.

---

## PER-DIMENSION SUMMARY

| Dimension | Status | Critical | Significant | Minor | Notes |
|:----------|:-------|:--------:|:-----------:|:-----:|:------|
| 1. Structural Integrity | **WARN** | 0 | 2 | 1 | GPU contention tight; depends_on inadequate; comment discrepancy |
| 2. Functional Flow | **FAIL** | 2 | 2 | 0 | Chat handler missing error handling; ledger injection undefined; no chat cap |
| 3. Outcome Simulation | **WARN** | 1 | 1 | 0 | Scenario D (no-match) has no absolute threshold; Scenario C unbounded chat |
| 4. Failure Modes | **FAIL** | 2 | 1 | 0 | 3 of 8 failure modes produce raw 500s; no graceful degradation |

---

## FINDINGS TABLE

| # | Dim | Severity | Type | Summary | Evidence | Fix |
|:--|:----|:---------|:-----|:--------|:---------|:----|
| 1 | 1 | SIGNIFICANT | [CORRECTIVE] | vLLM `gpu-memory-utilization=0.85` leaves only 1.1 GB on GPU 0 after TEI | L171, L108-109 | Reduce to `0.80` or `0.75` to guarantee headroom |
| 2 | 1 | SIGNIFICANT | [ADDITIVE] | No Docker healthchecks — `depends_on` without `condition: service_healthy` means gusengine starts before vLLM/TEI/Qdrant are ready | L256-259 | Add `healthcheck` blocks and `depends_on: condition: service_healthy` |
| 3 | 2,4 | **CRITICAL** | [ADDITIVE] | No `try/except` around `embed_text()` in chat path — TEI crash (ConnectionRefused) propagates as raw 500 | L677-678 | Wrap chat handler's embed+search+generate calls in error handling that returns structured JSON error |
| 4 | 2,4 | **CRITICAL** | [ADDITIVE] | No `try/except` around `hybrid_search()` — Qdrant 404 on missing collection (Failure Mode 3) returns raw 500 | L678, L720 | Add error handling; return `RETRIEVAL_FAILURE` JSON to frontend |
| 5 | 2,3 | **CRITICAL** | [ADDITIVE] | No runtime RAG budget floor in `build_context()` — `MIN_RAG_BUDGET=20000` exists only in ledger validator, not at query time | L801-805 vs L1082-1098 | Add `available = max(available, MIN_RAG_FLOOR)` or cap `chat_history_tokens` |
| 6 | 2,3 | **CRITICAL** | [ADDITIVE] | No chat history truncation mechanism — unbounded `chat_history_tokens` can push RAG budget to zero or negative | L791, L805, L910-911 | Add max chat history cap (e.g. 5000 tokens) with oldest-turn eviction |
| 7 | 2 | SIGNIFICANT | [ADDITIVE] | Ledger injection into prompt is undefined — `load_ledger()` exists but WHERE it enters the message assembly is unspecified | L1107-1123 vs L900-914 | Show complete chat handler assembly: where ledger goes relative to system prompt, context, history |
| 8 | 3 | SIGNIFICANT | [ADDITIVE] | No absolute relevance score threshold — `min_score_ratio=0.70` is relative to top score; off-topic queries always return irrelevant chunks | L714, L746-753 | Add absolute minimum RRF score cutoff (e.g. `min_absolute_score=0.005`) below which all results are discarded |
| 9 | 2 | SIGNIFICANT | [CORRECTIVE] | `index_chunk()` uses synchronous `client.upsert()` inside async `ingest_pdf()` — blocks event loop during bulk ingestion | L549, L662 | Use `AsyncQdrantClient` or wrap in `asyncio.to_thread()` |
| 10 | 1 | MINOR | [CORRECTIVE] | `build_context()` comment at L807 claims default RAG budget is 27,318 but function default for `ledger_tokens` is 0, giving 29,868 | L789, L807 | Fix comment to say "Typical (with ledger)" not "Default" |
| 11 | 2 | SIGNIFICANT | [CORRECTIVE] | Context header token overhead hardcoded at 20 (L819) but actual headers vary 10-50+ tokens depending on filename/headings length — budget can overshoot | L819, L826-832 | Compute actual header token count with TOKENIZER instead of hardcoding |
| 12 | 2,4 | **CRITICAL** | [ADDITIVE] | `generate_response()` has no `try/except` — vLLM OOM/timeout (Failure Mode 2) returns raw 500 to user | L916-928 | Catch `httpx.TimeoutException` and `httpx.HTTPStatusError`, return PHASE_ERROR JSON |
| 13 | 4 | SIGNIFICANT | [ADDITIVE] | DOMPurify integration is mandated (L1006) but implementation code not shown — sanitization gap between mandate and proof | L1004-1006, L1014 | Include actual `renderGusResponse()` code showing DOMPurify calls on all LLM-controlled strings |

---

## SCENARIO TRACE RESULTS

### Scenario A: Happy Path (1968 Ford Mustang, 289 V8 torque spec)

**Predicted Outcome:** Correct answer — "65-70 ft-lbs" with citation to source document, page 47.
**Confidence:** HIGH

**Full Trace:**

1. **PDF → Docling (L411-479):** Clean 300-page scan. `create_converter()` with `do_ocr=True`, `TableFormerMode.ACCURATE`. Page 47 contains a table row "Cylinder Head Bolts — 65-70 ft-lbs". Docling's table extractor detects the table structure. `HybridChunker(max_tokens=512)` keeps the table within a single chunk (typical table row + headers < 512 tokens). Chunk metadata: `page_numbers: [47]`, headings from section hierarchy.

2. **Chunk → TEI embed (L586-631):** `embed_text(chunk_text)` calls `/embed` → 1024-dim dense vector encoding "cylinder head bolts 65-70 ft-lbs" semantics. `/embed_sparse` → sparse vector with high weights on "cylinder", "head", "bolts", "torque", "ft-lbs". Both returned successfully.

3. **TEI → Qdrant (L546-568):** `index_chunk()` stores dense + sparse vectors with payload containing text, source filename, `page_numbers: [47]`, headings, token_count.

4. **User query → embed (L677):** "What is the torque specification for the cylinder head bolts on a 289 V8?" → Dense vector strongly aligned with the indexed chunk. Sparse vector hits "torque", "cylinder", "head", "bolts".

5. **hybrid_search (L701-767):** Dense prefetch returns the page 47 chunk in top-5. Sparse prefetch also returns it. RRF fusion ranks it very high (appears in both signals). Dynamic threshold (0.70 × top score) keeps it and nearby chunks.

6. **build_context (L785-839):** Chunk fits within 26,318-token RAG budget. Header formatted as `[Source 1: mustang_shop_manual.pdf | Pages 47 | Engine Specifications > Torque Values]`. Included in context string.

7. **generate_response (L887-928):** System prompt (Gus DAG) + RETRIEVED DOCUMENTS containing the chunk + user message sent to Qwen2.5. Temperature 0.1. Model extracts "65-70 ft-lbs" and formats JSON with `source_citations: [{source: "mustang_shop_manual.pdf", page: 47, context: "Engine Specifications > Torque Values"}]`.

8. **Frontend (L1012-1034):** `parseGusResponse()` extracts JSON. `renderGusResponse()` displays instructions. `renderCitation()` creates clickable bubble "mustang_shop_manual.pdf p.47". Click → PDF.js opens to page 47.

**Failure Points:** None identified for this scenario.

---

### Scenario B: Degraded Scan (1962 Chevy, water-damaged firing order)

**Predicted Outcome:** UNCERTAIN — Depends on EasyOCR quality on specific damage. Most likely: partial OCR success with possible digit garbling.
**Confidence:** MEDIUM

**Full Trace:**

1. **PDF → Docling + EasyOCR (L390-397):** `do_ocr=True`, `EasyOcrOptions(lang=["en"], use_gpu=False)`. The water-damaged page goes through EasyOCR. Firing order "1-8-4-3-6-5-7-2" is a sequence of single digits separated by hyphens.

   **EasyOCR failure modes on degraded text:**
   - Digit confusion: "1" ↔ "l" ↔ "I", "8" ↔ "B", "5" ↔ "S", "3" ↔ "B", "6" ↔ "G", "7" ↔ "Z"
   - Coffee stain occlusion: digits may be missed entirely
   - Likely OCR output for water-damaged text: something like `"l-B-4-3-G-5-7-Z"` or `"1-8-4-3-6-S-7-2"` (partial corruption)

2. **Chunk quality:** If the page heading "FIRING ORDER" survives OCR (headings tend to be larger/bolder, more OCR-resistant), the chunk text contains the keyword "firing order" plus garbled digits. If the heading is also degraded, the chunk is largely gibberish.

3. **Embedding (L586-631):** If "firing order" heading survived OCR, the dense embedding captures the semantic concept. The sparse vector contains "firing" and "order" tokens. The garbled digits are noise but don't kill the semantic signal.

4. **Retrieval:** Query "What's the firing order for the 283?" → Dense match on "firing order" concept + sparse match on keywords → chunk retrieved IF heading survived OCR. RRF score will be lower than a clean scan but likely above the 0.70 relative threshold.

5. **LLM response:** Qwen2.5 sees the chunk with garbled digits. Two outcomes:
   - **Best case:** Model recognizes the pattern as a firing order and reports the garbled version, possibly noting uncertainty.
   - **Likely case:** Model outputs whatever digits it sees in the chunk. If OCR produced `"l-B-4-3-G-5-7-Z"`, the model may output that — **giving a WRONG answer with a citation.**

**Failure Points:**
- **Stage 1 (OCR):** EasyOCR on CPU for degraded 1962 scan is the primary risk point. No confidence scoring or quality gate on OCR output.
- **Stage 5 (LLM):** Qwen2.5 has no mechanism to detect garbled OCR — it treats chunk text as ground truth per the system prompt's "derived strictly from RETRIEVED DOCUMENTS" rule. A wrong answer with a citation is worse than no answer.

**[ADDITIVE] Gap:** No OCR confidence threshold. EasyOCR returns confidence scores per text region, but `parse_and_chunk()` (L411-479) discards them — only checks `if not text or not text.strip()` (L455). A chunk of garbled OCR text passes this check. Consider adding a minimum average OCR confidence threshold (e.g., 0.60) per chunk, below which the chunk is flagged as low-confidence in its metadata and the system prompt can warn the user.

---

### Scenario C: Multi-Step Diagnostic (1967 Pontiac GTO rough idle)

**Predicted Outcome:** PHASE_A_TRIAGE correctly initiated. Subsequent turns WILL FAIL if conversation exceeds ~30 messages due to Finding #5/#6 (no chat history cap).
**Confidence:** MEDIUM (first turn HIGH, extended conversation LOW)

**Full Trace:**

1. **First message:** "My 1967 Pontiac GTO is running rough at idle."
   - `embed_text()` on query → hybrid_search returns chunks about idle diagnostics from Pontiac FSMs
   - `build_context()` with `chat_history_tokens=0` → full RAG budget available (~26,318 tokens)
   - System prompt DAG rule: "If user provides symptom → Output current_state: PHASE_A_TRIAGE" (L960)
   - Qwen2.5 outputs JSON with `current_state: "PHASE_A_TRIAGE"`, multiple-choice options (e.g., "[A] Rough idle cold only", "[B] Rough idle hot and cold", "[C] Rough idle with stalling")
   - Frontend `renderGusResponse()` renders buttons. ✅

2. **User clicks option [B]:**
   - `buildUserMessage("[B] Rough idle hot and cold", lastResponse)` (L1013) injects `completed_state: "PHASE_A_TRIAGE"`, `required_next_state: "PHASE_B_FUNNEL"` into user message.
   - `chat_history` now contains 2 messages (~200 tokens). RAG budget: ~26,118. ✅

3. **Turns 3-10 (PHASE_B funnel):**
   - Each turn adds ~200-400 tokens to chat history.
   - After 10 turns: `chat_history_tokens ≈ 2,000`. RAG budget: ~24,318. Still fine.

4. **⛔ Turn 40+ (extended diagnostic):**
   - `chat_history_tokens ≈ 10,000+`
   - `available = 32768 - 900 - 2550 - 2000 - 10000 = 17,318` — BELOW the 20,000 MIN_RAG_BUDGET
   - **But `build_context()` does NOT enforce this floor** (Finding #5)
   - RAG context degrades silently. Model gives increasingly poor answers.
   - At 40+ messages with detailed responses: `chat_history_tokens ≈ 28,000`
   - `available = 32768 - 900 - 2550 - 2000 - 28000 = -682` — **NEGATIVE**
   - `build_context()` for loop breaks immediately (L822: `0 + total_cost > -682` is always true)
   - `context_string = ""` — ZERO RAG context
   - System prompt: "If RETRIEVED DOCUMENTS section is empty → RETRIEVAL_FAILURE" (L978)
   - User gets `RETRIEVAL_FAILURE` even though documents exist and were indexed
   - **This is a CRITICAL failure: the system silently degrades from working to broken as the conversation lengthens, with no warning or chat history eviction.**

**Failure Points:**
- **No chat history cap (Finding #6):** Unbounded accumulation.
- **No RAG floor enforcement (Finding #5):** Available budget goes negative without detection.
- **No logging of budget exhaustion:** `build_context()` doesn't log when it returns zero chunks due to budget.

---

### Scenario D: No Match (1971 Toyota Celica — no matching docs)

**Predicted Outcome:** System returns IRRELEVANT Ford/Chevy chunks. Whether user sees `RETRIEVAL_FAILURE` depends entirely on Qwen2.5's judgment — no architectural enforcement.
**Confidence:** LOW

**Full Trace:**

1. **Query → embed:** "What's the valve clearance for a 1971 Toyota Celica?" → Dense and sparse vectors for this query.

2. **hybrid_search (L701-767):** Qdrant searches `fsm_corpus` which contains only Ford and Chevy documents.
   - Dense search: Returns chunks with highest cosine similarity to the query. Even with no relevant content, SOME chunks will have nonzero similarity (e.g., a chunk mentioning "valve clearance" for a Ford engine).
   - Sparse search: "valve", "clearance" tokens match in Ford/Chevy docs. "Toyota" and "Celica" may not match anything, but the other keywords do.
   - RRF fusion: Produces ranked results with RRF scores.

3. **Dynamic threshold (L746-753):**
   `top_score = results.points[0].score` — This is the RRF score for the most relevant (but still wrong) Ford/Chevy chunk.
   `threshold = top_score * 0.70`
   All chunks within 30% of top score are included. **There is no absolute minimum.**
   With RRF k=60 and top_k=20, scores cluster in ~[0.012, 0.016]. Threshold ≈ 0.011.
   Multiple irrelevant Ford/Chevy chunks pass this threshold.

4. **build_context:** Irrelevant chunks injected into RETRIEVED DOCUMENTS section.

5. **LLM decision:** The RETRIEVED DOCUMENTS section is NOT empty — it contains Ford/Chevy valve clearance specs. The system prompt's RETRIEVAL_FAILURE guard (L978) says "If the RETRIEVED DOCUMENTS section is empty or contains NO document chunks" — but it ISN'T empty.

   Qwen2.5 must independently determine that the retrieved chunks about Ford/Chevy don't answer the Toyota question. This depends on:
   - Model intelligence: Qwen2.5-32B is capable of recognizing the mismatch.
   - System prompt: "Every hypothesis MUST be derived strictly from the RETRIEVED DOCUMENTS" (L947) — the model should notice no Toyota documents exist.
   - **Risk:** The model might answer with Ford/Chevy valve clearance specs, incorrectly attributed as Toyota specs. This would be a WRONG answer with a citation — the worst failure mode for a safety-adjacent system.

**Failure Points:**
- **No absolute relevance threshold (Finding #8):** The relative threshold ensures results are returned even when nothing is relevant.
- **LLM-dependent safety:** The architecture relies on the LLM to self-police relevance, which is not guaranteed.

---

### Scenario E: Table Extraction (Wiring diagram with wire gauges)

**Predicted Outcome:** Correct answer, assuming the table is small enough to fit in one chunk.
**Confidence:** MEDIUM-HIGH

**Full Trace:**

1. **PDF → Docling (L398-399):** `do_table_structure=True`, `TableFormerMode.ACCURATE`. Docling's TableFormer model detects the wiring table and extracts it as structured data with rows and columns.

2. **HybridChunker (L440-444):** `max_tokens=512`, `merge_peers=True`. A typical wiring diagram table with ~20 rows, 3 columns (wire color, gauge, circuit number) tokenizes to ~200-300 tokens. This fits in one chunk. ✅

   **Risk case:** A comprehensive wiring harness table with 100+ rows could exceed 512 tokens. HybridChunker would split it. The split might separate the "brake light switch" row from the column headers. Without headers, the row data is ambiguous (e.g., "Red/Green 14 72" means nothing without knowing column order).

3. **Embedding:** "brake light switch" + table context → good semantic match for query "What gauge wire goes to the brake light switch?"

4. **Retrieval:** Both dense (semantic) and sparse ("brake", "light", "switch", "gauge", "wire") signals match. High RRF score. ✅

5. **Context → LLM:** Chunk contains the table with the brake light switch row. Qwen2.5 extracts the gauge value and cites the page.

**Failure Points:**
- **Large table splitting:** If the table exceeds 512 tokens and splits, column headers may be separated from data rows. Docling's HybridChunker with `merge_peers=True` mitigates this for adjacent same-level content, but very large tables may still split. This is a known limitation, not an architecture bug.

---

## FAILURE MODE ANALYSIS

### Failure Mode 1: TEI Container Crashes

**What WILL happen (not "should"):**

1. User sends query to `/api/chat`.
2. Chat handler calls `embed_text(user_query)` (L677).
3. `embed_text()` (L605) creates `httpx.AsyncClient(timeout=30.0)`.
4. `client.post(f"{base_url}/embed", ...)` raises `httpx.ConnectError` (ConnectionRefused).
5. `dense_response.raise_for_status()` at L611 is NEVER REACHED — the connection itself failed.
6. The `try/except` at L616-629 only catches errors from the SPARSE endpoint, not the dense endpoint.
7. `httpx.ConnectError` propagates up through `embed_text()`.
8. NO try/except shown in the chat handler around the `embed_text()` call (L677).
9. FastAPI's default exception handler catches it and returns **HTTP 500 with Python traceback**.
10. Frontend receives a non-JSON 500 response. `parseGusResponse()` fails to parse it.
11. **User sees:** Either a raw error page or a broken UI state.

**Verdict: CRITICAL (Finding #3).** A single container crash cascades into a broken user experience with no graceful degradation.

### Failure Mode 2: vLLM Runs Out of VRAM

**What WILL happen:**

1. KV cache is full (many concurrent or very long requests).
2. vLLM returns HTTP 400 or 503 (depending on vLLM version and error type).
3. `response.raise_for_status()` at L927 raises `httpx.HTTPStatusError`.
4. NO try/except shown in `generate_response()` or the chat handler around it.
5. FastAPI returns **HTTP 500 with Python traceback**.

**Alternative path:** If vLLM hangs instead of returning an error, the `httpx.AsyncClient(timeout=120.0)` at L916 will raise `httpx.TimeoutException` after 2 minutes. Same result — raw 500.

**Verdict: CRITICAL (Finding #12).** User waits up to 2 minutes then sees an error.

### Failure Mode 3: Qdrant Collection Doesn't Exist

**What WILL happen:**

1. First query after fresh deployment, before any ingestion.
2. Chat handler calls `hybrid_search(client, query_dense, query_sparse)`.
3. `hybrid_search()` at L720 calls `client.query_points(collection_name="fsm_corpus")`.
4. Qdrant returns HTTP 404 (collection not found).
5. `qdrant_client` library raises `qdrant_client.http.exceptions.UnexpectedResponse` (UNVERIFIED — exact exception class depends on qdrant-client version, but it will be an exception).
6. NO try/except around `hybrid_search()` in the chat handler (L678).
7. FastAPI returns **HTTP 500**.

**Verdict: CRITICAL (Finding #4).** Predictable first-run failure with no graceful handling.

### Failure Mode 4: MASTER_LEDGER.md Missing

**What WILL happen:**

1. `load_ledger()` at L1113 checks `os.path.exists(LEDGER_PATH)`.
2. File doesn't exist → returns `""`.
3. `ledger_tokens = len(TOKENIZER.encode(""))` = 0 or trivial.
4. System prompt still contains "Pinned MASTER_LEDGER.md is the ABSOLUTE TRUTH" (L954), but no ledger content is injected.
5. LLM receives the instruction to treat the ledger as truth but no actual ledger content. This is confusing but not crashing.
6. RAG budget increases by ~2,550 tokens (the ledger's normal allocation).

**Verdict: PASS — Degrades gracefully.** The `os.path.exists` guard at L1115 handles this correctly. The system prompt reference to the ledger is mildly misleading but non-breaking.

### Failure Mode 5: PDF Has 0 Extractable Text

**What WILL happen:**

1. `parse_and_chunk(pdf_path)` at L411.
2. Docling's `converter.convert(pdf_path)` succeeds (even blank PDFs parse to a Document object).
3. `doc = result.document` at L435 — not None, just empty.
4. `chunker.chunk(doc)` at L447 produces zero chunks (or chunks with only whitespace).
5. The `if not text or not text.strip(): continue` guard at L455-456 skips all empty chunks.
6. `chunks = []` returned.
7. `ingest_pdf()` at L658 loops over zero chunks, logs "Indexed 0 chunks" at L670.
8. Returns 0. No exception raised.

**Verdict: PASS.** Silent but non-crashing. The caller receives 0 and can decide how to handle it. A log message exists. Acceptable for prototype.

### Failure Mode 6: XSS Payload in Query

**What WILL happen:**

1. Query: `<script>alert('xss')</script> what torque`
2. Goes through embed_text (text is just text to the embedding model — no risk).
3. Goes through hybrid_search (text in Qdrant payload — no execution).
4. Goes into LLM context as user message. Qwen2.5 may or may not echo the script tag.
5. LLM response JSON: `mechanic_instructions` or `diagnostic_reasoning` might contain the echoed tag.
6. **Frontend:** Architecture MANDATES DOMPurify in `renderGusResponse()` (L1004-1006). If implemented correctly, `DOMPurify.sanitize()` strips `<script>` tags before `innerHTML` injection.
7. **BUT:** The actual DOMPurify integration code is NOT shown in the architecture (Finding #13). We must take it on faith.

**Verdict: CONDITIONAL PASS.** The mandate exists (L1006). If DOMPurify is properly integrated into `renderGusResponse()`, the XSS is blocked. If not, this is a CRITICAL security vulnerability. Cannot verify from architecture document alone.

### Failure Mode 7: Chat History Exceeds Budget

**What WILL happen:**

1. User has 40-message conversation. Each turn averages ~700 tokens (question + answer).
2. `chat_history_tokens = 40 × 700 = 28,000`.
3. `build_context()` at L801-805: `available = 32768 - 900 - 2550 - 2000 - 28000 = -682`.
4. `available` is **negative**.
5. The for loop at L815-836 immediately breaks (first chunk's `total_cost > -682` is always true).
6. `context_parts = []`, `context_string = ""`.
7. RETRIEVED DOCUMENTS section is empty.
8. System prompt RETRIEVAL_FAILURE guard triggers (L978).
9. User sees: `"current_state": "RETRIEVAL_FAILURE", "mechanic_instructions": "STOP. Required documentation unavailable."`

**What's MISSING:** No warning. No logging. No chat history truncation. No indication to the user that their conversation is too long. The system just stops working.

**Additional problem:** The `chat_history` list at L910-911 is assembled by `messages.extend(chat_history)` — the entire history is sent to vLLM. If `chat_history_tokens` exceeds the total model context, vLLM itself will error (Finding #12 again).

**Verdict: CRITICAL (Findings #5, #6).** Guaranteed failure for any conversation longer than ~30-40 messages. No minimum RAG floor enforcement at runtime.

### Failure Mode 8: Docker `internal: true` + `npm pack` Egress

**What WILL happen:**

1. `npm pack pdfjs-dist@4.0.379` at L336 runs on the **host machine**, as a pre-requisite setup command.
2. The Docker network `gus_internal` with `internal: true` at L292-295 is a Docker Compose runtime network, created during `docker compose up`.
3. `docker compose build` (for the frontend Dockerfile) uses Docker's default bridge network, NOT the compose network. Build-time network isolation requires explicit `network: none` in the build config, which is not set.
4. The `npm pack` command runs BEFORE `docker compose build` — it's a host-side shell command.
5. At runtime, all containers are on `gus_internal (internal: true)` and cannot make outbound connections. ✅

**Verdict: PASS.** Build and runtime networking are correctly separated. The `npm pack` command runs on the host with full network access. The `internal: true` network only applies to running containers. No conflict.

**However:** If the frontend Dockerfile itself runs `npm install` during `docker compose build`, that WOULD require network access and would succeed (build network ≠ compose network). This is correct behavior — air-gap applies at runtime, not build-time.

---

## FINAL VERDICT

## ⛔ BLOCKED

**5 CRITICAL findings prevent deployment:**

| # | Finding | Risk |
|:--|:--------|:-----|
| 3 | No error handling for TEI failures in chat path | Single container restart = broken UI |
| 4 | No error handling for Qdrant missing collection | First-run guaranteed crash |
| 5 | No runtime RAG budget floor enforcement | Long conversations silently lose all RAG context |
| 6 | No chat history truncation mechanism | Unbounded growth → budget exhaustion → false RETRIEVAL_FAILURE |
| 12 | No error handling for vLLM failures | OOM or timeout = raw 500 error |

**CONDITIONS FOR APPROVAL (implement all to move to APPROVED WITH CONDITIONS):**

1. **Add comprehensive error handling in the chat route handler** (addresses Findings #3, #4, #12): Wrap the embed → search → generate pipeline in try/except that catches connection errors, timeouts, and HTTP errors. Return structured JSON with `current_state: "PHASE_ERROR"` and human-readable `mechanic_instructions` explaining the failure. Log the full traceback server-side.

2. **Add chat history cap with eviction** (addresses Findings #5, #6): Implement a maximum `chat_history_tokens` budget (e.g., 5,000 tokens). When exceeded, evict oldest turns first, always preserving the most recent 2 turns. Add a runtime floor check in `build_context()`: `if available < MIN_RAG_FLOOR: log warning and truncate chat history`.

3. **Add Docker healthchecks** (addresses Finding #2): Add `healthcheck` to vLLM, TEI, and Qdrant service definitions. Change gusengine's `depends_on` to `condition: service_healthy`.

4. **Add absolute relevance threshold** (addresses Finding #8): Add a `min_absolute_score` parameter to `hybrid_search()` that discards all results below an absolute RRF score floor, independent of the relative threshold. This ensures off-topic queries return empty results → `RETRIEVAL_FAILURE`.

**SIGNIFICANT findings (5) do not block deployment but should be addressed before production.**

---

**END OF HOSTILE AUDIT REPORT — V10 ARCHITECTURE**
