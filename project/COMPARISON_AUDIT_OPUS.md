# V10 Deep Research Comparison — Independent Audit Report

**Auditor:** Independent AI Agent (Adversarial Audit)
**Date:** 2026-02-24
**Subject:** Cross-examination of `DEEP_RESEARCH_COMPARISON.md` against all four source documents

---

## SECTION 1: NOTEBOOKLM ALIGNMENT VERIFICATION

The comparison document evaluates each research result against 13 findings derived from `NOTEBOOKLM_INTEL.md`. Below is a line-by-line verification of each score.

### Finding 1: Dual-Track Ingestion Pipeline

**NotebookLM Finding:** Original untouched PDF saved as-is (Track 1); OCR/text extraction creates plain-text excerpts + position metadata map (Track 2).

- **R1 score: YES** → **AGREE.** R1's `extract_structural_metadata()` copies the master PDF to `MASTER_PDF_DIR` (Track 1) and generates structural JSON excerpts with bounding boxes (Track 2). Confirmed at R1 lines 182-186.
- **R2 score: YES** → **AGREE.** R2 describes storing master PDFs and using Docling for structural extraction with spatial metadata. Section A explicitly addresses this.
- **R3 score: YES** → **AGREE.** R3 explicitly names "Dual-Track Spatial Pipeline" and stores raw PDFs in `/var/lib/gusengine/pdfs/raw/` (Track 1) with Docling-parsed JSON in `/var/lib/gusengine/metadata/parsed/` (Track 2).

### Finding 2: Variable-Length Structural Chunking (NOT Fixed-Size)

**NotebookLM Finding:** Excerpts follow structural document boundaries (page breaks, paragraph returns, text-box coordinates). Not fixed-length. Size cap exists (mid-sentence break observed).

- **R1 score: YES** → **AGREE.** R1 uses PyMuPDF font/bold detection for heading boundaries with `MAX_CHARS = 1500` as a fallback cap. This mirrors NotebookLM's "structural-priority WITH a maximum size fallback" exactly.
- **R2 score: YES** → **AGREE.** R2 recommends Docling's `HybridChunker` which "respects document section boundaries (headings, page breaks, paragraphs), producing variable-length excerpts."
- **R3 score: YES** → **AGREE.** R3 uses Docling's `HybridChunker` with `max_tokens=600` and `merge_peers=True`. Tokenizer-aware chunking with structural boundaries.

### Finding 3: Bounding Box Spatial Metadata

**NotebookLM Finding:** Metadata map links each text excerpt to exact page number and spatial coordinates (X/Y bounding boxes).

- **R1 score: YES** → **AGREE.** R1 computes merged `[x0, y0, x1, y1]` bounding boxes from PyMuPDF block data (R1 lines 216-219).
- **R2 score: YES** → **AGREE.** R2 states Docling produces "page_no, bbox: {l, t, r, b}, heading path, and element type" per chunk.
- **R3 score: YES** → **AGREE.** R3 extracts `prov.bbox` with `{l, t, r, b}` coordinates from Docling's Pydantic metadata hierarchy (R3 lines 254-267).

### Finding 4: Hybrid Vector + Keyword Search

**NotebookLM Finding:** Parallel vector (cosine similarity) + lexical/keyword (BM25) search with simultaneous execution.

- **R1 score: YES** → **AGREE.** R1 uses LanceDB vector search + Tantivy FTS in parallel (R1 lines 454-457).
- **R2 score: YES+ (exceeds)** → **AGREE.** R2 uses Qdrant dense + sparse BM25 + RRF with additional `keyword` payload indexes for exact part numbers. The "exceeds" designation is justified.
- **R3 score: YES** → **AGREE.** R3 uses Qdrant `prefetch` API with parallel dense + sparse BM25 queries fused via RRF (R3 lines 537-556).

### Finding 5: 190 Excerpts from 30 Documents

**NotebookLM Finding:** 190 excerpts from 30 docs retrieved in a single response, dynamically token-limited.

- **R1 score: NO (85% gap)** → **AGREE.** R1 caps at 4,000 tokens (~25-35 excerpts). The comparison is correct this is a massive gap.
- **R2 score: YES** → **AGREE.** R2's Claude 200K context allows 158,000-182,000 tokens for excerpts. The math is sound.
- **R3 score: YES** → **AGREE.** R3's 100K token budget ÷ ~526 avg tokens = ~190 excerpts. The math is validated in R3's Appendix A.

### Finding 6: Dynamic Token-Capped Injection

**NotebookLM Finding:** Number of excerpts is NOT fixed — varies dynamically based on excerpt length, capped by context window.

