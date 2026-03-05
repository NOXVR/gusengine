# NotebookLM Platform Intelligence — Confirmed Findings

**Source:** Direct interrogation of NotebookLM instance (identical 514-PDF FSM corpus)
**Date:** 2026-02-24
**Purpose:** Reverse-engineer NotebookLM's RAG architecture to inform V10 pipeline design

---

## CONFIRMED FINDINGS (From NotebookLM Self-Report + Direct Observation)

### 1. Dual-Track Ingestion Pipeline

When a PDF is uploaded, the platform splits processing into two parallel tracks:

| Track | Function | Storage |
|:------|:---------|:--------|
| **File Storage** | Original untouched PDF saved as-is | Backend cloud storage |
| **Text Extraction** | OCR/text extraction creates plain-text excerpts + position metadata map | Indexed for LLM retrieval |

**Key Detail:** The metadata map links each text excerpt to the **exact page number and spatial coordinates** of the original PDF. This is how citation hovers work.

### 2. Variable-Length Structural Chunking (NOT Fixed-Size)

- Excerpts are **NOT fixed-length** (confirmed by NotebookLM)
- Some excerpts are a few words, others are hundreds of words
- The parsing engine follows **structural document boundaries**: page breaks, paragraph returns, text-box coordinates
- This is fundamentally different from RecursiveTextSplitter (fixed 400 chars, 20 overlap)

**NotebookLM quote:** *"The excerpts are absolutely not fixed-length. Some excerpts are just a few words or a single fragmented OCR string, while others are dense blocks of text containing hundreds of words. This indicates that the backend parsing engine attempts to follow structural document boundaries."*

### 3. Citation Rendering Architecture (CONFIRMED — Full Division of Labor)

The LLM and UI operate as completely separate layers with a clear division:

**What the LLM outputs:** A raw plain-text string — opening bracket, integer, closing bracket (e.g., `[1]`). Nothing else. No metadata, no hidden code, no structured reference objects. The integer corresponds to the sequential excerpt index from the retrieval payload.

**What the Frontend adds (ALL of the following):**

| Hover Element | Frontend Source |
|:-------------|:---------------|
| **Source document name** | Metadata map links excerpt index → original filename in cloud storage |
| **Section title** | During OCR, platform detects document hierarchy via **bold text and larger font sizes**, stores as heading metadata. Frontend retrieves scraped title for hovercard. |
| **Rendered PDF page** | Metadata map provides page number + X/Y spatial coordinates. Frontend fetches page from untouched master PDF in cloud storage, crops/focuses based on coordinates. |

**NotebookLM quote:** *"I emit a raw, plain-text string consisting of an opening bracket, an integer, and a closing bracket. The only information I encode is the index number. I am completely blind to the file's original name, its visual structure, or any user-facing titles."*

### 4. Complete Image Pipeline (CONFIRMED)

The platform processes images through a 4-step pipeline:

**Step 1 — Original File Storage (Image Repository):**
- PDFs are NOT sliced into individual images (JPEGs, PNGs, etc.)
- The entire untouched original PDF is saved as-is in backend cloud storage
- This intact file acts as the master visual repository

**Step 2 — Text Extraction + Spatial Mapping (The Link):**
- OCR pipeline extracts text AND generates a hidden **spatial metadata map**
- The map calculates **exact bounding box coordinates (X/Y)** and **page number** for every extracted text string
- Each excerpt index (e.g., Excerpt 15) is permanently linked to geometric coordinates on the stored PDF
- This is the critical architectural component: **text ↔ spatial position linking**

**Step 3 — Frontend Citation Interception:**
- LLM outputs plain text citation markers
- Frontend UI intercepts markers and runs a background process listening for mouse hover events

**Step 4 — Hover Resolution and Rendering:**
1. Frontend reads the citation index number
2. Cross-references against the spatial metadata map from Step 2
3. Metadata map returns exact page number + X/Y coordinates
4. Frontend requests that specific page from the untouched master PDF in cloud storage
5. UI receives the page, **crops or focuses the view based on coordinate data**
6. Renders the visual overlay on screen

**Key Insight:** *"The platform knows exactly which diagram to show you because the OCR engine extracted text that was physically printed over or next to the illustration in your original file. When the text is cited, the platform simply summons the visual real estate from the original file where those words physically reside."*

