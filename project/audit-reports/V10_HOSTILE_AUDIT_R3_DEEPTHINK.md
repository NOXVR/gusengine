# **V10 HOSTILE ARCHITECTURE AUDIT — PHASE 3**

## **DIMENSION 4: NUMERICAL VERIFICATION (Complete Budget Math)**

All token calculations are strictly validated against the Qwen2.5-32B absolute context limit of **32,768 tokens**.

**Scenario 1: First Request (no history, no ledger)**

* max\_context: 32768  
* system\_prompt: 900  
* ledger: 0  
* response\_budget: 2000  
* chat\_history: 0  
* user\_query: 50  
* **available\_for\_RAG:** 32768 \- 900 \- 0 \- 2000 \- 0 \- 50 \= **29,818 tokens**  
* *Verification:* Valid. This provides a massive 29K context window for initial symptom RAG.

**Scenario 2: Typical mid-session request (ledger active, 10 turns)**

* max\_context: 32768  
* system\_prompt: 900  
* ledger: 2550 (max allowed by validator)  
* response\_budget: 2000  
* chat\_history: 5000  
* user\_query: 100  
* **available\_for\_RAG:** 32768 \- 900 \- 2550 \- 2000 \- 5000 \- 100 \= **22,218 tokens**  
* *Verification:* Valid. 22K tokens fits roughly 43 maximum-size Docling chunks (512 tokens each), providing rich cross-document reasoning.

**Scenario 3: Cap-triggering long session (ledger active, 20+ turns)**

* max\_context: 32768  
* system\_prompt: 900  
* ledger: 2550  
* response\_budget: 2000  
* chat\_history: 8000 (hard cap via physical eviction loop)  
* user\_query: 200  
* **available\_for\_RAG:** 32768 \- 900 \- 2550 \- 2000 \- 8000 \- 200 \= **19,118 tokens**  
* *Verification:* Valid. 19,118 stays well above the MIN\_RAG\_FLOOR of 5000\. Normal usage mathematically guarantees RAG capacity. *(Note: See Finding P3-03 for mathematical paradox when the user query is excessively large).*

*System Prompt Math Check:* The raw text of the V10 DAG State Machine consumes approximately 450 tokens. The budgeted 900 tokens provides a 100% safety margin.

---

## **SCENARIO TRACES (Phase 3 Edge Cases)**

**Scenario K: Eviction Edge Case — Single Massive Message**

* **Trace:** A single 9,000-token user message exists in chat\_history. The loop for msg in reversed(chat\_history) checks if running (0) \+ 9000 \> MAX\_CHAT\_HISTORY\_TOKENS (8000). This evaluates to True immediately. The loop breaks.  
* **Outcome:** truncated remains \[\]. The massive message is gracefully dropped, preventing a crash. The system successfully defends the budget, though at the cost of total history amnesia.

**Scenario L: build\_context Return Type Mismatch**

* **Trace:** build\_context returns a tuple. chat.py does not unpack it. The tuple is evaluated inside a Python f-string: f"\\n\\n{context}".  
* **Outcome:** **FATAL PROMPT CORRUPTION.** Python converts the tuple to a string, injecting raw dictionary structures directly into the LLM prompt. (See Finding P3-01).

**Scenario M: Concurrent Eviction \+ Token Counting**

* **Trace:** Two simultaneous async requests execute TOKENIZER.encode() synchronously.  
* **Outcome:** **SAFE.** HuggingFace's Rust-based tokenizers library releases the GIL and is fully thread-safe. While executing synchronously inside an async route blocks the FastAPI event loop for \~1-3ms, the single-user air-gapped prototype environment means this transient blocking is entirely harmless.

**Scenario N: Ingestion Semaphore Starvation**

* **Trace:** Semaphore \= 2\. PDF 1 (10 hr) and PDF 2 (30s) occupy the slots. PDF 2 finishes its Docling parsing.  
* **Outcome:** **NO STARVATION, BUT RESOURCE FLOOD.** PDF 2 releases the semaphore slot, allowing PDF 3 to enter. However, because the semaphore releases *before* the embedding loop, downstream HTTP port exhaustion occurs. (See Finding P3-04).

**Scenario O: LLM Returns Non-JSON**

* **Trace:** Qwen2.5 hallucinated a conversational prefix before the JSON.  
* **Outcome:** **GRACEFUL RECOVERY.** The V9 heritage parser parseGusResponse is documented as a "brute-force forward scanner." It hunts for the first { and last }, isolating the JSON payload and successfully discarding the hallucinated text.

---

## **AUDIT FINDINGS**

### **FINDING-P3-01: Context Tuple Injection (Prompt Corruption)**

