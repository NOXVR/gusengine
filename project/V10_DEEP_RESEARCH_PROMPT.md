# V10 DEEP RESEARCH PROMPT — AUTOMOTIVE DIAGNOSTIC RAG PLATFORM ARCHITECTURE

## INSTRUCTIONS TO THE RESEARCH AI

You are being given a complex systems engineering task. You will produce a complete, production-grade architectural specification for a self-hosted automotive diagnostic RAG (Retrieval Augmented Generation) platform called "GusEngine."

### CRITICAL CONTEXT WARNINGS

**1. ATTACHED DOCUMENTS ARE PRIORITY.**
I am attaching the following documents. These are NOT supplementary — they are the ground truth for this project. You MUST read them completely before generating any output:

- **`ARCHITECTURE_V9_FROZEN.md`** — The previous (V9) architecture specification. This is the complete, hostile-audited blueprint for the current system. It contains validated infrastructure (Phases 1-3), system prompt logic (Phase 8), agent skills (Phase 9), and operational tooling (Phases 10-12) that MUST be preserved in V10. It also contains the RAG pipeline (Phases 4-5, 7) that is being REPLACED. Read this entire document.
- **`NOTEBOOKLM_INTEL.md`** — Confirmed findings from direct interrogation of Google NotebookLM's architecture. Every finding in this document was confirmed by the platform itself and/or by direct observation. This is empirical data, not speculation.
- **`PROJECT_DNA_V9.md`** — The project DNA document containing ground-truth specifications, variable values, file paths, and configuration.
- **`V9_CHANGELOG.md`** — Complete changelog of all V9 modifications, including the V9.2 watermark deprecation and V9.3 RAG pipeline deprecation.

**2. PLATFORM vs CHAT LAYER — DO NOT CONFUSE THESE.**
When discussing RAG systems like NotebookLM, there are TWO distinct layers:
- **The PLATFORM** — the full system including ingestion, storage, OCR, metadata mapping, retrieval, frontend rendering, and citation display.
- **The LLM CHAT LAYER** — the text-generation model that receives pre-compiled excerpts and produces responses.

The LLM layer cannot see images, does not know document filenames, and outputs only plain text citation indices `[N]`. ALL rich functionality (image rendering, section titles, document names in citations, PDF page display) is provided by the PLATFORM, not the LLM.

**A previous deep research attempt incorrectly stated that NotebookLM handles images via "multimodal verbalization using Gemini vision" to generate text descriptions. This is DEMONSTRABLY FALSE.** Direct observation confirms that NotebookLM stores the original untouched PDF and renders actual PDF page images in citation hovers via a spatial metadata map with bounding box coordinates. The LLM never sees the images. Do NOT repeat this error.

---

## WHAT WE ARE BUILDING

### The GusEngine Platform

GusEngine is a **self-hosted, air-gapped automotive diagnostic RAG platform** designed for professional Mercedes-Benz mechanics working on vintage vehicles (1960s-1980s). The system ingests 500+ Factory Service Manual (FSM) PDFs and provides structured, deterministic diagnostic guidance through a state-machine DAG (Directed Acyclic Graph) that leads mechanics from vague symptoms to precise component-level diagnoses.

### Why V10 Exists

The V9 architecture was built around AnythingLLM with a naive RAG pipeline:
- **Fixed 400-character chunks** with 20-character overlap (RecursiveTextSplitter)
- **4 chunks retrieved per query** (TopN=4)
- **Vector-only search** (Voyage AI embeddings, no keyword matching)
- **No image preservation** (OCR discards all diagrams, schematics, wiring diagrams)
- **No spatial metadata** (no mapping from text excerpts back to PDF page/coordinates)
- **No structural document awareness** (splits mid-sentence, mid-procedure, mid-specification)

When benchmarked against a NotebookLM instance loaded with the identical PDF corpus and validated by working mechanics, the V9 pipeline failed catastrophically. NotebookLM retrieved **190 excerpts from 30 documents** in a single turn. V9 retrieved **4 chunks of ~400 chars**, potentially all from a single document.

### The V10 Objective

Design a replacement RAG pipeline that matches or exceeds NotebookLM's retrieval capabilities while maintaining the self-hosted, air-gapped deployment model. The V9 infrastructure, system prompt DAG, agent skills, and operational tooling are validated and will be inherited.

