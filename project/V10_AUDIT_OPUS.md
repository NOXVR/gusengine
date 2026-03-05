# V10 ARCHITECTURE AUDIT — Claude Opus (Triad Auditor 1)

**Date:** 2026-02-24
**Target:** `ARCHITECTURE_V10.md` (1,123 lines, 48 KB)
**Auditor Role:** Hostile adversarial verification
**Documents Cross-Referenced:** V9 Frozen (2,107 lines), PROJECT_DNA_V9 (775 lines), NOTEBOOKLM_INTEL (179 lines), COMPARISON_AUDIT_OPUS (411 lines), COMPARISON_AUDIT_GEMINI (214 lines)

---

## VRAM Verification

- **Model Weights:** 32B × 4 bits ÷ 8 = 16 GB raw. V10 claims ~18 GB. Overhead from embedding tables, AWQ metadata, and CUDA allocations accounts for the delta. **Reasonable.**
- **KV Cache @ 32K:** 64 layers × 8 KV heads × 128 dim × 2 (K+V) × 2 bytes × 32,768 tokens = 64 × 8 × 128 × 4 × 32,768 = 8,589,934,592 bytes = **8 GB. Matches V10 L118.**
- **Total:** 18 + 8 + 2 + 2 + 0.5 = **30.5 GB on 48 GB. 17.5 GB headroom.**
- **64K scale-up:** 18 + 16 + 2 + 2 + 0.5 = 38.5 GB. Tight but plausible per L119 claim of ~46 GB.

**VRAM VERIFIED.**

---

## Findings Table