- **R1 score: YES** → **AGREE.** R1 implements a `while` loop that fills until `tokens_used + toks > MAX_TOKENS` (R1 line 485).
- **R2 score: YES+ (exceeds)** → **AGREE.** R2 adds diversity/redundancy scoring on top of token-capping. "Exceeds" is justified.
- **R3 score: YES** → **AGREE.** R3 iterates through RRF results with `current_tokens + estimated_tokens > max_tokens` check (R3 lines 567-570).

### Finding 7: Single-Pass Full-Corpus Search

**NotebookLM Finding:** Retrieval searches the entire unified database of ALL uploaded sources simultaneously. No pre-filtering.

- **R1 score: YES** → **AGREE.** R1 searches the entire LanceDB `fsm_corpus` table.
- **R2 score: YES** → **AGREE.** R2 searches the entire Qdrant collection.
- **R3 score: YES** → **AGREE.** R3 searches the entire `fsm_hybrid_corpus` collection in Qdrant.

### Finding 8: No Query Expansion

**NotebookLM Finding:** "NO expansion. Platform searches exact user words via both lexical and vector tracks. No rephrasing, no appended terms." However, NotebookLM DOES contextualize: "New user input is contextualized with conversation history before searching."

- **R1 score: YES** → **DISAGREE — should be PARTIAL.** R1 does NOT search exact user words. R1 line 451 reads: `search_query = f"{history_text} {req.message}".strip()` — it concatenates the last 4 history messages with the current query before embedding. While this isn't LLM-based rewriting, it IS query expansion via prepended history text. This changes the vector embedding of the query and the FTS keyword matching significantly. NotebookLM confirmed it contextualizes with history, but R1's naive concatenation is a different mechanism (dump all history text into the query string) than NotebookLM's likely more sophisticated contextualization. At best this is PARTIAL, not YES.

- **R2 score: NO** → **AGREE.** R2 explicitly uses Claude Haiku to "generate 2-3 retrieval queries" — this is full query expansion, contradicting the NotebookLM finding.

- **R3 score: PARTIAL** → **AGREE.** R3 uses LLM-based query contextualization (rewriting the query incorporating conversation history). This is closer to NotebookLM's behavior than R2's multi-query approach but still involves rephrasing, which NotebookLM says it doesn't do.

**Scoring inconsistency identified:** R1 gets YES while doing naive history concatenation (a form of query modification), but R3 gets PARTIAL for LLM-based contextualization. Both modify the query before search. R1 should be PARTIAL at most. This inflates R1's score by 1 point.

### Finding 9: Turn-Based Fresh Retrieval

**NotebookLM Finding:** Fresh retrieval every turn. Context window is FLUSHED between turns. New user input is contextualized with conversation history before searching.

- **R1 score: YES** → **AGREE.** R1's gateway is stateless; frontend manages rolling 4-message history. Context is rebuilt fresh each turn.
- **R2 score: PARTIAL** → **AGREE.** R2 discusses conversation history compression and "preserves the last 4 turns verbatim" but never explicitly addresses the turn-based flush model. "PARTIAL" is fair.
- **R3 score: YES** → **AGREE.** R3's retriever accepts `chat_history` as a parameter and rebuilds context from scratch each turn.

### Finding 10: Citation Architecture — LLM Outputs Plain [N]

**NotebookLM Finding:** LLM outputs raw plain-text `[N]` integers. No metadata, no hidden code, no structured reference objects.

- **R1 score: YES** → **AGREE.** R1's system prompt mandates: "the 'source' field MUST ONLY contain the plain integer bracket" (R1 line 579).
- **R2 score: YES** → **AGREE.** R2 implies this through the citation event emitter architecture where the LLM outputs `[N]` and the frontend resolves metadata.
- **R3 score: YES** → **AGREE.** R3's system prompt explicitly states: "Output the citation STRICTLY as a bracketed integer" (R3 line 611).

### Finding 11: Frontend Resolves Metadata/PDF Crops

**NotebookLM Finding:** Frontend intercepts `[N]` markers, cross-references metadata map, fetches page from master PDF, crops/focuses based on coordinates.

- **R1 score: YES** → **AGREE.** R1's `renderCitations()` JS function reads `[N]`, looks up `globalMetadataMap`, and fetches `/api/v10/render_crop` with bounding box parameters.
- **R2 score: YES+ (exceeds)** → **AGREE.** R2 provides a dual-UX model: pre-rendered WebP hover (instant) + PDF.js click-through with bounding box highlight. The "exceeds" designation is justified.
- **R3 score: YES+ (exceeds)** → **AGREE.** R3 provides a full React `CitationRenderer` component using `@react-pdf-viewer/highlight` with mathematical coordinate conversion from Docling's absolute bbox to percentage-based highlight areas.

### Finding 12: Hard Relevance Threshold

**NotebookLM Finding:** "A hard relevance threshold discards low-confidence matches (prevents noise)."

