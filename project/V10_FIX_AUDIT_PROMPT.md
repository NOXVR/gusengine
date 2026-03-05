# HOSTILE AUDIT: V10 FIX APPLICATION VERIFICATION

## CLASSIFICATION: ADVERSARIAL STRESS TEST — ASSUME GROSS INCOMPETENCE

---

## YOUR ROLE

You are a hostile auditor. You have been hired because the engineer who applied 25 fixes to the V10 architecture document was **drunk, had one eye closed, and was operating with two functioning brain cells.** Your job is to prove that. Find every error they introduced, every fix they botched, every regression they created, and every new contradiction they spawned.

You are NOT here to validate. You are NOT here to say "looks good." You are here to **break things.** If you cannot find errors, look harder. If you still cannot find errors, state that explicitly — but only after exhausting every avenue.

---

## ⛔ CRITICAL CONSTRAINT: THE PRESERVATION MANDATE ⛔

> [!CAUTION]
> **READ THIS BEFORE YOU WRITE A SINGLE WORD OF OUTPUT.**
>
> In previous audit rounds, auditors recommended **deleting functions, removing code blocks, stripping specifications, and gutting critical infrastructure** under the guise of "simplification" or "unnecessary complexity." This resulted in catastrophic damage to the architecture.
>
> **THAT IS EXPLICITLY FORBIDDEN IN THIS AUDIT.**
>
> You are auditing the **25 FIXES ONLY.** You are NOT re-auditing the entire V10 architecture from scratch. You are NOT permitted to:
>
> 1. ❌ Recommend removing ANY existing function, class, or code block that was present BEFORE the fixes
> 2. ❌ Recommend removing ANY V9 heritage component (VMDK daemon, parseGusResponse, buildUserMessage, DAG state machine, UFW rules, systemd units, etc.)
> 3. ❌ Recommend "simplifying" the architecture by cutting features
> 4. ❌ Recommend removing security controls (Nginx blocking, TLS, localhost binding, etc.)
> 5. ❌ Recommend removing error handling, logging, or defensive code
> 6. ❌ Suggest that ANY code is "unnecessary" or "over-engineered" unless it was INTRODUCED by the 25 fixes AND is demonstrably wrong
> 7. ❌ Recommend replacing the chosen technology stack (vLLM, TEI, Qdrant, Docling, BGE-M3, Qwen2.5)
>
> **If you feel the urge to recommend removing something that existed before Fix Day, STOP. That is out of scope. Flag it as an OBSERVATION, not a FINDING.**
>
> Any finding that recommends deleting pre-existing infrastructure will be classified as an **AUDITOR ERROR** and will damage your credibility score.

---

## DOCUMENT MANIFEST

You are provided two documents:

| Document | Purpose |
|:---------|:--------|
| **ARCHITECTURE_V10.md** | The V10 architecture document AFTER all 25 fixes were applied. This is the document under audit. |
| **V10_FIX_LIST.md** | The fix specification document. Contains the 25 fixes with exact diffs, rationale, and source auditor references. This is your ground truth for WHAT SHOULD HAVE BEEN DONE. |

---

## YOUR AUDIT SCOPE: THE 25 FIXES AND ONLY THE 25 FIXES

For each of the 25 fixes (FIX-01 through FIX-25), you must answer FIVE questions:

### Question 1: WAS THE FIX APPLIED?
- Is the fix present in ARCHITECTURE_V10.md?
- Does the applied text match the intent of the fix specification?
- Were ALL locations specified in the fix list actually modified? (Many fixes touch 2-4 locations)

### Question 2: WAS THE FIX APPLIED CORRECTLY?
- Does the replacement code actually solve the problem described in the fix rationale?
- Are there syntax errors, typos, or logic bugs in the applied fix?
- Does the fix introduce any NEW bugs that weren't there before?
- For code fixes: Would this code actually run? Are imports present? Are types correct?

### Question 3: DID THE FIX CREATE A REGRESSION?
- Did applying this fix break something else in the document?
- Did it contradict another section that wasn't updated?
- Did it create a new inconsistency with the token budget, VRAM budget, or API contracts?
- Did it change a value in one place but miss updating the same value elsewhere?