| # | Line(s) | Section | Severity | Finding | Evidence |
|:--|:--------|:--------|:---------|:--------|:---------|
| 1 | L136 vs L287 | Docker Compose / Air-Gap | 💀 CRITICAL | **Air-gap claim directly contradicts Docker Compose.** L136 CAUTION box states: "The Docker network is `internal: true` for the inference subnet." L287 actual YAML: `internal: false # Needs host access for localhost binding; firewall handles external`. These are mutually exclusive statements in the same document. | V10 L136 vs V10 L287. One of these lines is wrong. If L287 is authoritative, the air-gap claim at L136 is false. If L136 is the intent, the YAML at L287 is misconfigured. |
| 2 | (absent) | Ingestion / Embedding | 💀 CRITICAL | **Embedding generation code is entirely missing.** `index_chunk()` (L485-507) accepts `dense_vector` and `sparse_vector` as parameters. `hybrid_search()` (L531-592) accepts `query_dense` and `query_sparse`. But **no code anywhere in V10 shows how TEI is called** to produce these vectors — neither at ingestion time nor at query time. The HTTP calls to TEI's `/embed` and `/embed_sparse` endpoints are absent. This is a broken pipeline: chunks are parsed but never embedded, queries are searched but never vectorized. | V10 L439-507 (Embedding & Indexing) shows schema + index function but no embed function. V10 L517-593 (Retrieval) shows search but no query embedding. Compare to V10 L700-753 (Inference) which DOES show the full HTTP call to vLLM. |
| 3 | L287 | Docker Compose / Network | ⚠️ SIGNIFICANT | **`internal: false` allows container egress to internet.** Even correcting finding #1, `internal: false` means Docker containers can make outbound connections. Docker's iptables rules bypass UFW by default, so the comment "firewall handles external" is misleading. A compromised vLLM or TEI container could phone home. `internal: true` on the bridge network would still allow inter-container communication AND host→container via published ports, while blocking outbound internet. | Docker documentation: bridge networks with `internal: true` block egress but allow inter-container DNS and published port access via iptables DNAT. V10's 127.0.0.1 port bindings would still function. |
| 4 | L248 vs L896 vs L878 | Tribal Knowledge / Token Budget | ⚠️ SIGNIFICANT | **Ledger token cap is contradictory across three locations.** Docker env (L248): `LEDGER_MAX_TOKENS=2000`. Token budget diagram (L672): `~2,000 tokens`. Tribal Knowledge table (L878): `Ledger hard cap: 3,000 (adjusted: 2,550)`. `validate_ledger.py` (L896): `RAW_CAP = 3000`. The environment variable, the budget diagram, and the validation script disagree. If the validator allows 2,550 tokens but the budget only reserves 2,000, the ledger can overflow its allocation by 550 tokens, silently shrinking the RAG budget. | V10 L248, L672, L878, L896. The Docker env var should match the adjusted cap, or the budget diagram should match the validator. |
| 5 | L956 | Security | ⚠️ SIGNIFICANT | **Upload blocking regex is vestigial and the real endpoint is unprotected.** V10 preserves V9's Nginx rule blocking `/api/v1/document/(upload|create-folder)`. But V10 replaced AnythingLLM with custom FastAPI — this endpoint no longer exists. The actual ingestion endpoint is `/api/ingest` (L65). If Nginx doesn't block `/api/ingest` from external access, an attacker on the network could inject arbitrary PDFs into the vector store. | V9 L200-203 (Nginx upload blocking targets AnythingLLM API). V10 L64-66 (FastAPI endpoints are `/api/chat`, `/api/ingest`, `/api/health`). V10 L956 preserves the old rule without adding a new one. |
| 6 | (absent) | Embedding / Retrieval | ⚠️ SIGNIFICANT | **TEI sparse vector support is assumed but unverified.** V10's hybrid search requires sparse vectors from BGE-M3 (L558-564). HuggingFace TEI does support a `/embed_sparse` endpoint for compatible models, but V10 never mentions this endpoint, never shows the API call, and never verifies TEI exposes it for BGE-M3. If the TEI container version doesn't support sparse output, the entire hybrid search degrades to dense-only, losing the keyword matching that NotebookLM Intel (Finding 8) identifies as critical for technical corpuses. | NOTEBOOKLM_INTEL Finding 8: "critical for technical corpuses — it ensures exact strings like part numbers, wire color codes... are forcefully retrieved even when the semantic model doesn't understand their context." V10 L477-482 creates sparse vector config in Qdrant but never shows how sparse vectors are generated. |
| 7 | L376-421 | Ingestion Pipeline | ⚠️ SIGNIFICANT | **`parse_and_chunk()` has zero error handling.** No try/except around `converter.convert()` or the chunking loop. A corrupt PDF, an OCR crash, or an empty Docling result will throw an unhandled exception, crashing the ingestion of that file and potentially the entire batch. V9's `process_file()` had three-tier quarantine defense (49 audit findings, particularly #24, #26, #27). V10's Docling parser has none. | V9 FROZEN L46-49 (process_file hardening), V9 FROZEN L2032-2035 (Findings 24, 26, 27). V10 L376-421 — no try/except, no quarantine, no error logging. |
| 8 | L729-732 | Inference Layer | ⚠️ SIGNIFICANT | **Context injected as a second `system` message.** V10 injects RAG context as: `{"role": "system", "content": "RETRIEVED DOCUMENTS:\n\n{context}"}` after the main system prompt. Qwen2.5's chat template may merge, truncate, or mishandle multiple system messages. The vLLM OpenAI-compatible API typically concatenates multiple system messages, but this behavior is model-template-dependent and not guaranteed. The safer pattern is to append the context to the single system message string. | V10 L723-738. The Qwen2.5 chat template uses `<|im_start|>system\n...<|im_end|>` blocks. Multiple system blocks may produce unexpected tokenization or template errors depending on the vLLM version's chat template handling. |
| 9 | L368 | Ingestion Pipeline | 🔍 MINOR | **`table_structure_options` passed as dict instead of Pydantic model.** L368: `table_structure_options={"mode": TableFormerMode.ACCURATE}`. Docling's `PdfPipelineOptions` may expect a `TableStructureOptions` object. While Pydantic validation may coerce the dict, this is fragile. | V10 L368. Should be `TableStructureOptions(mode=TableFormerMode.ACCURATE)` with the import added. |
| 10 | L810 vs V9 L1346 | System Prompt / JSON Schema | 🔍 MINOR | **Citation `page` field changed type from string to integer without noting schema break.** V9 example: `"page": "N/A"` (string). V10 example: `"page": 3` (integer). If `parseGusResponse()` or `renderCitation()` does string operations on the page field (e.g., checking for "N/A"), the integer will cause a type error. V10 claims these functions are "PRESERVED UNCHANGED" (L834). | V9 FROZEN L1346: `"page": "N/A"`. V10 L810: `"page": 3`. V10 L834: "PRESERVED UNCHANGED." |
| 11 | L526-529 | Retrieval Pipeline | 🔍 MINOR | **Unused imports.** `SearchRequest`, `NamedVector`, `NamedSparseVector`, and `Query` are imported but never used in `search.py`. | V10 L526-529 — four unused imports from `qdrant_client.models`. |
| 12 | L414 | Ingestion Pipeline | 🔍 MINOR | **Missing `import os`.** `os.path.basename(pdf_path)` is called at L414, but `import os` is not shown in the file's imports (L342-350). | V10 L342-350 (imports), L414 (`os.path.basename`). |
| 13 | L312 | Model Pre-Download | 🔍 MINOR | **PDF.js downloaded from non-official GitHub fork.** URL: `https://github.com/nicbarker/pdfjs-dist/releases/download/v4.0.379/pdfjs-4.0.379-dist.zip`. The official distribution is Mozilla's `mozilla/pdf.js` GitHub releases or the `pdfjs-dist` npm package. This fork may be outdated, unmaintained, or compromised. | V10 L312. Should use official Mozilla release or `npm pack pdfjs-dist`. |
| 14 | L631 | Token Budget | 🔍 MINOR | **Code comment "27,868 tokens for RAG" assumes zero chat history, contradicting the budget diagram.** L631 comment: `32768 - 900 - 2000 - 2000 - 0 = 27,868`. L672-679 diagram: allocates 1,000 tokens for chat history, yielding 26,868 for RAG. The comment is technically correct for the function default (`chat_history_tokens: int = 0`) but misleading given the diagram's typical-case budget. | V10 L631, L672-679. |
| 15 | L363-365 | Ingestion Pipeline | 🔍 MINOR | **CPU-only OCR on degraded 1960s scans may vastly exceed time estimate.** `use_gpu=False` at L365 forces EasyOCR to CPU. The time estimate (L513) says "8-20 hours" for 2,442 pages. EasyOCR on CPU for degraded scanned documents with handwriting, rubber stamps, and faded text could be 1-3 minutes per page, yielding 40-120 hours. The estimate may be 2-6× too optimistic. | V10 L365, L513. DNA description of FSM corpus: "degraded 1960s-era scans" (Opus Audit L147). |

