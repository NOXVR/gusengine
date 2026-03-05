# V10 Deep Research Comparison Audit — Triad Prompt

## COPY THIS ENTIRE DOCUMENT AS THE PROMPT TO THREE SEPARATE DEEP RESEARCH AGENTS

Upload the following 5 files with this prompt:
1. `NOTEBOOKLM_INTEL.md` — Ground truth: confirmed findings from interrogating Google's NotebookLM
2. `DEEP_RESEARCH_1.md` — Research Result 1 (local/air-gapped architecture)
3. `DEEP_RESEARCH_2.md` — Research Result 2 (component selection report)
4. `DEEP_RESEARCH_3.md` — Research Result 3 (full V10 architectural specification)
5. `DEEP_RESEARCH_COMPARISON.md` — The comparison analysis being audited

---

## CONTEXT: WHAT THIS PROJECT IS AND WHAT LED TO THIS REQUEST

### The Project

GusEngine is a self-hosted, air-gapped automotive diagnostic RAG (Retrieval Augmented Generation) platform designed for a single mechanic specializing in vintage Mercedes-Benz (1960s-1990s). The system ingests ~500 factory service manuals (FSMs) as PDFs — many are degraded 1960s-era scans — and provides a conversational diagnostic assistant ("Gus") that references these manuals with source citations.

The V9 architecture was a working prototype deployed on Ubuntu 24.04 LTS with dual RTX 4090 GPUs, using AnythingLLM as the chat UI, Ollama for local LLM inference, and a naive RAG pipeline (RecursiveTextSplitter at 400 characters, Voyage AI embeddings, cosine similarity, fixed Top-4 retrieval).

### What Triggered the V10 Redesign

The V9 RAG pipeline was tested against Google's NotebookLM by loading an identical 514-PDF corpus into both systems. NotebookLM demonstrated dramatically superior retrieval quality. A systematic interrogation of NotebookLM (documented in `NOTEBOOKLM_INTEL.md`) reverse-engineered its RAG architecture and revealed fundamental flaws in V9's approach:

- V9 used **fixed-size character splitting** (400 chars, 20 overlap). NotebookLM uses **variable-length structural chunking** following document hierarchy.
- V9 retrieved a **fixed Top-4 chunks**. NotebookLM **dynamically injects ~190 excerpts** until a token budget is exhausted.
- V9 had **no spatial metadata**. NotebookLM preserves **bounding box coordinates** for every excerpt, enabling pixel-accurate citation rendering.
- V9 used **vector-only search**. NotebookLM runs **hybrid vector + BM25 keyword search** simultaneously with RRF fusion.

This led to the V9 RAG pipeline being deprecated and a V10 redesign effort launched. The V10 objective: **match or exceed NotebookLM's retrieval capabilities while remaining fully self-hosted and air-gapped**.

### The Three Research Results

Three separate deep research AI agents were given an identical prompt to design the V10 architecture. Each returned a different result:

- **Research 1** (720 lines): Air-gapped, fully local. Ollama + Llama 3.1 8B, PyMuPDF parsing, LanceDB + Tantivy hybrid search, FastAPI gateway. Complete deployable code but only 4,000-token RAG budget (vs NotebookLM's ~190 excerpts).

- **Research 2** (209 lines): Component selection report. Docling (IBM) for parsing, Qdrant for hybrid search, BGE-M3 embeddings, Claude Sonnet API for inference. Superior component choices and 200K context window, but **NOT air-gapped** (requires Claude API) and **no deployable code**.

- **Research 3** (829 lines): Full V10 architectural specification. Docling, Qdrant, bge-small embeddings, Llama 3.1 70B via vLLM with tensor parallelism, React frontend. Complete code for all components. Air-gapped with 128K context window.

### What Was Done

An AI assistant (the entity being audited) read all three research results and the NotebookLM intel document, then produced `DEEP_RESEARCH_COMPARISON.md` — a three-way comparative analysis with:
- Per-result strengths/weaknesses/factual errors
- Per-result alignment scoring against 13 confirmed NotebookLM architectural findings
- A star-rating scoring summary across 12 dimensions
- A "Best-of-Three" component selection table (17 components with source attribution and rationale)
- Five critical decision points for the final V10 architecture

### Why This Audit Exists

**The comparison analysis was produced by a single AI agent.** Before using this analysis to drive the final V10 architecture document, it must be independently verified. This prompt asks you to audit that comparison for:
- Missed strengths or weaknesses in any of the three research results
- Incorrect NotebookLM alignment scores
- Flawed reasoning in the component selection
- Bias toward or against any particular research result
- Errors of omission (important findings in the research docs not captured in the comparison)
- Logical inconsistencies between the analysis sections

---

## YOUR TASK

You are an independent auditor. Your job is to **cross-examine the comparison analysis** (`DEEP_RESEARCH_COMPARISON.md`) against the four source documents (`NOTEBOOKLM_INTEL.md`, `DEEP_RESEARCH_1.md`, `DEEP_RESEARCH_2.md`, `DEEP_RESEARCH_3.md`).

### Output Structure

Produce your audit report in the following exact structure:

---

### SECTION 1: NOTEBOOKLM ALIGNMENT VERIFICATION

For each of the 13 NotebookLM findings listed in `NOTEBOOKLM_INTEL.md`, verify whether the comparison document scored each research result correctly.

For each finding, state:
- **The NotebookLM finding** (from the intel doc)
- **R1 score in comparison** → **Your assessment** (AGREE / DISAGREE + reason)
- **R2 score in comparison** → **Your assessment** (AGREE / DISAGREE + reason)
- **R3 score in comparison** → **Your assessment** (AGREE / DISAGREE + reason)

If you find a scoring error, explain what the correct score should be and why.

### SECTION 2: MISSED FINDINGS AUDIT

Read each research result **in full**, independently of the comparison document. For each result, identify any strengths, weaknesses, factual errors, or design choices that the comparison document failed to capture.

Format:
- **Research [N] — Missed Strengths:** (list, or "None found")
- **Research [N] — Missed Weaknesses:** (list, or "None found")
- **Research [N] — Missed Factual Errors:** (list, or "None found")

### SECTION 3: SEVERITY CALIBRATION REVIEW

The comparison assigns severity ratings (CRITICAL, SIGNIFICANT, MEDIUM, MINOR) to each weakness. Review these assignments:
- Are any weaknesses rated too high? (Explain why)
- Are any weaknesses rated too low? (Explain why)
- Are any severity assignments missing context that changes the rating?

### SECTION 4: COMPONENT SELECTION AUDIT

The comparison's "Best-of-Three Component Selection" table recommends 17 components. For each:
- **AGREE** or **DISAGREE** with the selection
- If you disagree, explain which alternative is better and why
- Flag any components where the comparison mischaracterized the source research

Pay special attention to:
1. The embedding model decision (BGE-M3 vs bge-small vs all-MiniLM)
2. The LLM inference decision (Llama 3.1 70B via vLLM — is this actually feasible on dual RTX 4090s?)
3. The frontend decision (custom React vs Open WebUI)
4. The relevance threshold decision (R2's 40% dynamic threshold)
5. The query contextualization vs no-query-expansion tension

### SECTION 5: BIAS AND BALANCE CHECK

Analyze whether the comparison document shows systematic bias:
- Does it unfairly favor or penalize any particular research result?
- Are the star ratings in the scoring summary justified by the detailed analysis?
- Does the synthesis fairly represent viable alternatives, or does it railroad toward a predetermined conclusion?
- Is the "R3 is the chassis, R2 is the engine, R1 is the soul" framing justified by the evidence?

### SECTION 6: CRITICAL GAPS

Identify anything that SHOULD be in this comparison analysis but ISN'T:
- Missing evaluation dimensions
- Unasked questions that would affect component selection
- Risks not flagged in the critical decision points
- Integration concerns between components selected from different research results

### SECTION 7: FINAL VERDICT

Provide your overall assessment:
- **Accuracy Score:** (1-10) How accurately does the comparison reflect the source documents?
- **Completeness Score:** (1-10) How comprehensively does it cover the source material?
- **Bias Score:** (1-10, where 10 = perfectly balanced) How fair and balanced is the analysis?
- **Actionability Score:** (1-10) How useful is the component selection table for actually building V10?
- **Top 3 Corrections:** The three most important things to fix in the comparison before using it to build V10.

---

## CRITICAL INSTRUCTIONS

1. **Read all 5 files before writing anything.** Do not begin your analysis until you have read every source document in full.

2. **Use specific line references and quotes.** When you identify an error or disagreement, cite the exact text from the source document and the comparison document.

3. **Do not add your own V10 design opinions.** Your job is to verify the accuracy and fairness of the comparison analysis, not to propose your own architecture. If you think a component selection is wrong, explain why based on evidence in the source documents, not your own preferences.

4. **Be hostile.** This is an adversarial audit. You are looking for mistakes, omissions, mischaracterizations, and logical flaws. Do not give the comparison the benefit of the doubt.

5. **The ground truth hierarchy is:**
   - **NOTEBOOKLM_INTEL.md** is the highest authority (confirmed findings from the actual platform)
   - **DEEP_RESEARCH_1/2/3.md** are the primary sources being analyzed
   - **DEEP_RESEARCH_COMPARISON.md** is the document being audited (do not trust it)

6. **Produce an exhaustive, detailed report.** This audit will determine whether the comparison analysis can be trusted to drive a production architecture. Err on the side of thoroughness.