- **R1 score: YES** → **AGREE.** R1 implements `if scores[cid] < 0.015: continue` (R1 line 480).
- **R2 score: YES** → **AGREE.** R2 implements "40% of the top score" dynamic threshold + score-gap detection.
- **R3 score: NO** → **AGREE.** R3 has no threshold — iterates through RRF results until token budget is exhausted. The system prompt instructs the LLM to "silently ignore" lexical collisions, but this is not a retrieval-layer threshold as NotebookLM describes. Correct score.

### Finding 13: Section Titles from OCR Heading Detection

**NotebookLM Finding:** "During OCR, platform detects document hierarchy via bold text and larger font sizes, stores as heading metadata."

- **R1 score: YES** → **AGREE.** R1 detects headings via `"bold" in s.get("font", "").lower() or s["size"] > 11.5` (R1 line 208).
- **R2 score: YES** → **AGREE.** R2 states Docling classifies elements into categories including "Title" and "Text."
- **R3 score: YES** → **AGREE.** R3 uses Docling which detects Title elements; `HybridChunker.contextualize()` preserves heading hierarchy.

---

### ALIGNMENT SCORE CORRECTIONS

| Result | Comparison Score | Corrected Score | Discrepancy |
|:-------|:-----------------|:----------------|:------------|
| **R1** | **11/13** | **11/13** (but for different reasons) | The comparison claims 2 gaps: "context depth" (correct) and "model quality" (not one of the 13 findings). The actual gaps should be: (1) 190 excerpts = NO, (2) No query expansion = should be PARTIAL, not YES. Net effect: 11 full + 1 partial + 1 no = still reportable as 11/13, but the composition is different. |
| **R2** | **11/13** | **11/13** | Confirmed. |
| **R3** | **11/13** | **11/13** | Confirmed. |

**Critical note on R1:** The comparison states R1's score is "11/13" with "2 critical gaps (context depth, model quality)." But "model quality" (Llama 8B vs frontier model) is NOT one of the 13 NotebookLM findings being scored. Looking at R1's alignment table, R1 actually receives 12 YES and 1 NO, which should be 12/13. The comparison arrives at 11/13 by counting an extra-tabular concern (model quality) as a finding gap. If the "No query expansion" finding is corrected to PARTIAL for R1 (as argued above), the score becomes 11 YES + 1 PARTIAL + 1 NO = effectively 11/13. **The final number is coincidentally correct, but the reasoning is wrong.** The comparison should show R1 failing on Finding 5 (190 excerpts) and partially meeting Finding 8 (no query expansion), not on a phantom "model quality" finding.

---

## SECTION 2: MISSED FINDINGS AUDIT

### Research 1 — Missed Strengths

1. **VMDK/OVA ingestion pipeline preserved.** R1 uniquely preserves the V9 capability to extract PDFs from VMDK disk images and OVA virtual appliances (R1 lines 248-295). Neither R2 nor R3 address this. The comparison does not credit R1 for this capability, which may be critical if the mechanic's FSM corpus is delivered in virtual machine format.

2. **TOCTOU-immune file locking.** R1 implements a `wait_for_stable()` function (R1 lines 163-179) that performs double-verification file locking to prevent race conditions during PDF ingestion. This V9 inherited safeguard is not mentioned in the comparison.

3. **Manifest-based deduplication.** R1 uses SHA-256 hashing and a `manifest.json` to prevent re-processing already-ingested files (R1 lines 252-253). Neither the comparison nor R2/R3 address ingestion idempotency at this level.

### Research 1 — Missed Weaknesses

1. **CRITICAL: PyMuPDF cannot OCR scanned PDFs.** This is the single most important omission in the entire comparison. PyMuPDF's `get_text("dict")` extracts text from digitally-authored PDFs, but the entire FSM corpus consists of "degraded 1960s-era scans." Scanned PDFs contain only raster images — PyMuPDF will extract ZERO text from them without an external OCR engine. R1 installs no OCR engine (no Tesseract, no EasyOCR, no Surya). The comparison notes that R2 has "OCR fallback" as a strength and that R1 uses "PyMuPDF raw dict" as inferior to Docling, but it never identifies that **R1's parsing pipeline will produce empty output for the majority of the corpus.** This should be rated **CRITICAL**, not merely a comparative weakness. The comparison's OCR/degraded scans star rating gives R1 ★★☆☆☆ — this should be ☆☆☆☆☆ or "NOT FUNCTIONAL."

2. **No table extraction.** The comparison mentions R1 "had no table handling," but this is buried in R2's strengths list rather than being flagged as a standalone R1 weakness. FSM spec tables containing torque values and tolerances are safety-critical.

### Research 1 — Missed Factual Errors