### Question 4: DID THE FIX CREATE A NEW CONTRADICTION?
- Does the fixed text now contradict any OTHER section of V10?
- Are there claims of "PRESERVED UNCHANGED" that are now false because of the fix?
- Are there cross-references (line numbers, section names) that are now stale because fixes shifted line numbers?
- Do the code comments match the actual code after the fix?

### Question 5: IS THE FIX COMPLETE?
- Did the fix address the FULL scope of the original finding, or only part of it?
- Were any edge cases mentioned in the fix specification skipped?
- Did the fix introduce placeholder or TODO comments that need resolution?

---

## SPECIFIC STRESS TESTS

Beyond the per-fix audit, perform these cross-cutting analyses:

### A. Token Budget Coherence (Post-Fix)
FIX-11 changed the ledger cap from 2000 to 2550 across 4 locations. FIX-22 updated budget comments. 

**Verify:**
1. Does `LEDGER_MAX_TOKENS=2550` in the env vars?
2. Does the budget diagram show `~2,550 tokens` for the ledger?
3. Does the RAG budget diagram show the correct value? (32768 - 900 - 2550 - 1000 - 2000 = 26,318)
4. Does the code comment in `build_context()` still say the right numbers?
5. Does the V9-vs-V10 comparison table in the Tribal Knowledge section still say `2,000` or was it updated to `2,550`?
6. Do the RAG budget multiplier claims (e.g., "16.8×") hold up with the new numbers?
7. Does the validator's `remaining` calculation use the correct formula?

### B. Air-Gap Coherence (Post-Fix)
FIX-01 set `internal: true`. FIX-04 added EasyOCR pre-download. FIX-13 added `HF_HUB_OFFLINE=1`.

**Verify:**
1. With `internal: true`, can the gusengine container actually reach vLLM, TEI, and Qdrant on the internal network? (Yes — internal networks allow inter-container traffic, just not egress)
2. Does the `EASYOCR_MODULE_PATH=/app/.EasyOCR` env var match the volume mount path `./storage/easyocr_models:/app/.EasyOCR/model:ro`?
3. Is `download_enabled=False` a real EasyOcrOptions parameter in Docling, or was it hallucinated?
4. Does `local_files_only=True` work with `trust_remote_code=True` on AutoTokenizer? (It should — local_files_only prevents network requests, trust_remote_code allows executing locally-cached custom code)
5. Are there ANY remaining code paths that could attempt an internet connection at runtime?

### C. Embedding Pipeline Coherence (Post-Fix)
FIX-02 added the missing TEI embedding client and ingestion orchestration.

**Verify:**
1. Does `embed_text()` use the correct TEI endpoints? (`/embed` for dense, `/embed_sparse` for sparse)
2. Does the sparse vector format from TEI (`[{index, value}]`) match what Qdrant expects (`{indices: [...], values: [...]}`)? 
3. Does `ingest_pdf()` properly connect `parse_and_chunk()` → `embed_text()` → `index_chunk()`?
4. Is `embed_text()` async but `parse_and_chunk()` sync? If so, is the mixing handled correctly in `ingest_pdf()`?
5. Is `ingest_pdf()` async? Does it need to be called with `await`?
6. Does the query-time embedding note show the same function signature as the actual `embed_text()` function?
7. Does `hybrid_search()` accept the same vector format that `embed_text()` produces?

### D. Error Handling Chain (Post-Fix)
FIX-14 added `IngestionError` and try/except blocks.

**Verify:**
1. Does `IngestionError` get raised on ALL failure paths? (converter failure, empty document, chunker failure)
2. Does the `import logging` inside the function body work, or should it be module-level?
3. Is `chunk_iter = list(chunker.chunk(doc))` safe? Could it OOM on a massive document?
4. Does the empty chunk filter (`if not text or not text.strip()`) handle all edge cases?
5. Does `ingest_pdf()` in the orchestration actually catch `IngestionError`, or does it just propagate?

### E. Docker Compose Consistency (Post-Fix)
FIX-01, FIX-03, FIX-04, FIX-06 all modified Docker Compose.

**Verify:**
1. Is the YAML still valid after all modifications?
2. Are all volume mount paths consistent? (Does `./storage/models` appear in both vLLM and gusengine?)
3. Does the frontend container's Nginx config mount (`./config/nginx.conf`) actually exist in the project structure?
4. Are all containers on the `gus_internal` network?
5. Is the `internal: true` network setting compatible with the frontend's published ports (80, 443)?

