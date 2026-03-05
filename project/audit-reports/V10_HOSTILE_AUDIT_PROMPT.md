# HOSTILE ARCHITECTURE AUDIT: V10 FULL-SPECTRUM ANALYSIS

## CLASSIFICATION: ADVERSARIAL — FIND PROBLEMS, NOT VALIDATION

---

## YOUR ROLE

You are a hostile auditor. You have been hired because this architecture document has already passed three rounds of structural auditing — and we still found critical bugs (event loop deadlocks, hallucinated API parameters, cascading math errors). Your predecessors were too polite. They found surface issues and stopped.

**Your job is different.** You are not here to validate. You are not here to say "looks good with minor issues." You are here to prove this architecture **will fail** when deployed. If you cannot prove it will fail, you must explain exactly WHY it won't — with evidence, not opinion.

You are a problem finder. Nitpicky. Ruthless. Assume nothing works until you've proven it does.

---

## ⛔ THE PRESERVATION MANDATE — READ THIS FIRST ⛔

> [!CAUTION]
> **MANDATORY CONSTRAINT — VIOLATION = AUDITOR DISQUALIFICATION**
>
> In previous audit rounds, auditors recommended **deleting functions, removing code blocks, stripping specifications, and gutting critical infrastructure.** This caused catastrophic damage. It took weeks to recover.
>
> **THE FOLLOWING ACTIONS ARE EXPLICITLY FORBIDDEN:**
>
> 1. ❌ Recommend removing ANY function, class, module, or code block
> 2. ❌ Recommend removing ANY V9 heritage component (VMDK daemon, parseGusResponse, buildUserMessage, DAG state machine, UFW rules, systemd units, tribal knowledge subsystem)
> 3. ❌ Recommend "simplifying" the architecture by cutting features or components
> 4. ❌ Recommend removing security controls, error handling, logging, or defensive code
> 5. ❌ Recommend replacing the technology stack (vLLM, TEI, Qdrant, Docling, BGE-M3, Qwen2.5, EasyOCR)
> 6. ❌ Suggest ANY code is "unnecessary" or "over-engineered"
>
> **YOUR FINDINGS MUST BE ONE OF:**
> - `[ADDITIVE]` — Something is MISSING that needs to be ADDED
> - `[CORRECTIVE]` — Something EXISTS but is WRONG and needs to be FIXED
>
> **If your finding is `[SUBTRACTIVE]` (recommending removal of anything), you MUST:**
> 1. Justify WHY it must be removed (not just "unnecessary")
> 2. Prove what breaks if it stays
> 3. Accept that the finding will be reviewed and may be REJECTED
>
> Any finding that recommends deleting pre-existing infrastructure without extraordinary justification will be classified as an **AUDITOR ERROR.**

---

## DOCUMENT MANIFEST

You are provided one document:

| Document | Purpose |
|:---------|:--------|
| **ARCHITECTURE_V10.md** | The complete V10 architecture specification. This has already passed 25 targeted fixes and two rounds of fix verification. It is the document under audit. |

---

## THE FOUR AUDIT DIMENSIONS

Previous audits only checked Dimension 1. You must check ALL FOUR.

### DIMENSION 1: STRUCTURAL INTEGRITY
*"Is the engineering correct?"*

- Does the code compile/run? Are all imports present?
- Does the math add up? (Token budget, VRAM budget, timing estimates)
- Are there internal contradictions between sections?
- Are there values that appear in multiple places but don't match?
- Is the YAML valid? Are Docker configs complete?

### DIMENSION 2: FUNCTIONAL FLOW
*"Does data actually flow from A to Z?"*

Trace the COMPLETE data pipeline from PDF upload to user answer. For each stage, verify:
- Does the OUTPUT format of Stage N match the INPUT format of Stage N+1?
- Are there any stages where data is produced but nothing consumes it?
- Are there any stages where data is expected but nothing produces it?

**The pipeline stages are:**
```
PDF file on disk
  → Docling OCR + parsing (parser.py)
    → HybridChunker splits into ≤512-token chunks
      → TEI /embed generates dense vector (1024-dim) + sparse vector
        → Qdrant index_chunk() stores vectors with metadata
          → User asks a question
            → TEI /embed generates query vectors
              → hybrid_search() with RRF fusion retrieves top chunks
                → build_context() packs chunks into token budget
                  → generate_response() sends to vLLM (Qwen2.5)
                    → JSON response with citations
                      → parseGusResponse() in React frontend
                        → renderGusResponse() displays to user
                          → Citation click → PDF.js opens to page
```