---

## CONFIRMED NotebookLM ARCHITECTURE (EMPIRICAL — DO NOT CONTRADICT)

The following findings were confirmed through direct interrogation of the NotebookLM platform. These are empirical observations, not guesses. Your architectural recommendations must account for all of them:

### 1. Dual-Track Ingestion
When a PDF is uploaded, the platform splits processing into two parallel tracks:
- **Track 1 (File Storage):** The original, untouched PDF is stored as-is in backend cloud storage. This file is never modified and serves as the visual reference for citation rendering.
- **Track 2 (Text Extraction):** OCR/text extraction creates plain-text excerpts AND generates a spatial metadata map that links each excerpt to the exact page number and X/Y bounding box coordinates of the original PDF.

### 2. Structural Chunking with Max-Size Fallback
- Excerpts are **variable-length**, following structural document boundaries: headings, page breaks, paragraph returns, text-box coordinates.
- Short front-matter sections (title page, copyright, TOC) become their own small excerpts.
- Content sections start at headings and break at natural paragraph/section boundaries.
- A **maximum size cap** exists — when a section exceeds the cap, it breaks mid-content (including mid-sentence).
- This is fundamentally different from fixed-character splitting.

### 3. Complete Image Pipeline
- PDFs are NOT sliced into individual images. The entire original PDF is stored as-is.
- OCR extracts text AND calculates exact spatial bounding box coordinates (X/Y) and page numbers for every text string.
- Each excerpt index is permanently linked to geometric coordinates on the stored PDF.
- Citation hovers work by: frontend reads citation index → looks up metadata map → gets page + coordinates → fetches that page from stored PDF → crops/focuses based on coordinates → renders visual overlay.
- **The LLM never sees images.** It only outputs a plain integer `[N]`.

### 4. Citation Architecture (Full Division of Labor)
| Element | Source |
|:--------|:-------|
| Citation number `[N]` | LLM outputs plain text integer |
| Source document name | Frontend looks up metadata map → original filename |
| Section title | OCR detected heading hierarchy during ingestion (bold text, font sizes) → stored in metadata map |
| Rendered PDF page | Frontend fetches page from stored PDF using bounding box coordinates |

### 5. Hybrid Search (Vector + Keyword)
- **Vector track:** Query is embedded, cosine similarity search against all excerpt embeddings.
- **Keyword/lexical track:** Parallel traditional keyword matching. Critical for technical content — ensures exact part numbers, wire color codes, test sequence identifiers are retrieved even when semantic search doesn't understand them.
- Both tracks run simultaneously against the **entire unified corpus** (all 500+ documents).
- No query expansion or rephrasing — exact user words are searched.

### 6. Dynamic Context Injection
- **190 excerpts from 30 documents** were loaded for a single diagnostic query.
- There is NO fixed TopN. The number of excerpts varies dynamically based on chunk length, capped only by the LLM's context window token limit.
- There is NO limit on the number of source documents represented in a single payload.
- A **hard relevance threshold** discards below-confidence excerpts (no bottom-scraping).

### 7. Turn-Based Fresh Retrieval
- Each user turn triggers a **fresh retrieval pass** against the full corpus.
- The previous turn's excerpts are **flushed** from context.
- The new user input is **contextualized with conversation history** before searching (so the system "remembers" the diagnostic context).
- This enables progressive refinement: broad symptoms → broad charts (turn 1), specific selection → specific procedures and part numbers (turn 2).

### 8. No Mid-Generation Retrieval
- The LLM cannot request additional excerpts during generation. The entire payload is pre-compiled and static for each turn.
- All semantic reasoning (connecting symptoms to components, following diagnostic logic) is performed by the LLM after receiving the excerpt payload.

