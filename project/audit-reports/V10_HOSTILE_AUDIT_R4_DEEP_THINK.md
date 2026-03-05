# **V10 HOSTILE ARCHITECTURE AUDIT — PHASE 4 REPORT**

## **SCENARIO TRACES (Predicted Outcomes)**

* **Scenario P (Oversized Message \+ User Query at Cap):** **CRITICAL OVERFLOW (OOM).** The budget math divergence between chat.py and context\_builder.py guarantees a crash. P3-02 forces chat\_history to physically retain the 9,000-token string. However, build\_context() mathematically clamps the history token subtraction to 8,000. It allocates RAG chunks based on a "phantom budget", generating a final vLLM sequence of 33,768 tokens. This breaches the 32,768 hard limit, crashing the inference engine with an HTTP 400\.  
* **Scenario Q (PHASE\_ERROR Accumulation):** **CATASTROPHIC STATE WIPE.** The 10,001-token user query and 200-token PHASE\_ERROR enter history. The eviction loop processes in reverse, keeping the 200-token error, then evaluating the 10,001 query. It instantly breaks because 10,201 \> 8,000. The truncated array now contains *only* the assistant's 200-token error. The post-eviction validator (DT-P3-07) detects an orphaned assistant message and strips it. History becomes \[\]. The user's entire multi-turn diagnostic state is permanently erased.  
* **Scenario R (Persistent httpx Client after TEI Restart):** **SAFE DEGRADATION.** httpx.AsyncClient relies on an internal HTTP connection pool. The dead TCP socket raises a RemoteProtocolError on the first subsequent request. The try/except block in chat.py catches this, returning a graceful PHASE\_ERROR JSON. httpx automatically evicts the dead socket, and the next request self-heals via a fresh handshake.  
* **Scenario S (Race Between Ingestion and First Chat):** **ABORTED ON ARRIVAL.** Qdrant's MVCC would seamlessly isolate concurrent client.upsert() and FusionQuery executions, but ingestion never reaches the database. The webhook payload from the host daemon contains an absolute host path (/home/...) which is instantly rejected by the container's path traversal firewall.  
* **Scenario T (DOMPurify Sanitization of Valid Diagnostic Content):** **CRITICAL DATA CORRUPTION.** DOMPurify natively classifies automotive schematic notation (e.g., \<B+\>, \<GND\>) as unauthorized HTML tags. It silently strips them, rendering life-safety instructions unreadable and dangerous.

---

## **FINDINGS**

### **FINDING-P4-01: Ghost Budget Overflow via Math Clamping**

* **Dimension:** 4 (Numerical Verification / Scenario P)  
* **Severity:** CRITICAL  
* **Classification:** \[SUBTRACTIVE\]  
* **Description:** P3-02 forces chat\_history to physically retain oversized messages (\>8000 tokens) to prevent empty history errors. However, a legacy clamp in build\_context artificially limits the chat\_history\_tokens variable to exactly 8000 when performing budget math. This allocates "phantom space" to the RAG budget that doesn't actually exist. Furthermore, formatting overhead (ChatML markers, section headers) pushes the payload an extra \~50 tokens over the limit.  
* **Proof:** Scenario P trace. chat\_history \= 9000 actual tokens. build\_context clamps math to 8000\. available \= 32768 \- 900 (sys) \- 2550 (ledger) \- 2000 (resp) \- 8000 (clamped) \- 9999 (query) \= 9319 tokens. Total prompt sent to vLLM \= 900 \+ 2550 \+ 9319 \+ 9000 (actual history) \+ 9999 \+ 2000 \= **33,768 tokens**. 33768 \> 32768 causes vLLM to immediately crash.  
* **Fix:** Remove the 8000-token clamping block entirely from build\_context(). The context builder must subtract the physical size of the history array. Additionally, subtract a 50-token FRAMING\_RESERVE from available.

Python

\# In backend/retrieval/context\_builder.py, REMOVE lines 29-34 entirely:  
\# if chat\_history\_tokens \> MAX\_CHAT\_HISTORY\_TOKENS:  
\#     chat\_history\_tokens \= MAX\_CHAT\_HISTORY\_TOKENS

### **FINDING-P4-02: Single-Signal Fusion Query Crash**