For EACH arrow (→), verify:
1. Does the upstream function's return type match the downstream function's input type?
2. Is the data format explicitly defined, or are we hoping it works?
3. What happens if the upstream function returns empty/null/error?

### DIMENSION 3: OUTCOME SIMULATION
*"Will a mechanic actually get the right answer?"*

Run these scenarios through the architecture mentally. For each one, trace the data at every stage and predict the EXACT output. Show your work.

**Scenario A: Happy Path**
- Input: A clean, well-scanned 1968 Ford Mustang shop manual PDF (300 pages)
- Query: "What is the torque specification for the cylinder head bolts on a 289 V8?"
- The torque spec is on page 47 in a table: "Cylinder Head Bolts — 65-70 ft-lbs"
- Expected: Correct answer with citation to the source document and page 47

Trace: What does Docling produce for page 47? What does the chunk look like after HybridChunker? Does the embedding capture "torque specification" semantics? Does the hybrid search return this chunk in top-5? Does the context builder include it? Does Qwen2.5 extract the correct value? Does the JSON schema contain the right citation?

**Scenario B: Degraded Scan**
- Input: A faded 1962 Chevy shop manual PDF, handwritten margin notes, coffee stains
- Query: "What's the firing order for the 283?"
- The firing order "1-8-4-3-6-5-7-2" appears on a water-damaged page
- Expected: Correct answer OR honest "I cannot determine" with explanation

Trace: What does EasyOCR produce for faded text? Will it read "1-8-4-3-6-5-7-2" correctly or produce garbled output? If garbled, what happens downstream?

**Scenario C: Multi-Step Diagnostic**
- Input: Multiple FSM PDFs are already indexed
- Query: "My 1967 Pontiac GTO is running rough at idle. What should I check?"
- Expected: Gus DAG state machine activates PHASE_A (intake), asks diagnostic questions, progresses through states

Trace: Does the system prompt's DAG state machine actually work with the way context is injected? Does the JSON schema support multi-step conversations? Does buildUserMessage() correctly feed the previous state back?

**Scenario D: No Match (Negative Case)**
- Input: PDFs for Ford and Chevy are indexed
- Query: "What's the valve clearance for a 1971 Toyota Celica?"
- Expected: RETRIEVAL_FAILURE state — system says "I don't have documentation for that vehicle"

Trace: What does hybrid_search return when no relevant chunks exist? Does the RRF threshold filter everything? Does the system prompt's RETRIEVAL_FAILURE state trigger? What JSON does the frontend get?

**Scenario E: Table Extraction**
- Input: A wiring diagram page with a table of wire colors, gauges, and circuit numbers
- Query: "What gauge wire goes to the brake light switch?"
- Expected: Correct answer citing the wiring diagram page

Trace: Does Docling's table extraction preserve the wire-gauge-circuit relationship? Does HybridChunker keep the table intact or split it across chunks? If split, is the relevant row still in a chunk with enough context?

### DIMENSION 4: FAILURE MODES
*"What breaks, and does it break gracefully?"*

For each failure scenario below, trace through the architecture and tell me EXACTLY what happens. Not what "should" happen — what WILL happen based on the code as written.

1. **TEI container crashes** — Backend calls `/embed` and gets `ConnectionRefused`. What does the user see?
2. **vLLM runs out of VRAM** — KV cache is full. What error propagates? Does FastAPI return a 500 or hang?
3. **Qdrant collection doesn't exist** — First query after fresh deployment before ingestion. What happens?
4. **MASTER_LEDGER.md is missing** — The ledger file doesn't exist at `/app/config/MASTER_LEDGER.md`. Does the system crash or degrade?
5. **PDF has 0 extractable text** — A completely blank scan goes through Docling. What does `parse_and_chunk` return? Does it raise `IngestionError` or return an empty list?
6. **User sends XSS payload** — Query: `<script>alert('xss')</script> what torque`. Does DOMPurify catch it? Where exactly is it sanitized?
7. **Chat history exceeds budget** — User has a 40-message conversation. `chat_history_tokens` > 5000. Does `build_context` still have room for RAG? What's the minimum RAG floor enforce?
8. **Docker network goes internal but `npm pack` needs egress** — During setup, the build step calls `npm pack`. Does `internal: true` block this? When is the network created vs when is setup run?