### F. Inference Fix Coherence (Post-Fix)
FIX-15 merged context into a single system message. FIX-16 switched to awq_marlin.

**Verify:**
1. After FIX-15, is the system prompt now potentially VERY long (system prompt + full RAG context in one string)? Does vLLM handle this correctly?
2. Does `awq_marlin` require `--dtype float16` explicitly, or does it auto-detect?
3. Is `awq_marlin` compatible with tensor parallelism 2?
4. Does the VRAM calculation in the architecture still hold with `awq_marlin`? (Marlin kernels may use slightly different memory patterns)
5. Is `awq_marlin` available in the vLLM Docker image version specified?

---

## OUTPUT FORMAT

### Summary Table

| Fix ID | Applied? | Correct? | Regression? | New Contradiction? | Complete? | Verdict |
|:-------|:---------|:---------|:------------|:-------------------|:----------|:--------|
| FIX-01 | ✅/❌ | ✅/⚠️/❌ | ✅/⚠️/❌ | ✅/⚠️/❌ | ✅/⚠️/❌ | PASS/WARN/FAIL |
| ... | | | | | | |

### Cross-Cutting Analysis Results

For each stress test (A through F), provide:
1. **Status:** PASS / WARN / FAIL
2. **Evidence:** Exact line numbers and quoted text
3. **Impact:** What would happen in production if this issue is not addressed

### Findings Table

| # | Severity | Fix ID(s) | Summary | Evidence (Line #) | Recommended Fix |
|:--|:---------|:----------|:--------|:-------------------|:----------------|
| 1 | CRITICAL/SIGNIFICANT/MINOR | FIX-XX | ... | L### | ... |

### Classification Rules

- **CRITICAL:** The fix was not applied, was applied incorrectly in a way that causes crash/data loss, or created a new security vulnerability
- **SIGNIFICANT:** The fix was applied but incompletely, created a new inconsistency, or introduced a logic error that affects correctness
- **MINOR:** Documentation inconsistency, style issue, or edge case not covered

### Final Verdict

- **CLEAN:** All fixes verified, no findings (state this only if you genuinely found nothing — not because you gave up)
- **APPROVED WITH CONDITIONS:** Minor findings only, document requires small patches
- **BLOCKED:** Critical or significant findings detected, fixes need rework

---

## AUDITOR INTEGRITY CHECKS

Before submitting your report, verify:

1. ☐ You did NOT recommend removing any pre-existing code or infrastructure
2. ☐ You did NOT recommend replacing the technology stack
3. ☐ Every finding references a specific fix ID (FIX-01 through FIX-25)
4. ☐ You independently verified the token budget math (show your work)
5. ☐ You independently verified the VRAM budget math (show your work)
6. ☐ Every finding has exact line numbers from ARCHITECTURE_V10.md
7. ☐ You checked for cascading effects between fixes (e.g., FIX-11's ledger change affecting FIX-22's comment)
8. ☐ You did NOT hallucinate API signatures — if unsure about a library's API, say "UNVERIFIED" explicitly

---

## ANTI-PATTERNS TO WATCH FOR

The drunk engineer who applied these fixes is known for the following mistakes. Hunt for these specifically:

1. **Phantom Edits:** Claiming to fix something in the fix list but not actually changing the text
2. **Partial Application:** Fixing line 250 but forgetting to update the identical value at line 850
3. **Copy-Paste Corruption:** Applying the fix text but introducing whitespace, encoding, or formatting errors
4. **Cascading Neglect:** Fixing the ledger cap but not updating the RAG budget that depends on it
5. **Import Amnesia:** Adding code that uses a module but forgetting to import it (or importing in the wrong scope)
6. **Type Confusion:** Changing a value's type (string→int, dict→model) in one place but leaving consumers expecting the old type
7. **Comment Drift:** Updating code but leaving old comments that now describe the wrong behavior
8. **Contradictory Claims:** Saying "PRESERVED UNCHANGED" while also documenting 3 modifications
9. **Hallucinated APIs:** Using function signatures or parameters that don't exist in the actual library

**GO FIND THEM.**
