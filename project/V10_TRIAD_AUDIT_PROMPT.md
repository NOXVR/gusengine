# V10 ARCHITECTURE TRIAD AUDIT — HOSTILE VERIFICATION PROMPT

**DATE:** 2026-02-24
**TARGET:** `ARCHITECTURE_V10.md` (1,123 lines, 48 KB)
**METHODOLOGY:** Independent hostile audit. You are ONE of THREE auditors. You will NOT see the other auditors' work. Your findings will be cross-examined against the other two for consensus convergence.

---

## YOUR MANDATE

You are a hostile auditor performing an adversarial review of the V10 architecture for a life-safety-adjacent automotive diagnostic RAG engine. Your job is to **find every error, contradiction, omission, and fatal flaw** in the target document.

> [!CAUTION]
> **FIDELITY RULE — READ THIS BEFORE ANYTHING ELSE:**
> You are an AUDITOR, not an ARCHITECT. Your job is to VERIFY, not REDESIGN.
>
> **YOU MUST NOT:**
> - Propose alternative architectures, models, or frameworks
> - Spend tokens solving problems you find — IDENTIFY them, cite the line, state why it's wrong, and move on
> - Suggest switching to a different LLM, vector store, embedding model, or any other component UNLESS the existing choice is provably non-functional
> - Pad your output with explanatory tutorials about how RAG works, how transformers work, or how GPUs work
> - Restate the architecture back to us — we wrote it, we know what it says
>
> **YOU MUST:**
> - Read EVERY LINE of every document provided
> - Cross-reference claims in V10 against the source documents (V9 Frozen, DNA, NotebookLM Intel)
> - Independently verify ALL math (VRAM, token budgets, KV cache, context windows)
> - Flag contradictions between V10 and its source documents
> - Flag missing V9 heritage (components that should have been preserved but weren't)
> - Flag air-gap violations (any component that requires internet at inference time)
> - Flag code errors (syntax, logic, API misuse, missing imports)
> - Classify every finding by severity: 💀 CRITICAL, ⚠️ SIGNIFICANT, 🔍 MINOR

---

## VRAM VERIFICATION — MANDATORY INDEPENDENT CALCULATION

> [!CAUTION]
> **THE #1 FAILURE MODE of prior audits was VRAM math.** Three previous auditors spent enormous effort arguing about whether 70B models fit on 48GB VRAM, consuming 30-40% of their audit tokens on a problem that was ALREADY SOLVED by downgrading to 32B. 
>
> **YOUR TASK IS NOT TO SOLVE THE VRAM PROBLEM. IT IS ALREADY SOLVED.**
>
> Your task is to VERIFY that the solution is correct by performing this exact calculation:

### Required Verification Steps

1. **Model Weights:** Qwen2.5-32B-Instruct-AWQ (4-bit quantization). Calculate: 32 billion params × 4 bits / 8 bits per byte = ? GB. Verify V10's claim of ~18 GB.

2. **KV Cache @ 32K context:** Qwen2.5-32B has 64 layers, 8 KV heads (GQA), 128 head dimension. Calculate: 64 × 8 × 128 × 2 (K+V) × 2 bytes (FP16) × 32,768 tokens = ? GB. Verify V10's claim of ~8 GB.

3. **Total:** Weights + KV Cache + vLLM overhead (~2 GB) + BGE-M3 (~2 GB) + TEI overhead (~0.5 GB) = ? GB. Verify this fits in 48 GB with headroom.

4. **Report your numbers.** If they match V10's claims (within ±2 GB), state "VRAM VERIFIED" and move on. If they don't match, flag it as a finding with your numbers.

**DO NOT:**
- Propose alternative models or quantization schemes
- Discuss what would happen at 64K or 128K context (V10 already documents this)
- Explain how KV cache works
- Suggest FP8, GPTQ, or any other quantization format
- Spend more than 10% of your output on VRAM analysis

---

## DOCUMENTS PROVIDED

You must read ALL of the following documents. They are provided in order of priority.

### Document 1: TARGET — `ARCHITECTURE_V10.md`
**This is the document you are auditing.** Read every line.

### Document 2: HERITAGE SOURCE — `ARCHITECTURE_FINAL_V9_FROZEN.md` (2,107 lines)
**The predecessor architecture.** V10 claims to preserve specific V9 components. You must verify:
- Is the Gus DAG system prompt preserved correctly? (V9 lines 1303-1356 → V10 system prompt section)
- Is `parseGusResponse()` logic described correctly? (V9 lines 1457-1483)
- Is `buildUserMessage()` logic described correctly? (V9 lines 1488-1523)
- Are V9 security measures (UFW, Nginx, TLS, localhost binding, upload blocking) accurately referenced?
- Is the VMDK/OVA extraction daemon accurately described?
- Is the tribal knowledge subsystem (validate_ledger.py, sync_ledger.py, update_ledger.sh) accurately referenced?
- Are V9's 49 audit findings preserved by reference?

### Document 3: GROUND TRUTH — `PROJECT_DNA_V9.md` (775 lines)
**The engineering decision record.** Cross-reference V10's design choices against DNA decisions. Flag any V10 choices that contradict DNA engineering decisions without explicit justification.

### Document 4: BENCHMARK — `NOTEBOOKLM_INTEL.md` (179 lines)
**The competitive benchmark.** V10 claims to achieve "NotebookLM parity" in several areas. Verify:
- Does Docling HybridChunker actually achieve structural segmentation comparable to NotebookLM's described approach?
- Is the dual-layer architecture (text for LLM, original PDF for display) correctly implemented?
- Is the "greedy token-capped context injection" comparable to NotebookLM's "raw, sequential plain-text strings divided into numerical excerpts"?

### Document 5: PRIOR AUDIT — `COMPARISON_AUDIT_OPUS.md` (411 lines)
**The most accurate prior auditor** (7/10 accuracy). Check whether V10 incorporated Opus's key findings, including:
- VMDK/OVA heritage preservation
- TOCTOU-immune file locking
- Custom React vs Open WebUI decision
- CDN air-gap violation (unpkg.com)
- R1's OCR gap (PyMuPDF zero text on scans)

### Document 6: PRIOR AUDIT — `COMPARISON_AUDIT_GEMINI.md`
**Gemini Deep Think audit.** Check whether V10 incorporated GT's key findings, including:
- Token estimation regression (R2's linear regression vs native tokenizer)
- R3's CDN air-gap violation
- Context limit as code, not model constraint

### Document 7: PRIOR AUDIT — `COMPARISON_AUDIT_GEMINI_DR.md`
**Gemini Deep Research audit.** Check whether V10 incorporated DR's key findings, including:
- Detailed GPU math (27 cited sources)
- LanceDB vs Qdrant argument (V10 chose Qdrant — verify rationale)
- KV cache compression (GEAR/AQUA-KV) — V10 defers this
- bge-small-en-v1.5 vs BGE-M3 (V10 chose BGE-M3 — verify rationale)
- Docling ingestion time estimate

---

## AUDIT CHECKLIST

For each section of `ARCHITECTURE_V10.md`, verify the following:

### A. Component Map
- [ ] All 5 containers represented (vLLM, TEI, Qdrant, GusEngine, Frontend)
- [ ] Port assignments consistent between diagram and Docker Compose
- [ ] Volume mounts described match Docker Compose volumes
- [ ] No external network dependencies at inference time

### B. GPU Memory Budget
- [ ] VRAM math independently verified (see mandatory calculation above)
- [ ] KV cache formula correct for Qwen2.5-32B architecture (GQA heads, layers, dim)
- [ ] Scale-up table realistic
- [ ] No claim of 128K context on 48GB VRAM

### C. Docker Compose
- [ ] All service definitions syntactically valid
- [ ] GPU passthrough configured correctly (NVIDIA runtime)
- [ ] Localhost binding on all internal ports
- [ ] Log rotation on all containers
- [ ] Environment variables consistent with code references
- [ ] Model paths in volume mounts match model download commands
- [ ] `depends_on` ordering correct

### D. Ingestion Pipeline
- [ ] Docling API usage correct (imports, class names, method signatures)
- [ ] `do_ocr=True` explicitly set (audit fix for R1's PyMuPDF gap)
- [ ] HybridChunker usage correct
- [ ] AutoTokenizer usage correct (not tiktoken)
- [ ] Page number extraction from Docling metadata realistic
- [ ] Ingestion time estimate for 514 PDFs (~2,442 pages) realistic

### E. Embedding & Indexing
- [ ] BGE-M3 dimensions correct (1024 dense)
- [ ] Qdrant collection schema valid (dense + sparse vectors)
- [ ] Sparse vector configuration correct for BM25-like behavior
- [ ] Index function correctly creates points with all required payload fields

### F. Retrieval Pipeline
- [ ] Qdrant query API usage correct (Prefetch, FusionQuery, Fusion.RRF)
- [ ] Dynamic threshold calculation correct (40% of top score)
- [ ] Greedy context builder correctly counts tokens
- [ ] Token budget math adds up (32768 - 900 - 2000 - 2000 = 27,868)
- [ ] Context formatting includes provenance headers

### G. Inference Layer
- [ ] vLLM CLI flags correct and compatible with Qwen2.5-32B-AWQ
- [ ] OpenAI-compatible API endpoint correct (`/v1/chat/completions`)
- [ ] Temperature 0.1 appropriate for deterministic JSON output
- [ ] Message assembly (system + context + history + user) correct

### H. System Prompt (Gus DAG V10)
- [ ] DAG state machine preserved from V9 (PHASE_A → B → C → D, with B looping)
- [ ] Citation rules updated for Qdrant metadata (not AnythingLLM sources[].title)
- [ ] JSON output schema unchanged from V9
- [ ] RETRIEVAL_FAILURE safeguard preserved
- [ ] STATE TRANSITION ENFORCEMENT preserved
- [ ] No contradictions between V10 system prompt and V9 system prompt

### I. Frontend Architecture
- [ ] PDF.js self-hosted (no CDN dependency)
- [ ] V9 CSS class contract preserved
- [ ] `parseGusResponse()` and `buildUserMessage()` referenced correctly
- [ ] DOMPurify sanitization mentioned (V9 XSS warning)

### J. Tribal Knowledge
- [ ] Token budget updated for 32K context
- [ ] AutoTokenizer replaces tiktoken
- [ ] Ledger injection mechanism (FastAPI file read) described
- [ ] Archive lifecycle mentioned

### K. Security
- [ ] All V9 security measures listed
- [ ] No new external API dependencies
- [ ] Air-gap verified across all components

### L. Verification
- [ ] All 15 checklist items executable
- [ ] Expected outputs realistic
- [ ] GPU verification step included
- [ ] Air-gap verification step included

### M. Known Boundaries
- [ ] Honestly stated limitations
- [ ] No overclaiming of capabilities
- [ ] Upgrade path realistic

---

## OUTPUT FORMAT

Your output MUST follow this exact format:

```markdown
# V10 ARCHITECTURE AUDIT — [YOUR AUDITOR NAME]

## VRAM Verification
[Your independent calculation. Max 10 lines. End with VRAM VERIFIED or VRAM FAILED.]

## Findings Table

| # | Line(s) | Section | Severity | Finding | Evidence |
|:--|:--------|:--------|:---------|:--------|:---------|
| 1 | L42-45 | Component Map | 💀 CRITICAL | [What's wrong] | [Why it's wrong, citing source doc] |
| 2 | L120 | Docker Compose | ⚠️ SIGNIFICANT | [What's wrong] | [Why] |
| ... | ... | ... | ... | ... | ... |

## Heritage Verification

| V9 Component | Preserved in V10? | Accurate? | Notes |
|:-------------|:----------------:|:---------:|:------|
| Gus DAG State Machine | ✅ | ✅ / ❌ | [Notes] |
| parseGusResponse() | ✅ | ✅ / ❌ | [Notes] |
| ... | ... | ... | ... |

## NotebookLM Parity Check

| NotebookLM Finding | V10 Implementation | Gap? |
|:-------------------|:-------------------|:-----|
| Dual-track ingestion | [How V10 addresses] | [Yes/No + details] |
| ... | ... | ... |

## Audit Checklist Results
[Mark each item from the checklist A-M as PASS / FAIL with brief notes on failures]

## Summary Statistics

| Metric | Count |
|:-------|:------|
| 💀 CRITICAL findings | ? |
| ⚠️ SIGNIFICANT findings | ? |
| 🔍 MINOR findings | ? |
| Total lines audited | 1,123 |
| Heritage items verified | ?/? |
| NotebookLM parity items | ?/? |

## Overall Verdict

**VERDICT:** [APPROVED / APPROVED WITH CONDITIONS / BLOCKED]
[1-3 sentences max. No essays.]
```

---

## ANTI-PATTERN WARNINGS

The following anti-patterns were observed in prior audits and MUST be avoided:

1. **The Redesign Trap:** Do NOT propose alternative architectures. If Qdrant is wrong, say WHY with evidence. Do not draft a LanceDB replacement.

2. **The VRAM Essay:** Do NOT write 2,000 words about GPU memory. Verify the math in 10 lines. Move on.

3. **The Tutorial Trap:** Do NOT explain how RAG pipelines work, how embeddings work, or how transformers work. We know. You're auditing an architecture document, not teaching a class.

4. **The Token Sink:** Prior auditors spent 30-40% of their tokens on VRAM analysis because it's a complex, engaging problem. **CAP YOUR VRAM SECTION AT 10 LINES.** If the math checks out, say so and move to the next section. Your valuable tokens should be spent on FINDING ERRORS, not CONFIRMING CORRECT WORK.

5. **The Overclaim:** Do NOT claim the architecture "will fail" unless you can prove it with math, code analysis, or verifiable API documentation. "I feel like this might be an issue" is not a finding.

6. **The Missing Homework Problem:** Every finding MUST cite a specific line number in `ARCHITECTURE_V10.md` AND a specific source document + line that contradicts it. Unsourced findings will be discarded.

---

**END OF AUDIT PROMPT. BEGIN YOUR AUDIT NOW.**