* **Dimension:** 2 (Fix Interaction Matrix)  
* **Severity:** CRITICAL  
* **Classification:** \[CORRECTIVE\]  
* **Description:** Fix DT-8 conditionally drops the sparse prefetch object if TEI degrades, leaving a prefetch\_list of length 1\. However, P3-08's hybrid\_search unconditionally passes this to FusionQuery(fusion=Fusion.RRF). Qdrant physically requires at least 2 prefetch queries to perform a fusion; executing RRF on a single query triggers a fatal HTTP 400 validation error, destroying the dense-only fallback path and halting all chat operations.  
* **Proof:** TEI sparse fails. prefetch\_list contains only dense. client.query\_points executes FusionQuery. Qdrant rejects it: Bad request: Fusion requires at least 2 prefetch queries. hybrid\_search raises an unhandled exception.  
* **Fix:** Conditionally structure the Qdrant query payload.

Python

   if len(prefetch\_list) \== 1:  
        results \= client.query\_points(collection\_name="fsm\_corpus", query=prefetch\_list\[0\].query, limit=top\_k)  
    else:  
        results \= client.query\_points(collection\_name="fsm\_corpus", prefetch=prefetch\_list, query=FusionQuery(fusion=Fusion.RRF), limit=top\_k)

### **FINDING-P4-03: DOMPurify Strips Critical Automotive Symbols**

* **Dimension:** 3 (Frontend State Machine Consistency)  
* **Severity:** CRITICAL  
* **Classification:** \[CORRECTIVE\]  
* **Description:** The DT-P3-06 DOMPurify implementation assigns sanitized LLM text to .innerHTML. Automotive FSMs heavily rely on angle brackets for pin designations (\<B+\>, \<GND\>). DOMPurify parses these as invalid HTML tags and blindly excises them, permanently destroying critical diagnostic parameters.  
* **Proof:** Scenario T trace. instructions.innerHTML \= DOMPurify.sanitize("Check voltage at \<B+\>") resolves to "Check voltage at ". The mechanic probes the wrong pin.  
* **Fix:** The LLM strictly emits plain string text. Bypass .innerHTML parsing entirely and use .textContent, which natively prevents XSS while preserving all literal characters.

JavaScript

// In frontend renderGusResponse:  
  const instructions \= document.createElement('div');  
  instructions.className \= 'gus-instructions';  
  instructions.textContent \= gus.mechanic\_instructions; // Natively safe  
  containerEl.appendChild(instructions);  
// Apply identical .textContent fix to gus.diagnostic\_reasoning

### **FINDING-P4-04: Host-to-Container Webhook Path Mismatch**

* **Dimension:** 6 (Docker Infrastructure Post-Fix State)  
* **Severity:** CRITICAL  
* **Classification:** \[CORRECTIVE\]  
* **Description:** The manual-ingest.service daemon runs natively on the host OS and sends absolute host paths (e.g., /home/user/storage/pdfs/manual.pdf) to the containerized /api/ingest endpoint. The FastAPI backend validates pdf\_path.startswith(ALLOWED\_PDF\_DIR \+ "/"), where ALLOWED\_PDF\_DIR is strictly /app/pdfs. The host path fails this check, instantly blocking 100% of automated ingestions.  
* **Proof:** Daemon POSTs {"pdf\_path": "/home/user/storage/pdfs/manual.pdf"}. Container checks if it starts with /app/pdfs/. It doesn't. Route instantly returns {"status": "rejected", "message": "Path outside allowed directory"}.  
* **Fix:** Extract the filename from the webhook payload and construct the containerized path dynamically before validation.

Python

\# In backend/routes/ingest.py  
    body \= await request.json()  
    filename \= os.path.basename(body\["pdf\_path"\])  
    pdf\_path \= os.path.realpath(os.path.join(ALLOWED\_PDF\_DIR, filename))

### **FINDING-P4-05: Eviction Loop Cascade Wipes Entire DAG State**

* **Dimension:** 2 (Fix Interaction Matrix)  
* **Severity:** SIGNIFICANT  
* **Classification:** \[CORRECTIVE\]  
* **Description:** When chat\_history contains a large user query followed by a small assistant response, the reversed eviction loop processes the small assistant response, then hits the large user query. Because their sum \> 8000, it breaks, discarding all older context. It leaves *only* the small assistant response. The DT-P3-07 validator then strips this dangling assistant message. Result: The array goes to \[\].  
* **Proof:** Scenario Q trace. chat\_history \= \[User: 10001\], \[Assistant: 200\]. Loop keeps Assistant, breaks on User. truncated \= \[Assistant\]. Post-validator pops Assistant. History is wiped.  
* **Fix:** Use continue instead of break to skip oversized messages while continuing to salvage older valid history until the 8000-token budget is perfectly optimized.