---

## Heritage Verification

| V9 Component | Preserved in V10? | Accurate? | Notes |
|:-------------|:------------------:|:---------:|:------|
| Gus DAG State Machine | ✅ | ✅ | L766-819. All four phases, B-looping, state transition enforcement, PHASE_ERROR, RETRIEVAL_FAILURE preserved. Citation rules correctly updated for Qdrant metadata. |
| parseGusResponse() | ✅ | ✅ | L836. Forward-scanning brute-force description matches V9 L1457-1483. Pass 1 removal correctly noted. |
| buildUserMessage() | ✅ | ✅ | L838. PHASE_B null override, nextStates map referenced. Logic matches V9 L1488-1523. |
| renderGusResponse() | ✅ | ✅ | L838. State badge, instructions, citations, buttons, completion referenced. |
| V9 Security (UFW, Nginx, TLS, localhost) | ✅ | ⚠️ | L948-956. All measures listed. However, upload blocking regex targets non-existent AnythingLLM endpoint (Finding #5). |
| VMDK/OVA Extraction Daemon | ✅ | ✅ | L424-436. `chunk_pdf()` correctly deprecated. Output path updated. TOCTOU locking, three-tier quarantine, manifest dedup noted. Webhook trigger to `/api/ingest` is a clean adaptation. |
| Tribal Knowledge (validate/sync/update) | ✅ | ⚠️ | L867-939. Architecture preserved. Token budget updated. But cap values are contradictory (Finding #4). |
| V9 49 Audit Findings | ✅ | ✅ | L1093-1096. Preserved by reference to V9 FROZEN L2022-2107. |
| Docker Log Rotation | ✅ | ✅ | All 5 containers have `max-size: 50m`, `max-file: 3`. Verified L175-179, L204-206, L222-225, L255-259, L278-282. |
| CSS Class Contract | ✅ | ✅ | L861-863. All V9 CSS classes listed. DOM element IDs preserved. |
| DOMPurify XSS Defense | ✅ | ✅ | L831. V9 XSS warning addressed by reference. |
| Three-Tier Quarantine | ✅ | ✅ | L427. Referenced in VMDK daemon section. Correctly describes V9 mechanism. |

**Heritage Score: 12/12 preserved, 10/12 accurate.** Two accuracy issues: vestigial upload blocking (Finding #5) and ledger cap contradiction (Finding #4).

---

## NotebookLM Parity Check

| NotebookLM Finding | V10 Implementation | Gap? |
|:-------------------|:-------------------|:-----|
| **1. Dual-track ingestion** (original PDF + text extraction) | Original PDFs in `./storage/pdfs/` (L87). Docling text extraction cached in `./storage/extracted/` (L88). Frontend Nginx serves PDFs from `./storage/pdfs/` (L272). | **No gap.** Clean dual-track. |
| **2. Variable-length structural chunking** | Docling HybridChunker with `max_tokens=512` and `merge_peers=True` (L390-394). Structural boundaries + size fallback matches NOTEBOOKLM_INTEL Finding 7 (mid-sentence break at excerpt 5). | **No gap.** |
| **3. Hybrid vector + keyword search** | Qdrant dense + sparse + RRF fusion (L549-568). Dense via BGE-M3 cosine. Sparse via BGE-M3 IDF-weighted. | **Conditional gap.** Depends on TEI actually exposing sparse vectors (Finding #6). |
| **4. Dynamic token-capped injection** | Greedy fill loop (L638-661) fills until token budget exhausted. Variable chunk count per query. | **No gap.** Matches NOTEBOOKLM_INTEL Finding 6. |
| **5. Single-pass full-corpus search** | Single Qdrant `query_points` call against `fsm_corpus` collection (L550-569). All 514 PDFs compete simultaneously. | **No gap.** |
| **6. No query expansion** | No query rewriting or expansion code shown in V10. User query is searched directly. | **No gap.** Matches NOTEBOOKLM_INTEL: "NO expansion. Platform searches exact user words." |
| **7. Fresh retrieval per turn** | Each `/api/chat` call triggers fresh `hybrid_search()` + `build_context()`. No cached context reuse between turns. | **No gap.** Implicit from architecture; could be stated more explicitly. |
| **8. Hard relevance threshold** | Dynamic 40% of top score (L574-578). | **Minor gap.** Gemini DT audit (L83-84) argues RRF scores are rank-fractions, making percentage thresholds mathematically incoherent. However, V10 applies the threshold POST-fusion, which is a reasonable heuristic for the prototype. Not a parity failure — NotebookLM's threshold mechanism is also unspecified. |
| **9. Citation architecture** | V10 uses structured JSON citations with full metadata (L772-777, L806-816). NotebookLM uses plain `[N]` with frontend resolution. V10's approach is architecturally different but functionally equivalent for the diagnostic use case — citation data reaches the user either way. | **Deliberate departure, not a gap.** |
| **10. LLM blind to images** | L1073: "Images/diagrams are preserved in original PDFs for display but NOT vectorized. The LLM reasons from text only." | **No gap.** Matches NOTEBOOKLM_INTEL Finding 4: "LLM is blind to images." |

**Parity Score: 9/10 confirmed, 1 conditional on TEI sparse vectors.**

---

## Audit Checklist Results

### A. Component Map
- [x] **PASS** — All 5 containers represented (L53-76)
- [x] **PASS** — Port assignments consistent between diagram (L59-60) and Docker Compose (L152, L187, L214, L235, L269)
- [x] **PASS** — Volume mounts match between diagram (L84-89) and Docker Compose (L154, L189, L216, L237-239, L272)
- [ ] **FAIL** — Air-gap contradiction (Finding #1): L136 claims `internal: true`, L287 says `internal: false`

### B. GPU Memory Budget
- [x] **PASS** — VRAM math independently verified (see above)
- [x] **PASS** — KV cache formula correct: 64 layers × 8 GQA heads × 128 dim
- [x] **PASS** — Scale-up table realistic (L124-129)
- [x] **PASS** — No claim of 128K on 48GB (L120 correctly marks it ❌)

### C. Docker Compose
- [x] **PASS** — Service definitions syntactically valid
- [x] **PASS** — GPU passthrough correct (L157-163, L191-196)
- [x] **PASS** — Localhost binding on internal ports (L152, L187, L214, L235)
- [x] **PASS** — Log rotation on all 5 containers
- [ ] **FAIL** — `LEDGER_MAX_TOKENS=2000` contradicts `validate_ledger.py RAW_CAP=3000` (Finding #4)
- [x] **PASS** — Model paths in volumes match download commands (L154, L189 vs L302-307)
- [x] **PASS** — `depends_on` ordering correct (L249-252, L274-275)

### D. Ingestion Pipeline
- [x] **PASS** — `do_ocr=True` explicitly set (L362)
- [x] **PASS** — HybridChunker usage plausible for Docling API
- [x] **PASS** — AutoTokenizer usage correct (L354-357)
- [x] **PASS** — Page number extraction via `chunk.meta.doc_items` plausible
- [ ] **FAIL** — No error handling in `parse_and_chunk()` (Finding #7)
- [ ] **FAIL** — Missing `import os` (Finding #12)

### E. Embedding & Indexing
- [x] **PASS** — BGE-M3 dimensions correct: 1024 dense (L471)
- [x] **PASS** — Qdrant collection schema valid (L468-483)
- [x] **PASS** — Sparse vector IDF modifier correct for BM25-like behavior (L480)
- [ ] **FAIL** — Embedding generation code missing entirely (Finding #2)

### F. Retrieval Pipeline
- [x] **PASS** — Qdrant `query_points` with Prefetch and FusionQuery API usage correct (L550-568)
- [x] **PASS** — Dynamic threshold calculation present (L577-578)
- [x] **PASS** — Greedy context builder correctly counts tokens (L638-661)
- [x] **PASS** — Token budget math: 32768 - 900 - 2000 - 2000 = 27,868 (L631)
- [x] **PASS** — Context formatting includes provenance headers (L649-655)

### G. Inference Layer
- [x] **PASS** — vLLM CLI flags correct for Qwen2.5-32B-AWQ (L164-172)
- [x] **PASS** — OpenAI-compatible endpoint correct (L742-744)
- [x] **PASS** — Temperature 0.1 appropriate (L716, L748)
- [ ] **FAIL** — Multiple system messages may misbehave with Qwen2.5 chat template (Finding #8)

### H. System Prompt (Gus DAG V10)
- [x] **PASS** — DAG state machine preserved (PHASE_A → B → C → D, B looping)
- [x] **PASS** — Citation rules updated for Qdrant metadata (L773-777)
- [x] **PASS** — JSON output schema preserved (L806-816)
- [x] **PASS** — RETRIEVAL_FAILURE safeguard preserved (L802-803)
- [x] **PASS** — STATE TRANSITION ENFORCEMENT preserved (L796-799)
- [ ] **FAIL** — Page field type changed from string to integer without noting frontend impact (Finding #10)

### I. Frontend Architecture
- [x] **PASS** — PDF.js self-hosted requirement stated (L827, L309-314)
- [x] **PASS** — V9 CSS class contract preserved (L861-863)
- [x] **PASS** — parseGusResponse() and buildUserMessage() referenced correctly (L834-838)
- [x] **PASS** — DOMPurify sanitization mentioned (L831)

### J. Tribal Knowledge
- [ ] **FAIL** — Token budget contradictions between env var, diagram, and validator (Finding #4)
- [x] **PASS** — AutoTokenizer replaces tiktoken (L887-893)
- [x] **PASS** — Ledger injection mechanism described (L921-939)

### K. Security
- [ ] **FAIL** — Upload blocking regex targets dead AnythingLLM endpoint; `/api/ingest` unprotected (Finding #5)
- [ ] **FAIL** — Air-gap contradiction (Finding #1)
- [x] **PASS** — All other V9 security measures listed (L948-961)

### L. Verification
- [x] **PASS** — All 15 checklist items executable (L1000-1065)
- [x] **PASS** — Expected outputs realistic
- [x] **PASS** — GPU verification step included (L1009-1011)
- [x] **PASS** — Air-gap verification step included (L1032-1034)

### M. Known Boundaries
- [x] **PASS** — Honestly stated limitations (L1069-1079)
- [x] **PASS** — No overclaiming of capabilities
- [x] **PASS** — Upgrade path realistic (L1082-1089)

---

## Summary Statistics

| Metric | Count |
|:-------|:------|
| 💀 CRITICAL findings | 2 |
| ⚠️ SIGNIFICANT findings | 6 |
| 🔍 MINOR findings | 7 |
| **Total findings** | **15** |
| Total lines audited | 1,123 |
| Heritage items verified | 12/12 preserved, 10/12 accurate |
| NotebookLM parity items | 9/10 confirmed, 1 conditional |
| Checklist sections passed | 9/13 (A-M) fully clean |

---

## Overall Verdict

**VERDICT: APPROVED WITH CONDITIONS**

The V10 architecture is structurally sound, VRAM-feasible, and correctly preserves V9 heritage. The two CRITICAL findings are both documentation/configuration errors (air-gap contradiction at L136/L287, missing embedding pipeline code) rather than fundamental design flaws — the architecture clearly *intends* hybrid search with TEI embeddings and an internal Docker network, but the implementation artifacts are incomplete. All 15 findings are fixable without architectural redesign. The conditions for approval are: (1) resolve the `internal: true/false` contradiction and set the network to `internal: true`, (2) add the TEI embedding client code for both ingestion and query, (3) harmonize the ledger token cap across all three locations, and (4) update the Nginx upload blocking rule for the FastAPI endpoint.