1. **`all-MiniLM-L6-v2` has a 256-token (not 512-token) effective max input.** The comparison states R1's model has "512 max tokens" in the head-to-head table. While the model technically supports 512 tokens, performance degrades significantly beyond 256 tokens. For structural excerpts up to 1500 characters (~375 tokens), many excerpts will exceed the model's effective window. This is not a factual error in R1 itself, but a factual error in the comparison's characterization.

### Research 2 — Missed Strengths

1. **Matryoshka embedding mention (nomic-embed-text-v1.5).** R2 identifies truncatable dimensional representations for storage savings. The comparison does not mention this as a potential optimization path.

2. **Weaviate `autocut` feature noted as comparison.** R2's evaluation of alternative vector stores includes discussion of Weaviate's built-in score-based truncation, providing useful context for why Qdrant was selected. Not captured in the comparison.

3. **RAG Document Viewer by Preprocess.co.** R2 identifies a specific frontend component that "auto-scrolls and spotlights the cited region in a self-contained HTML bundle embeddable via iframe." This is a potentially valuable shortcut for the citation rendering system that the comparison does not capture.

### Research 2 — Missed Weaknesses

1. **Query rewriting generates MULTIPLE retrieval queries.** The comparison notes R2's "query rewriting with Claude Haiku" but doesn't emphasize that R2 generates "2-3 retrieval queries" per turn. This means multiple Qdrant searches per turn, increasing latency and complexity. This is a significant architectural difference from NotebookLM's single-pass model.

2. **No conversation history flushing mechanism specified.** The comparison rates this as PARTIAL for turn-based fresh retrieval, but doesn't flag that R2's "conversation history compression" (summarizing older turns) is architecturally opposite to NotebookLM's full flush model. R2 carries forward compressed history, while NotebookLM starts fresh each turn.

### Research 2 — Missed Factual Errors

None found beyond those identified in the comparison.

### Research 3 — Missed Strengths

1. **Lexical collision filtering in system prompt.** R3's system prompt explicitly instructs the LLM to "analyze the current diagnostic context and silently ignore all injected excerpts that represent lexical collisions or irrelevant systems" with the "vacuum" example (R3 line 614). The comparison mentions this at point #8 of R3's strengths, so this is captured. Confirmed.

2. **Qdrant snapshot before DR backup.** R3's backup script runs `curl -X POST .../snapshots` before `rsync` to ensure consistency (R3 line 648). The comparison mentions this at point #12. Confirmed.

### Research 3 — Missed Weaknesses

1. **No OCR capability in Docling configuration.** R3's `initialize_parser()` function (R3 lines 187-204) configures Docling with `do_table_structure=True` and image generation disabled, but does NOT set `do_ocr=True`. R2 explicitly recommends `do_ocr: True` as mandatory for scanned vintage manuals. Without OCR enabled, Docling will perform layout analysis on the visual structure but may fail to extract text from scanned pages. The comparison does not flag this configuration omission.

2. **vLLM `--max-model-len 131072` memory requirements.** R3 sets `--max-model-len 131072` in the vLLM config (R3 line 91). The KV cache memory for a 70B model at 128K context length is enormous — potentially 40-60GB+ depending on quantization. Combined with model weights (~35-40GB at INT4), this likely exceeds the 48GB available across dual RTX 4090s. The comparison flags the "Dual RTX 4090 requirement" as MEDIUM severity but doesn't do the specific memory math. This should be CRITICAL — the system may not boot as configured.

3. **`pdfjs-dist` worker URL points to unpkg.com CDN.** R3's CitationRenderer component loads `pdf.worker.min.js` from `https://unpkg.com/pdfjs-dist@3.4.120/build/pdf.worker.min.js` (R3 line 746). This violates the air-gapped requirement — unpkg.com is an external CDN. The comparison does not catch this. The worker must be self-hosted.

4. **LangChain imports beyond contextualization.** The comparison flags the LangChain dependency but focuses only on the removal path. The deeper issue is that R3's `ChatPromptTemplate.from_messages()` call (R3 line 505) appears to have an empty list argument — the actual prompt template content is missing from the document (likely a rendering artifact from the Google Docs export). This means the contextualization logic cannot be verified.

### Research 3 — Missed Factual Errors

1. **Qdrant version mismatch.** R3 uses `qdrant/qdrant:v1.10.0` in the Docker config (R3 line 314). The comparison's factual error section catches this correctly — v1.10.0 introduced basic hybrid search but v1.15.2+ is needed for server-side BM25 tokenization. However, the comparison buries this in the factual errors table rather than connecting it to the component selection, which recommends "Qdrant ≥ v1.15.2."