### 9. Known Weakness: Lexical Collisions
- Keyword matching can cause false positives. Example: "vacuum" query for engine intake also retrieves door lock vacuum switch manuals.
- The LLM must filter these via system prompt instructions (e.g., the Gus Protocol's mandate to cross-reference all data against the diagnostic context).

---

## WHAT THE V10 ARCHITECTURE DOCUMENT MUST CONTAIN

### Structure Requirements
The V10 architecture must be a **complete, standalone, deployable specification** — not a diff or patch against V9. It must contain every command, every configuration value, every code block needed to build the system from bare metal.

### Inheritance from V9
The following V9 components are validated and must be carried forward **verbatim or with minimal, documented modifications**:

| V9 Component | V10 Action | Notes |
|:-------------|:-----------|:------|
| Phases 1-3 (bare metal, Docker, API key binding) | INHERIT VERBATIM | Infrastructure is pipeline-independent |
| Phase 6 (tribal knowledge / MASTER_LEDGER) | INHERIT VERBATIM | Knowledge subsystem is pipeline-independent |
| Phase 8 (system prompt / DAG state machine) | INHERIT + UPDATE CITATIONS | State machine logic is sound; citation format needs updating for new metadata-driven citations |
| Phase 9 (agent skills - VIN Lookup, Purchase Router, Draft Tribal Knowledge) | INHERIT VERBATIM | Skills don't interact with RAG pipeline |
| Phase 10 (disaster recovery) | INHERIT + EXTEND | Add backup for new metadata store |
| Phases 11-12 (frontend, verification) | INHERIT + EXTEND | Frontend needs citation hover rendering layer |
| Appendix A (skill definitions) | INHERIT VERBATIM | |
| Appendix B (frontend reference) | INHERIT + EXTEND | Add citation hover rendering code |
| All hostile audit fixes (V9.1) | MUST BE PRESERVED | These fixes are validated and must not be lost |

### New V10 Components Required
The following must be designed from scratch, informed by the NotebookLM findings:

**1. Structural Document Parser (replaces Phase 4 chunk_pdf)**
- Must segment PDFs by headings, sections, figures, logical boundaries
- Must have a max-size fallback for oversized sections
- Must preserve figure callouts and table structure inline
- Must generate the spatial metadata map (excerpt → page + bounding box coordinates)
- Must detect heading hierarchy via font size/bold for section title metadata
- Recommend specific open-source tools and provide implementation code

**2. Dual-Track Storage (replaces Phase 5 sync_ingest.py)**
- Track 1: Store original untouched PDFs for citation rendering
- Track 2: Store structural excerpts with metadata in searchable index
- Must handle 500+ PDFs with corpus-wide excerpt indexing

**3. Hybrid Search Engine (replaces Phase 7 RAG mathematics)**
- Vector search (cosine similarity) + parallel keyword/lexical search
- Dynamic excerpt injection (token-capped, not fixed TopN)
- Hard relevance threshold with noise filtering
- Full-corpus simultaneous search
- Recommend specific components (embedding model, vector DB, keyword engine)

**4. Citation Metadata Layer (replaces Phase 8 citation rules)**
- Metadata map linking excerpt index → source filename + page + bounding box coordinates + section title
- Frontend citation rendering: hover → fetch PDF page → crop to coordinates → display overlay
- LLM outputs only plain `[N]` indices

**5. Turn-Based Retrieval with Context (new)**
- Fresh retrieval per turn
- Query contextualization with conversation history
- Progressive refinement support

### Self-Hosted Constraint
The system MUST remain self-hostable on a single Linux server (Ubuntu 24.04 LTS). It cannot depend on Google Cloud, AWS, or any external API for core functionality. External APIs are acceptable only for optional features (VIN lookup via public NHTSA API). The deployment target is described in the attached PROJECT_DNA document.

### Code Completeness
Every script, configuration file, systemd unit, Docker command, and cron job must be provided as complete, copy-pasteable code blocks — not pseudocode, not "implement this." The V9 document set this standard and V10 must match or exceed it.

---

## OUTPUT FORMAT

Produce a single, comprehensive architecture document structured as numbered Phases (matching the V9 convention where possible for traceability). Include:

1. **Preface** with V9→V10 migration context and what changed
2. **Inherited phases** (Phases 1-3, 6, 9) — carried forward with explicit V9 line references
3. **Replaced phases** (new Phases 4-5, 7) — complete new implementations with code
4. **Updated phases** (Phases 8, 10-12) — inherited with documented modifications
5. **V10 Appendices** — inherited + extended
6. **Token budget** — calculated for the new dynamic injection model
7. **Verification checklist** — updated for V10 pipeline testing

Do not produce a summary, overview, or high-level description. Produce the actual architecture specification.