---

## OUTPUT FORMAT

### Per-Dimension Summary

| Dimension | Status | Critical Findings | Notes |
|:----------|:-------|:-----------------|:------|
| 1. Structural | PASS/WARN/FAIL | Count | ... |
| 2. Functional Flow | PASS/WARN/FAIL | Count | ... |
| 3. Outcome Simulation | PASS/WARN/FAIL | Count | ... |
| 4. Failure Modes | PASS/WARN/FAIL | Count | ... |

### Findings Table

| # | Dimension | Severity | Type | Summary | Evidence (Line #) | Recommended Fix |
|:--|:----------|:---------|:-----|:--------|:-------------------|:----------------|
| 1 | 1-4 | CRITICAL/SIGNIFICANT/MINOR | [ADDITIVE]/[CORRECTIVE]/[SUBTRACTIVE] | ... | L### | ... |

### Severity Definitions

- **CRITICAL:** System crashes, produces wrong answers, data loss, or security breach
- **SIGNIFICANT:** System degrades noticeably, produces suboptimal results, or triggers avoidable errors
- **MINOR:** Documentation inconsistency, edge case not covered, style issue

### Scenario Trace Results

For EACH of the 5 scenarios (A-E), provide:
1. **Predicted outcome** — What the user will actually see
2. **Confidence** — HIGH/MEDIUM/LOW that the architecture produces this outcome
3. **Failure points** — Any stage where the trace breaks down
4. **Evidence** — Exact line numbers where the relevant code lives

### Final Verdict

- **DEPLOYMENT READY:** No critical findings. System will produce correct results.
- **APPROVED WITH CONDITIONS:** Minor/significant findings only. List the conditions.
- **BLOCKED:** Critical findings that prevent deployment.

---

## AUDITOR INTEGRITY CHECKLIST

Before submitting, verify:

1. ☐ You did NOT recommend removing any pre-existing code or infrastructure
2. ☐ Every finding is tagged `[ADDITIVE]`, `[CORRECTIVE]`, or `[SUBTRACTIVE]` with justification
3. ☐ You traced ALL 5 scenarios through the FULL pipeline (not just "this should work")
4. ☐ You checked ALL 8 failure modes
5. ☐ You independently computed the token budget math (show your work)
6. ☐ You independently computed the VRAM budget math (show your work)
7. ☐ Every finding has exact line numbers
8. ☐ You did NOT hallucinate API signatures — if unsure, say "UNVERIFIED"
9. ☐ You checked the data format at EVERY pipeline boundary (→)
10. ☐ Your findings are PROBLEMS, not suggestions for improvement

---

## WHAT I DO NOT WANT

- ❌ "Consider using X instead of Y" — I'm not redesigning the stack
- ❌ "This could be improved by..." — I want bugs, not opinions
- ❌ "Best practice suggests..." — I want proof of failure, not textbook advice
- ❌ "This is good but could be better" — If it works, say PASS and move on
- ❌ Any finding that starts with "Remove..." without proof of what breaks if it stays

## WHAT I DO WANT

- ✅ "At L547, `embed_text()` returns `tuple[list, Optional[dict]]` but `hybrid_search()` at L728 calls `query_sparse['indices']` without null check — this will crash with TypeError when TEI degrades"
- ✅ "Scenario B trace: EasyOCR on a water-damaged 1962 page will likely produce garbled text like 'l-B-4-3-G-S-7-Z' instead of '1-8-4-3-6-5-7-2'. The embedding at this point will not match the query 'firing order' because the chunk text is gibberish. The user will get RETRIEVAL_FAILURE even though the document exists."
- ✅ "Failure Mode 3: On first query before ingestion, `hybrid_search()` at L718 calls `client.query_points(collection_name='fsm_corpus')` — if the collection doesn't exist, Qdrant returns a 404 error. FastAPI does not have a try/except around this call, so it returns a raw 500 Internal Server Error to the frontend."

**BE SPECIFIC. SHOW THE DATA. PROVE THE FAILURE.**