**LLM is blind to images** — it does not see, index, or search visual content. Images are served entirely by the platform display layer.

**Correction to Deep Research:** The claim of "multimodal verbalization using Gemini vision" generating text descriptions is **demonstrably wrong**. The platform renders original PDF images via coordinate-based lookup, not AI-generated descriptions.

### 5. Excerpt Count Scales With Document Size

- The K-Jetronic manual produces "hundreds" of excerpts
- Short documents may produce only 1-2 excerpts
- No artificial limit on excerpts per document observed

### 6. Multi-Document Retrieval (CONFIRMED — Single Pass)

For the hot-start test query, NotebookLM retrieved from 3+ source documents simultaneously:
1. C.I.S. Problem Diagnosis Chart — matched "hard starting" and "cranks"
2. Static Pressure Test documentation — matched pressure loss and starting failures
3. K-Jetronic Technical Instruction manual — matched "vapor lock" and fuel system mechanics

**Mechanism:** All three were retrieved in a **single hybrid search pass**. The platform does NOT perform multiple retrieval rounds or recursive lookups. Cross-document retrieval is **emergent** — it happens naturally because a single query contains concepts distributed across multiple manuals, and the hybrid search matches them all simultaneously.

**Critical limitation confirmed:** The LLM **cannot request additional excerpts mid-generation**. There is no recursive retrieval loop or active fetch mechanism. The entire payload is pre-compiled and injected BEFORE generation begins. The context is a **static, frozen snapshot**.

**Implication for V10:** Multi-document retrieval does NOT require a special retrieval chaining system. It requires: (1) hybrid search (vector + keyword), (2) enough dynamic TopN headroom, and (3) structural chunking that preserves complete document sections so each retrieved excerpt carries meaningful context.

### 8. Retrieval Pipeline Architecture (CONFIRMED)

The platform executes a 5-stage retrieval pipeline BEFORE the LLM sees any text:

```
User Query → Embedding Model → Vector Search ─┐
                                                ├─ Rank → Threshold → Top-K → Context Injection → LLM
User Query → Lexical/Keyword Search ───────────┘
```

**Stage 1 — Vector Embedding:** User query is converted to a high-dimensional vector via embedding model. Cosine similarity search runs against the pre-built vector database of all excerpt embeddings.

**Stage 2 — Keyword Matching (HYBRID):** A parallel lexical search engine performs traditional keyword matching. This is **critical for technical corpuses** — it ensures exact strings like part numbers, wire color codes (`1.5 bk/vi`), and test sequences (`Test 4`) are forcefully retrieved even when the semantic model doesn't understand their context.

**Stage 3 — Simultaneous Full-Corpus Search:** The retrieval searches the **entire unified database** of ALL uploaded sources simultaneously. No pre-filtering. Every excerpt across 500+ sources competes mathematically for relevance. Exception: user can manually toggle source files on/off in the UI, applying a hard pre-filter.

**Stage 4 — Relevance Threshold + Top-K Cutoff:** Combined semantic+keyword relevance scores are ranked. A **hard relevance threshold** discards low-confidence matches (prevents noise). A top-K cutoff limits the final set.

**Stage 5 — Dynamic Context Injection:** The final highest-ranked excerpts are compiled into a single payload. The **number of excerpts is NOT fixed** — it varies dynamically based on each excerpt's length, strictly capped by the LLM's context window token limit.

**V9 vs NotebookLM comparison:**

| Parameter | V9 AnythingLLM | NotebookLM |
|:----------|:---------------|:-----------|
| Search type | Vector only | Hybrid (vector + keyword) |
| TopN | Fixed at 4 | Dynamic, token-limited |
| Relevance threshold | Default/unknown | Hard threshold, noise filtered |
| Keyword matching | None | Parallel lexical search |
| Corpus scope | All sources | All sources (identical) |

### 7. Excerpt Boundary Analysis (K-Jetronic Manual — First 10)

Direct inspection of how the platform segmented `k-jetronic-manual.pdf`:

| Excerpt | Index | Starts With | Ends With | Split Type |
|:--------|:------|:------------|:----------|:-----------|
| 1 | 271 | `# Gasoline Fuel-Injection System K-Jetronic` | `...Berthold Gauder, Leinfelden-Echterdingen.` | **Heading / title page** |
| 2 | 272 | `Translation: Peter Girling.` | `...We reserve the right to make changes at any time.` | **Section (copyright)** |
| 3 | 273 | `Printed in Germany.` | `...Workshop testing techniques 38` | **Section (TOC)** |
| 4 | 274 | `# K-Jetronic` | `...particularly important with regard to maintenance and repair.` | **Chapter heading** |
| 5 | 275 | `This manual will describe...` | `...The heat released in the` | **⚠️ MID-SENTENCE break** |
| 6 | 276 | `Cylinder charge in the spark-ignition engine` | `...12 Exhaust valve, α Throttle-valve angle. U M M 05` | **Section + figure callouts** |
| 7 | 277 | `Mechanical injection systems` | `...to specific engine operating conditions.` | **Topic heading** |
| 8 | 278 | `Electronic injection systems` | `...Motronic as an integrated engine-manage-ment system.` | **Topic heading** |
| 9 | 279 | `Overview 11 Throttle-body fuel injection (TBI)` | `...electronic` | **Section heading** |
| 10 | 280 | `Bosch gasoline fuel injection from the year 1954` | `...Fuel supply, – Air-flow measurement and – Fuel metering.` | **Historical section** |

**Key observations:**
1. **Hybrid chunking strategy:** Structural-priority (headings, sections, paragraphs) WITH a maximum size fallback. Excerpt 5 breaks mid-sentence, proving a size cap exists.
2. **Corpus-wide indexing:** Indices 271-280 for the K-Jetronic manual means excerpts 1-270 belong to other documents. All 514 PDFs are in a single flat excerpt index.
3. **Figure callouts preserved inline:** Excerpt 6 includes `11 Intake valve, 12 Exhaust valve` — figure labels are extracted into the text, maintaining the spatial relationship.
4. **Variable length confirmed:** Excerpts 1-3 (front matter) are very short; Excerpts 4-5 (chapter content) are much longer.

---

## INVESTIGATION CHECKLIST (ALL CONFIRMED)

The following questions were queried via direct NotebookLM interrogation:

- [x] Exact retrieval mechanism — **CONFIRMED: Hybrid (vector cosine similarity + keyword/lexical)**
- [x] Number of excerpts injected per query — **CONFIRMED: 190 excerpts from 30 docs in single response (dynamic, token-limited)**
- [x] Whether query expansion occurs before retrieval — **CONFIRMED: NO expansion. Platform searches exact user words via both lexical and vector tracks. No rephrasing, no appended terms. All semantic reasoning happens in the LLM AFTER retrieval.**
- [x] Whether new turns trigger fresh retrieval or reuse static context — **CONFIRMED: Fresh retrieval every turn. Context window is FLUSHED between turns. New user input is contextualized with conversation history before searching (query + history = contextualized search). Enables progressive refinement: broad symptoms → broad charts (turn 1), specific selection → specific procedures (turn 2).**
- [x] Exact excerpt boundaries for a specific document — **CONFIRMED: See Finding 7**
- [x] Failure handling when no relevant excerpts found — **CONFIRMED: Hard threshold discards all below-confidence excerpts. Zero matches = blank context payload (no error flag). LLM self-detects empty context and reports "sources do not contain relevant information." Known weakness: lexical collisions inject false-positive excerpts (e.g., "vacuum" matches door lock manual when asking about engine vacuum). LLM must filter these via system prompt.**
- [x] Context window size and utilization — **CONFIRMED: 190 excerpts, 30 docs, token-capped only**
- [x] Whether multi-document retrieval is single-pass or multi-pass — **CONFIRMED: Single pass, all sources simultaneously**

---

## DEEP RESEARCH CORRECTIONS

The deep research output contained the following claims that contradict direct observation:

| Deep Research Claim | Observed Reality | Verdict |
|:-------------------|:-----------------|:--------|
| Images handled via "multimodal verbalization" generating text descriptions | Original PDF images rendered in citation hovers — actual images, not descriptions | **INCORRECT** |
| `DocumentLayout` proto for tree-based hierarchy | Plausible for text structure but unconfirmed | **UNVERIFIED** |
| TableFormer-based table extraction | Plausible but unconfirmed | **UNVERIFIED** |
| Headings detected as structural nodes | Consistent with variable-length structural chunking finding | **PLAUSIBLE** |