* **Dimension:** 2 (End-to-End Data Flow Integrity)  
* **Severity:** CRITICAL  
* **Classification:** \[CORRECTIVE\]  
* **Description:** build\_context() correctly returns a tuple: \-\> tuple\[str, list\[dict\]\]. In chat.py, it is invoked as context \= build\_context(...). Because the tuple is not unpacked, the context variable holds the literal Python tuple. When injected via system\_content \+= f"\\n\\nRETRIEVED DOCUMENTS:\\n\\n{context}", Python natively stringifies it.  
* **Proof:** Trace Scenario L. The LLM receives: ('Header\\\\nText', \[{'text': 'Text', 'source': 'doc.pdf'}\]). This forces dictionary syntax into the prompt, duplicates the token footprint, and permanently breaks the "Zero-Retrieval Safeguard" because a tuple ("", \[\]) evaluates as truthy in if context:.  
* **Fix:** Unpack the tuple in chat.py:  
* Python

context\_string, used\_chunks \= build\_context(...)  
if context\_string:  
    system\_content \+= f"\\n\\nRETRIEVED DOCUMENTS:\\n\\n{context\_string}"

*   
* 

### **FINDING-P3-02: Qdrant Vector Collection Dead-on-Arrival**

* **Dimension:** 6 (Docker and Infrastructure Edge Cases)  
* **Severity:** CRITICAL  
* **Classification:** \[ADDITIVE\]  
* **Description:** qdrant\_setup.py provides create\_collection() which configures the critical dense/sparse hybrid search parameters. However, this function is **never called** anywhere in the system lifecycle.  
* **Proof:** A fresh docker-compose deployment spins up an empty Qdrant instance. When the V9 background daemon triggers /api/ingest, index\_chunk() executes client.upsert(collection\_name="fsm\_corpus", ...). Because fsm\_corpus does not exist, Qdrant throws an HTTP 404 (NotFoundError). Ingestion fails permanently.  
* **Fix:** Add FastAPI startup logic in chat.py or the clients.py singleton:  
* Python

from backend.indexing.qdrant\_setup import create\_collection  
if not qdrant\_client.collection\_exists("fsm\_corpus"):  
    create\_collection(qdrant\_client)

*   
* 

### **FINDING-P3-03: MIN\_RAG\_FLOOR Context Overflow Paradox**

* **Dimension:** 4 (Numerical Verification / Budget Math)  
* **Severity:** CRITICAL  
* **Classification:** \[CORRECTIVE\]  
* **Description:** Phase 1 introduced MIN\_RAG\_FLOOR \= 5000. If mathematical budget drops below 0, it artificially forces available \= 5000. However, it does this *without dynamically truncating* the variables that caused the deficit (e.g., user\_query), guaranteeing an out-of-memory crash.  
* **Proof:** User pastes a 25,000-token log dump.  
  1. available \= 32768 \- 900(sys) \- 2550(ledger) \- 2000(resp) \- 8000(chat) \- 25000(query) \= \-5682.  
  2. The code evaluates if available \< MIN\_RAG\_FLOOR: available \= 5000.  
  3. Context builder pulls 5000 tokens of chunks.  
  4. Prompt sent to vLLM \= 900 \+ 2550 \+ 8000 \+ 25000 \+ 5000 \= 41,450 tokens.  
  5. 41,450 \> 32,768 limit. vLLM crashes with HTTP 400 Bad Request.  
* **Fix:** Enforce a hard cap on user\_query\_tokens before RAG math is calculated:  
* Python

if user\_query\_tokens \> 10000:  
    return {"response": json.dumps({"current\_state": "PHASE\_ERROR", "mechanic\_instructions": "Query too long."})}

*   
* 

### **FINDING-P3-04: Sibling Directory Path Traversal Bypass**

* **Dimension:** 1 (Phase 2 Fix Code Review)  
* **Severity:** SIGNIFICANT  
* **Classification:** \[CORRECTIVE\]  
* **Description:** The path traversal mitigation uses .startswith() without a trailing slash. This permits attackers to escape the boundary by targeting sibling directories that share the exact string prefix.  
* **Proof:** ALLOWED\_PDF\_DIR \= "/app/pdfs". A webhook payload specifies: {"pdf\_path": "/app/pdfs\_keys/ssh\_key.pdf"}. os.path.realpath normalizes it safely. However, "/app/pdfs\_keys/ssh\_key.pdf".startswith("/app/pdfs") evaluates to **True**. The security check is bypassed.  
* **Fix:** Append a trailing slash: if not pdf\_path.startswith(ALLOWED\_PDF\_DIR \+ "/"):

### **FINDING-P3-05: Ingestion Semaphore Leak & TEI Socket Exhaustion**

* **Dimension:** 1 (Phase 2 Fix Code Review)  
* **Severity:** SIGNIFICANT  
* **Classification:** \[CORRECTIVE\]  
* **Description:** The INGEST\_SEMAPHORE (limit 2\) gates parse\_and\_chunk. Once parsing is complete, the task drops the lock and enters a loop to await embed\_text() for every chunk. Furthermore, embed\_text() instantiates a brand new httpx.AsyncClient() per chunk.  
* **Proof:** Trace Scenario N. 514 tasks queue up. Fast PDFs parse, drop the lock, and enter the embedding loop. Up to 512 background tasks will concurrently loop over thousands of chunks. The system rapidly creates and destroys tens of thousands of unpooled HTTP connections to TEI, causing ephemeral port exhaustion (TIME\_WAIT), TEI 503 timeouts, and a complete ingestion crash.  
* **Fix:** Expand the semaphore block to encompass the entire pipeline, and use a shared global httpx.AsyncClient for connection pooling.