2. **Empty list initializations.** The comparison notes `chunks_data =` and `points =` appear empty (R3 lines 248, 410), but attributes this to "likely rendering issue." In fact, these are clearly `chunks_data = []` and `points = []` that lost their brackets during Google Docs export (the markdown escaping converted `[]` to nothing). This confirms the code is NOT copy-paste-deployable as-is, contradicting the comparison's code completeness ★★★★★ rating for R3.

---

## SECTION 3: SEVERITY CALIBRATION REVIEW

### Weaknesses Rated Too Low

1. **R1 Weakness #2 (all-MiniLM-L6-v2 embedding model) — rated SIGNIFICANT, should be CRITICAL.** Combined with the missed OCR weakness, R1's entire ingestion-to-retrieval pipeline is fundamentally broken for scanned PDFs. Even for the subset of PDFs with extractable digital text, a 384-dimension, 256-token-effective model encoding technical automotive content is a severe quality limitation. This directly impacts every downstream component.

2. **R3 Weakness #6 (Dual RTX 4090 requirement) — rated MEDIUM, should be CRITICAL.** If the 70B model cannot fit in GPU memory with 128K context, the entire architecture fails to launch. This isn't a "concern" — it's a binary go/no-go gate. The comparison should demand quantization parameters or alternative model sizing as a mandatory specification.

3. **R3 Weakness #5 (`approx_chars_per_token = 4` heuristic) — rated MEDIUM, should be SIGNIFICANT.** At 100K tokens of RAG context, a systematic token estimation error compounds massively. If the heuristic overestimates capacity by 20% (plausible for technical content with many special characters), the system could attempt to inject ~120K actual tokens into a 128K window, leaving insufficient room for system prompt + generation. This risks inference failure on every turn.

### Weaknesses Rated Too High

1. **R2 Weakness #7 (7 Docker containers) — rated MEDIUM, could be MINOR.** Docker Compose manages container lifecycle automatically. Seven containers with `restart: unless-stopped` is standard production practice. The comparison's framing of "more failure points" overstates the operational complexity for a single-server deployment.

2. **R2 Weakness #9 (Query rewriting adds latency) — rated MINOR, correctly rated.** Confirmed appropriate.

### Missing Context That Changes Ratings

1. **R2 Weakness #5 (AnythingLLM "no passthrough mode"):** The comparison rates this as SIGNIFICANT and says "Research 1 proved this wrong." However, R1's workaround (tunneling context in the user message) is a hack that sends the entire RAG payload as part of the user message through AnythingLLM's chat API. This works but (a) means AnythingLLM's internal memory/logging sees the full RAG payload every turn, (b) makes chat history management fragile, and (c) subjects the payload to AnythingLLM's own processing pipeline. R2's claim that AnythingLLM has "no passthrough mode" is technically accurate — there is no dedicated API for context injection. R1 found a workaround, but R2's characterization isn't wrong. Severity should be MEDIUM, not SIGNIFICANT.

---

## SECTION 4: COMPONENT SELECTION AUDIT

### 1. PDF Parser: Docling (IBM) — from R2+R3

**AGREE.** Both R2 and R3 converge on Docling, which provides layout model classification, TableFormer table extraction, HybridChunker with structural boundaries, and native bounding box metadata. R1's PyMuPDF is unsuitable for scanned PDFs and lacks layout understanding. The selection is well-justified.

### 2. OCR Fallback: Surya — from R2

**AGREE.** Only R2 addressed degraded scan handling. Surya's tunable thresholds are appropriate for 1960s-era scans. Note the GPL-3.0 license concern, which is correctly flagged.

### 3. Embedding Model: BGE-M3 — from R2

**AGREE.** BGE-M3 (1024d, 8192-token context) is substantially superior to both R1's all-MiniLM-L6-v2 (384d, ~256 effective tokens) and R3's bge-small-en-v1.5 (384d, 512 tokens). The dual dense+sparse vector generation from a single model is a significant architectural advantage that simplifies the pipeline. The ~4-point MTEB gap from Voyage AI is well-documented.

**However, the comparison mischaracterizes the source:** R2 also mentions **Qwen3-Embedding-0.6B** (MTEB 70.58, 32K context, Apache 2.0) as a runner-up with higher quality than BGE-M3 on GPU. The comparison does not mention this alternative, which could be relevant given the dual RTX 4090 setup has ample GPU capacity for a 0.6B embedding model.

### 4. Vector Store: Qdrant ≥ v1.15.2 — from R2+R3

**AGREE.** Both R2 and R3 converge on Qdrant. R2 provides the correct version requirement; R3 provides the code. The selection is well-justified.

### 5. LLM Inference: Llama 3.1 70B via vLLM — from R3

**DISAGREE — insufficiently specified and potentially infeasible.**

The comparison says "Must validate GPU memory requirements" as a critical decision point, but then includes this component in the selection table as if validated. The math is problematic:

- Llama 3.1 70B at FP16: ~140GB (does not fit)
- Llama 3.1 70B at INT4 (AWQ/GPTQ): ~35-40GB
- KV cache for 128K context at 70B scale: ~20-40GB additional (varies by implementation)
- Total: potentially 55-80GB minimum
- Available: 2 × 24GB = 48GB VRAM

Even with aggressive INT4 quantization, fitting the model weights AND the KV cache for 128K context into 48GB VRAM is extremely tight or impossible. R3 specifies `--max-model-len 131072` without any quantization flag.

**The comparison should either:** (a) specify a quantization scheme (AWQ 4-bit) and reduced max context length (e.g., 32K-64K), or (b) recommend Llama 3.1 8B with a larger context window as a fallback, or (c) recommend a model that actually fits (e.g., Qwen2.5-32B-Instruct at Q4, which fits in ~20GB and supports 128K context).

The component selection table should flag this as "CONDITIONAL — requires quantization validation" rather than presenting it as decided.

### 6. Context Budget: 100K token RAG budget — from R3

**CONDITIONALLY AGREE.** The math is correct IF the 128K context window is achievable. If quantization forces a reduced context length (e.g., 32K), the budget drops to ~20K tokens — still a massive improvement over R1's 4K but far short of NotebookLM parity.

### 7. Greedy Fill: R3's loop + R2's diversity scoring

**AGREE.** Combining R3's working code with R2's algorithmic improvements (diversity bonus, redundancy penalty, dynamic threshold) is the correct synthesis. Both elements are well-justified.

### 8. Relevance Threshold: 40% dynamic — from R2

**AGREE.** R2's dynamic threshold adapts to varying score distributions. R1's static 0.015 is fragile; R3 has no threshold at all. R2's approach is the best option. Note: the comparison doesn't specify how to implement score-gap detection within R3's codebase.

### 9. Orchestration: Custom Python, NO LangChain — from R2+R3

**AGREE.** R2's rejection of frameworks is well-reasoned (token overhead, dependency risk). R3's code should be the base with LangChain imports replaced by direct HTTP calls.

### 10. Chat Frontend: React with @react-pdf-viewer/highlight — from R3

**PARTIALLY DISAGREE.** R3's React component is the only working frontend code, but it's a single component (`CitationRenderer.tsx`), not a full chat UI. Building an entire production chat interface from scratch is a massive undertaking. The comparison dismisses R2's Open WebUI recommendation as adding "dependency risk," but building a custom React chat app from scratch adds far more development risk and timeline risk.