Python

\# In backend/routes/chat.py  
        if running \+ msg\_tokens \> MAX\_CHAT\_HISTORY\_TOKENS and truncated:  
            continue  \# Skip oversized message instead of aborting the whole loop

### **FINDING-P4-06: Strict Server-Side JSON Validation Subverts Frontend Parser**

* **Dimension:** 1 (Phase 3 Code Review)  
* **Severity:** SIGNIFICANT  
* **Classification:** \[SUBTRACTIVE\]  
* **Description:** P3-12 adds strict json.loads(response) to validate LLM output. Instruct models frequently ignore system instructions and wrap valid JSON in markdown fences (\`\`\`json\\n...\\n\`\`\`). json.loads natively rejects this formatting. The backend intercepts it as an error and returns a generic PHASE\_ERROR. This actively subverts the V9 parseGusResponse frontend function, which was specifically engineered to forward-scan and extract JSON from markdown wrappers.  
* **Proof:** LLM outputs valid JSON inside a markdown block. json.loads throws JSONDecodeError. Backend discards valid diagnostic and returns fallback error.  
* **Fix:** Remove the entire try/except json.JSONDecodeError block introduced by P3-12. Allow the raw string to pass to the robust frontend parser.

---

## **RESIDUAL HIDDEN CODE RISK ASSESSMENT (Dimension 5\)**

1. **parseGusResponse(rawText)**: **LOW RISK**. Forward-scanning brute-force JSON extraction is highly resilient to model hallucinations. Even if the server passes oddly formatted strings, the brute-force nested object search reliably extracts DAG structures.  
2. **buildUserMessage(selectedOption, lastResponse)**: **LOW RISK**. It injects required\_next\_state cleanly. The backend system prompt strictly enforces this parameter as an "ABSOLUTE LAW".  
3. **load\_ledger()**: **LOW RISK**. Reading a \~3KB file from disk sequentially per request takes microseconds. A TOCTOU edit exactly during the read window is possible but negligible in a single-user desktop environment.  
4. **validate\_ledger.py**: **MEDIUM RISK**. It imports TOKENIZER via os.environ.get("TOKENIZER\_MODEL\_PATH"). If the validator script is run on the host (V9 heritage) but the model resides in ./storage/models, path desyncs from the container's /app/models could cause script failure, temporarily blinding the user to ledger size overflows.

---

## **VERDICTS**

**1\. AUDIT VERDICT:** **CONDITIONAL PASS**

**2\. REQUIRED FIXES:** Implementation of Findings P4-01 through P4-06 is required to achieve operability. Without them, the system guarantees pipeline crashes, total state loss, and the corruption of life-safety diagnostic terminology.

**3\. CONFIDENCE SCORES:**

* Dimension 1 (Phase 3 Code Review): **95%**  
* Dimension 2 (Fix Interaction Matrix): **100%**  
* Dimension 3 (Frontend State Machine): **100%**  
* Dimension 4 (Numerical Verification): **100%**  
* Dimension 5 (Residual Risk): **90%**  
* Dimension 6 (Docker Infra): **100%**

**4\. RESIDUAL RISK:**

The system relies exclusively on prompt-based coercion to output strict DAG JSON. Without programmatic generation control (like outlines or vLLM guided decoding), Qwen2.5-AWQ remains highly susceptible to "JSON drift" on long multi-turn diagnostics, where perplexity anomalies caused by 4-bit AWQ degradation might cause it to invent arbitrary keys that fail frontend parsing.

## **INTEGRITY CHECKLIST**

* \[x\] No finding overlaps with the 52 items in the cumulative fix changelog  
* \[x\] Every finding includes a concrete execution trace  
* \[x\] No \[SUBTRACTIVE\] finding without proof of breakage  
* \[x\] All scenario traces (P through T) complete with predicted outcomes  
* \[x\] At least one finding per dimension (or explicit dimension clearance)  
* \[x\] Budget math independently computed for all edge-case scenarios