### **FINDING-P3-06: DOMPurify ReferenceError Crashes Frontend**

* **Dimension:** 5 (Completeness of Shown Code)  
* **Severity:** SIGNIFICANT  
* **Classification:** \[ADDITIVE\]  
* **Description:** Phase 2 "DOMPurify Integration" adds DOMPurify.sanitize() throughout renderGusResponse(). However, the import is commented out (// import DOMPurify from 'dompurify';), and DOMPurify is never downloaded in the air-gap prep scripts.  
* **Proof:** On the first LLM response, the frontend evaluates DOMPurify.sanitize(gus.mechanic\_instructions). Because DOMPurify is undefined globally, the browser throws a ReferenceError, permanently crashing the React/UI thread.  
* **Fix:** Add npm pack dompurify to the Docker pre-download shell commands and add a \<script\> tag referencing it locally.

### **FINDING-P3-07: Chat Eviction Splinters Conversational Roles**

* **Dimension:** 1 (Phase 2 Fix Code Review)  
* **Severity:** MINOR  
* **Classification:** \[CORRECTIVE\]  
* **Description:** The eviction loop blindly truncates messages based strictly on cumulative tokens. If the loop cuts off precisely in the middle of a user/assistant pair, the oldest message in truncated might be {"role": "assistant"}.  
* **Proof:** vLLM using the Qwen2.5 chat template strictly expects history to begin with a user role after the system prompt. Passing a dangling assistant message as the first conversational turn can cause the template renderer to throw an error or the model to hallucinate text formats.  
* **Fix:** Add a role validator after truncation:  
* Python

if truncated and truncated\[0\]\["role"\] \== "assistant":  
    truncated.pop(0)

*   
* 

### **FINDING-P3-08: DAG Matrix Missing Error Recovery Rules**

* **Dimension:** 3 (DAG State Machine)  
* **Severity:** MINOR  
* **Classification:** \[CORRECTIVE\]  
* **Description:** The LLM system prompt lacks transition rules for navigating *out* of an error state.  
* **Proof:** After a PHASE\_ERROR, the user is prompted to try again. The LLM receives a chat\_history ending in an error state. The DAG rules dictate what to do in Phase A, B, C, D, but provide no mapping for error recovery. The LLM loses its determinism and behaves unpredictably.  
* **Fix:** Append this explicit recovery rule to the system prompt matrix:  
  \- After PHASE\_ERROR or RETRIEVAL\_FAILURE, if the user sends any new message, RESET to PHASE\_A\_TRIAGE.

---

## **VERDICTS**

**1\. VERDICT:** **CONDITIONAL PASS**

The architecture is fundamentally capable of local, air-gapped diagnostic reasoning. However, it will **100% crash on the first user action** due to the Tuple Injection bug (P3-01) and Uninitialized Vector Store (P3-02).

**2\. FIXES REQUIRED FOR PASS:**

* Unpack tuple\[str, list\[dict\]\] in chat.py. (Finding P3-01)  
* Add startup create\_collection() call for Qdrant. (Finding P3-02)  
* Enforce an upstream hard cap on user\_query tokens to stop math underflows. (Finding P3-03)  
* Expand semaphore bounds, apply trailing slashes, add DOMPurify, and apply DAG recovery rules (Findings P3-04 through P3-08).

**3\. CONFIDENCE SCORES:**

* Dimension 1 (Phase 2 Fix Logic): **95%**  
* Dimension 2 (Data Flow Integrity): **100%** (Tuple type mismatch objectively confirmed)  
* Dimension 3 (DAG State Completeness): **95%** (Dead-end error routing identified)  
* Dimension 4 (Token Math Verification): **100%** (Paradox of unbounded query mathematically proven)  
* Dimension 5 (Hidden Code Risk): **95%** (DOMPurify absence verified)  
* Dimension 6 (Infrastructure Edge Cases): **100%** (Zero-day empty container state verified)

**4\. RESIDUAL RISK:**

**Docling CPU Extraction Timelines:** While the semaphore protects host RAM, parse\_and\_chunk using EasyOCR on the CPU takes \~1-3 minutes *per page*. For a batch of 514 mechanical manuals (thousands of pages), ingestion will take literally weeks to run. The "20-60 hour" timeline noted in the spec is overly optimistic for degraded 1960s-era mechanical PDF scans. Without aggressive offline pre-caching on stronger hardware prior to air-gapping, initial ingestion is functionally unusable.

## **INTEGRITY CHECKLIST**

* \[X\] No finding overlaps with the 35 items in the cumulative fix changelog  
* \[X\] Every finding includes a concrete execution trace  
* \[X\] No \[SUBTRACTIVE\] finding without proof of breakage  
* \[X\] All 5 scenario traces complete with predicted outcomes  
* \[X\] At least one finding per dimension  
* \[X\] Token budget math independently computed for all 3 scenarios