**Recommendation:** The comparison should present this as a genuine decision point, not a resolved selection. Open WebUI with a custom Pipe function (R2's approach) provides a working chat UI in days; custom React requires weeks/months.

### 11. Citation Rendering: R2's WebP hover + R3's PDF.js click — from R2+R3

**AGREE.** The dual-UX approach (instant pre-rendered hover + deep PDF viewer click-through) is a sound synthesis of both approaches.

### 12. System Prompt: R1's DAG + R3's citation rules — from R1+R3

**AGREE.** R1's full Gus Protocol DAG state machine is essential and is the only complete implementation. R3's V10-specific citation format and lexical collision filtering are necessary additions.

### 13. Deployment: Docker Compose — from R3

**AGREE.** Docker Compose with GPU passthrough is the standard production deployment model. R1's scattered systemd services are harder to manage.

### 14. V9 Inheritance: from R1+R3

**AGREE.** Both preserve V9 infrastructure. Combining for complete coverage is correct.

### 15. Token Counting: Linear regression — from R2

**DISAGREE.** R2's linear regression approach was designed for Claude's tokenizer, which Anthropic doesn't provide locally. For Llama 3.1, the model's own tokenizer is available via `AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3.1-70B-Instruct")` — R3 already imports this. Using the actual tokenizer gives exact counts, not regression estimates. The comparison should recommend using Llama's native tokenizer (already available in the pipeline), not R2's workaround designed for a different model.

### 16. Part Number Matching: Keyword payload indexes — from R2

**AGREE.** R2 correctly identifies that BM25 alone may miss exact part number matches and recommends additional `keyword` payload fields in Qdrant for exact-match filtering. This is a valuable addition.

### 17. Disaster Recovery: Expanded DR script — from R3

**AGREE.** R3's script covers both tracks + Qdrant snapshot before backup. R1's DR was a single cron line.

---

## SECTION 5: BIAS AND BALANCE CHECK

### Systematic Bias Analysis

**The comparison exhibits moderate pro-R2 and pro-R3 bias at the expense of R1.**

Evidence:

1. **R1's NotebookLM alignment score is artificially depressed.** The comparison counts "model quality" as one of R1's two gaps against the 13 NotebookLM findings, but model quality is not one of the 13 findings. R1's actual alignment table shows 12 YES and 1 NO (should be 12/13), not 11/13. This makes R1 appear equal to R2 and R3 when it actually scores highest on architectural alignment.

2. **R1's OCR weakness is underreported.** The comparison rates R1's embedding model as SIGNIFICANT but never identifies the critical fact that PyMuPDF cannot OCR scanned PDFs — which means R1's pipeline produces no output for the core use case. If this were properly flagged, R1's overall viability drops dramatically. But this same severity should also be applied to R3's failure to enable `do_ocr=True` in Docling configuration.

3. **R3's code completeness is overrated.** The comparison gives R3 ★★★★★ for code completeness, but R3's code has: (a) empty list initializations from rendering artifacts (`chunks_data =`, `points =`), (b) markdown escaping artifacts throughout (`\\_`, `\\-`, etc.), (c) a contextualization prompt template with missing content, and (d) a PDF.js worker URL pointing to an external CDN. This code is NOT copy-paste-deployable. A ★★★★☆ rating would be more accurate.

4. **R2's "no code" weakness is appropriately identified.** The comparison correctly rates R2's code completeness as ★☆☆☆☆. This is fair — R2 is a component selection report, not a deployment guide.

### Star Rating Justification

Most star ratings are justified by the detailed analysis, with these exceptions:

- **R1 Research Depth ★★☆☆☆** — Arguably too low. R1 includes detailed analysis of token budgets, PyMuPDF internals, LanceDB+Tantivy architecture, and the division of labor principle. It may not evaluate 50+ tools like R2, but it's not "2 out of 5" quality research. ★★★☆☆ would be more fair.

- **R3 Code Completeness ★★★★★** — Too high given rendering artifacts and missing code (see above). Should be ★★★★☆.

- **R1 Search Quality ★★★☆☆ vs R3 Search Quality ★★★☆☆** — These should not be equal. R1 has a hard relevance threshold (0.015); R3 has no threshold at all. R1 should rate higher on search quality than R3.

### "R3 is the chassis, R2 is the engine, R1 is the soul" Framing

This framing is mentioned in the audit prompt but does not appear verbatim in the comparison document. The comparison's best-of-three selection table does effectively implement this logic: R3 provides the structural codebase (8 of 17 selections include R3 as source), R2 provides the superior component choices (10 of 17 selections include R2 as source), and R1 contributes the system prompt DAG and air-gapped philosophy (4 of 17 selections include R1 as source). This synthesis approach is reasonable and well-justified by the evidence, though R1's unique contributions (VMDK ingestion, TOCTOU locking, complete DAG) are undervalued.

### Railroading Toward a Predetermined Conclusion

The comparison does not railroad toward a single research result. The synthesis genuinely draws from all three. However, the comparison does railroad toward a specific architectural decision (Llama 3.1 70B via vLLM) that may be infeasible. This is presented as resolved when it should be the single biggest open question.

---

## SECTION 6: CRITICAL GAPS

### Missing Evaluation Dimensions

1. **OCR quality testing methodology.** None of the three research results — and the comparison — address how to validate OCR quality across the 500+ PDFs. A systematic approach (sample 50 PDFs, manually verify OCR output, measure character error rate) should be recommended.

2. **Latency budget.** The comparison never discusses end-to-end latency. A mechanic standing at a workbench needs sub-5-second response times. Llama 3.1 70B generating text at 128K context length on quantized dual GPUs may produce 2-5 tokens/second — meaning a 500-token response takes 100-250 seconds. This could be a dealbreaker. NotebookLM uses Gemini on Google's TPU infrastructure with far faster inference.

3. **Embedding latency at query time.** BGE-M3 at 568M parameters on CPU takes "20-30ms per query" (R2). This is acceptable. But combined with Qdrant search time, vLLM inference time, and PDF rendering time, the total latency needs to be profiled.

4. **Disk storage requirements.** 500 PDFs × 200 pages × pre-rendered WebP at 150 DPI ≈ 500MB-5GB of page images. Plus original PDFs, parsed JSON, Qdrant volumes, model weights (~40GB for 70B quantized, ~2GB for BGE-M3). Total storage requirements should be calculated.

5. **Concurrent user support.** The V9/V10 system is designed for a single mechanic, but the comparison doesn't explicitly confirm this constraint or discuss what happens if multiple browser tabs are open.

### Unasked Questions

1. **Which Llama 3.1 quantization (AWQ vs GPTQ vs GGUF) is recommended, and at what bit depth?** This determines whether the system is feasible.

2. **What is the fallback if 70B doesn't fit?** Should the architecture accommodate graceful degradation to a smaller model (e.g., 8B with 128K context, sacrificing quality for capacity)?

3. **How will the React frontend be served?** R3 provides a component but no build toolchain, no development server, no production build configuration. Is this a Next.js app? Vite? Create React App?

4. **How does Docling handle the VMDK/OVA ingestion pipeline?** R1 preserves this V9 capability; R3 does not. If FSMs are delivered in VM images, R3's Docling pipeline cannot ingest them without R1's VMDK extraction logic.

### Risks Not Flagged

1. **Single point of failure: vLLM process.** If the vLLM inference server crashes or OOMs (likely with the aggressive memory configuration), the entire system is down. No fallback inference path is specified.

2. **Docling processing time for 500+ PDFs.** R2 estimates 86 hours on CPU or 14 hours on GPU. This is a multi-day blocking operation. The comparison doesn't discuss incremental ingestion (process new PDFs as they arrive) vs batch (process all at once).

3. **BGE-M3 via TEI requires separate container.** The comparison selects BGE-M3 via HuggingFace TEI (from R2) but R3's code uses FastEmbed locally. This is an integration gap — swapping from FastEmbed to TEI requires changing the indexer and retriever code to make HTTP calls to the TEI container instead of local model loading.

### Integration Concerns Between Components

1. **Docling (R2/R3) + VMDK extraction (R1).** These are from different research results and have never been tested together. R1's extraction daemon outputs JSON; R3's Docling parser expects raw PDFs. The integration path: R1's VMDK extractor → saves PDF to directory → R3's Docling parser watches directory → processes PDF. This should work but needs explicit documentation.

2. **BGE-M3 via TEI (R2) + Qdrant collection config (R3).** R3's code creates a Qdrant collection with 384-dimension dense vectors (matching bge-small). Switching to BGE-M3 requires changing the vector dimension to 1024 and potentially changing the sparse vector generation approach (BGE-M3 generates its own sparse vectors vs R3's FastEmbed BM25 model).

3. **Open WebUI Pipe (R2) vs Custom React (R3).** The comparison selects R3's React approach but notes R2's Open WebUI as "worth investigating." These are mutually exclusive architectural paths. The V10 document needs to commit to one.

4. **R2's query rewriting + R3's query contextualization.** The comparison selects both in different component rows without addressing that they overlap. Are both needed? If using Llama for contextualization, is Claude Haiku (unavailable air-gapped) also needed for query rewriting?

---

## SECTION 7: FINAL VERDICT

### Scores

| Metric | Score | Justification |
|:-------|:-----:|:-------------|
| **Accuracy** | **7/10** | Most alignment scores are correct; key errors include R1's inflated "No query expansion" YES, the phantom "model quality" finding, R3's overrated code completeness, and the failure to identify R1's fatal OCR gap as CRITICAL. |
| **Completeness** | **6/10** | Major omissions: no latency analysis, no memory math for 70B+128K, no OCR quality testing methodology, no discussion of graceful degradation, no storage requirements. VMDK pipeline integration not addressed. |
| **Bias** | **7/10** | Moderate pro-R2/R3 bias. R1's alignment score artificially depressed; R3's code completeness overrated. The synthesis approach (draw from all three) is fundamentally sound, but R1's unique contributions are undervalued. |
| **Actionability** | **6/10** | The component selection table is useful but presents the Llama 70B inference decision as resolved when it's the single biggest open risk. Several integration paths between components from different research results are unspecified. Token counting recommendation is wrong (should use Llama's native tokenizer). Frontend build toolchain not addressed. |

### Top 3 Corrections Before Using This Comparison to Build V10

1. **Resolve the GPU memory feasibility question FIRST.** The entire architecture hinges on whether Llama 3.1 70B with 128K context fits on dual RTX 4090s. Run `vllm serve meta-llama/Meta-Llama-3.1-70B-Instruct --tensor-parallel-size 2 --max-model-len 131072 --quantization awq` and see if it boots. If it doesn't, the V10 architecture needs a fundamentally different LLM strategy (smaller model, reduced context, or hybrid local+API approach). Define the fallback model and context budget now, not after building the rest of the pipeline.

2. **Elevate R1's OCR gap and R3's missing `do_ocr=True` to CRITICAL.** The V10 document must explicitly specify Docling's OCR configuration (`do_ocr=True`, EasyOCR backend, 300 DPI) and the Surya fallback pipeline. Without this, the parsing pipeline produces empty output for scanned PDFs. This should be the second item validated after GPU memory.

3. **Replace the token counting recommendation.** Use Llama 3.1's native `AutoTokenizer` (already imported in R3's code) for exact token counts. Do not use R2's linear regression approach, which was designed for Claude's unavailable tokenizer. For the greedy fill loop, call `tokenizer.encode()` on each excerpt and count the resulting token list length. This gives zero estimation error.

---

*End of audit report.*
