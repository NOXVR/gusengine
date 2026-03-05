# **V10 HOSTILE ARCHITECTURE AUDIT — PHASE 5**

## **CONVERGENCE ASSESSMENT (DIMENSION 5\)**

**VERDICT: CONDITIONAL PASS**

After 5 phases and 74 total findings, the GusEngine architecture exhibits **STRONG CONVERGENCE**.

* **Fix Generation Rate:** The volume of defects has dropped sharply (Phase 1: 20 → Phase 2: 15 → Phase 3: 17 → Phase 4: 15 → Phase 5: 7).  
* **Fix Depth Pattern:** We are no longer discovering foundational gaps (like missing healthchecks) or cross-component deadlocks. Phase 5 findings are exclusively **fourth-order fix-on-fix interactions**—brittle Python logic (regex anchors, loop continuation, exception hierarchies) introduced in Phase 4 that inadvertently bypassed earlier guards.  
* **System Stability:** The core topology (vLLM scaling, hybrid RAG chunking, DOMPurify/textContent isolation) has zero structural cracks.

The "fix-on-fix" bleeding is entirely isolated to Phase 4 control-flow patches and can be permanently cauterized using the 7 corrections below.

---

## **FINDINGS**

### **FINDING-P5-01: Eviction continue Destroys Role Alternation (Scenario U)**

* **Dimension:** 1 (Phase 4 Logic) & 2 (Fix Chain Integrity)  
* **Severity:** CRITICAL  
* **Classification:** \[CORRECTIVE\]  
* **Description:** DT-P4-05 changed the chat history eviction loop from break to continue to retain older, smaller messages. However, skipping oversized messages in the middle of a timeline destroys the strictly alternating user/assistant role sequence. Qwen2.5 and vLLM's ChatML template enforce this alternation. If an assistant message is skipped but the surrounding user messages fit the budget, the resulting array has consecutive user roles. Submitting this to vLLM triggers an immediate HTTP 400 Bad Request (TemplateError), permanently breaking the conversation.  
* **Proof:** Trace Scenario U: chat\_history \= \[{user: 100}, {assistant: 100}, {user: 100}, {assistant: 8000}, {user: 100}\]. Budget loop keeps {user: 100}. Evaluates {assistant: 8000}; 100+8000 \> 8000 \-\> continue (skips). Keeps {user: 100}, {assistant: 100}, {user: 100}. Resulting array: \[{user: 100}, {assistant: 100}, {user: 100}, {user: 100}\]. Back-to-back user messages crash the template.  
* **Fix:** Revert continue back to break to preserve contiguous chronological truncation.

Python

\# backend/routes/chat.py  
if running \+ msg\_tokens \> MAX\_CHAT\_HISTORY\_TOKENS and truncated:  
    break  \# Reverted from continue to preserve contiguous role alternation

### **FINDING-P5-02: Regex Anchors Sabotage JSON Extraction (Scenario V)**

* **Dimension:** 1 (Phase 4 Logic) & 3 (Frontend State Consistency)  
* **Severity:** CRITICAL  
* **Classification:** \[CORRECTIVE\]  
* **Description:** DT-P4-06 added regex to strip markdown fences: re.sub(r'^\`\`\`(?:json)?\\s\*\\n?', ...). The ^ anchor strictly requires the string to *start* with backticks. If the LLM generates any conversational prose before the code fence (e.g., "Here is the state:\\n\`\`\`json..."), the strip() method doesn't remove it, the ^ anchor fails, and the leading fence is retained. The trailing fence regex (\\n?\`\`\`\\s\*$) *does* succeed. The resulting string has an opening markdown fence but no closing fence, ensuring json.loads() fails with a JSONDecodeError, forcing an unrecoverable PHASE\_ERROR and preempting the frontend's legacy parsing fallback.  
* **Proof:** Trace Scenario V: LLM output "Response:\\n\`\`\`json\\n{\\"current\_state\\": \\"PHASE\_B\\"}\\n\`\`\`". re.sub for the start fails because the string starts with R. re.sub for the end successfully strips the trailing fence. stripped \= "Response:\\n\`\`\`json\\n{\\"current\_state\\": \\"PHASE\_B\\"}\\n". json.loads() crashes.  
* **Fix:** Abandon regex anchoring for brute-force JSON block extraction.

Python

\# backend/routes/chat.py  
import re  
match \= re.search(r'\\{.\*\\}', response.strip(), re.DOTALL)  
stripped \= match.group(0) if match else response.strip()

### **FINDING-P5-03: Dense Fallback Neutralizes the Zero-Retrieval Safeguard (Scenario W)**

* **Dimension:** 2 (Fix Chain Integrity) & 4 (Numerical Verification)  
* **Severity:** SIGNIFICANT  
* **Classification:** \[CORRECTIVE\]  
* **Description:** DT-P4-02 implements a dense-only fallback query if sparse prefetch fails. H05 enforces a hard min\_absolute\_score \= 0.013 to discard off-topic queries and trigger the ZERO-RETRIEVAL SAFEGUARD. This threshold is calibrated for Reciprocal Rank Fusion (where top ranks score \~0.016). In dense-only mode, scores are Cosine Similarities. Even a completely unrelated FSM chunk will typically yield a cosine score \> 0.3. Since 0.3 \> 0.013, the absolute floor check is trivially bypassed. Off-topic queries inject garbage context, preventing the safeguard from triggering and inducing hallucinations.  
* **Proof:** Trace Scenario W: Sparse search fails; dense-only fallback activates. User query "How to bake a cake" returns top cosine score 0.35 (irrelevant). 0.35 \< 0.013 evaluates to False. Floor check bypassed. Irrelevant chunk injected into context.  
* **Fix:** Dynamically adapt the absolute score threshold based on the active retrieval mode.

Python

\# backend/retrieval/search.py  
is\_fusion \= len(prefetch\_list) \>= 2  
absolute\_floor \= min\_absolute\_score if is\_fusion else 0.40  \# Cosine floor calibration  
if top\_score \< absolute\_floor:  
    return \[\]

### **FINDING-P5-04: Silent Complete Data Loss in Bulk Ingestion (Scenario X)**

* **Dimension:** 1 (Phase 4 Logic) & 6 (Docker/Infrastructure)  
* **Severity:** CRITICAL  
* **Classification:** \[CORRECTIVE\]  
* **Description:** P4-08 wrapped chunk embedding and indexing in a try/except: continue loop to prevent single OCR failures from aborting a PDF. However, if the TEI service or Qdrant container is down, *every single chunk* triggers the except block. The loop quietly exhausts, and the function logs "Indexed {len(chunks)} chunks" and returns len(chunks) (the number of *attempted* chunks). Because no IngestionError is raised, the background wrapper logs a successful run and never updates .ingest\_failures.log. The operator is blinded to the fact that 0 chunks were inserted.  
* **Proof:** Trace Scenario X: 200 chunks generated. TEI connection drops. Loop iteration 0: embed\_text() raises httpx.ConnectError. Caught by except Exception, executes continue. Repeats 200 times. Function logs "Indexed 200 chunks" and returns 200\. 0 chunks exist in Qdrant.  
* **Fix:** Track successfully indexed chunks, return the real count, and raise an IngestionError if the success count is 0\.

Python

\# backend/ingestion/pipeline.py  
    success\_count \= 0  
    for i, chunk in enumerate(chunks):  
        try:  
            \# ... embed and index ...  
            success\_count \+= 1  
        except Exception as e:  
            continue  
    if success\_count \== 0 and len(chunks) \> 0:  
        raise IngestionError("All chunks failed to index.")  
    return success\_count

### **FINDING-P5-05: Basename Extraction Flattens Subdirectory Mounts**

* **Dimension:** 1 (Phase 4 Logic) & 6 (Docker/Infrastructure)  
* **Severity:** MINOR  
* **Classification:** \[CORRECTIVE\]  
* **Description:** DT-P4-04 uses os.path.basename(body\["pdf\_path"\]) to cleanly strip absolute host paths from webhook payloads. However, this implicitly flattens the directory structure. If an operator categorizes manuals into subdirectories on the host (e.g., /home/user/storage/pdfs/engine/manual.pdf), basename extracts "manual.pdf". The script resolves this to /app/pdfs/manual.pdf, which does not exist because the Docker volume mount preserves the host's subdirectories (/app/pdfs/engine/manual.pdf). Ingestion permanently fails with FileNotFoundError.  
* **Proof:** Webhook payload pdf\_path: "/home/user/storage/pdfs/engine/manual.pdf". basename \-\> "manual.pdf". Container attempts to read /app/pdfs/manual.pdf \-\> FileNotFoundError.  
* **Fix:** Extract the relative path dynamically using the known volume mount boundary (pdfs/).

Python

\# backend/routes/ingest.py  
    raw\_path \= body\["pdf\_path"\]  
    rel\_path \= raw\_path.split("pdfs/", 1)\[-1\] if "pdfs/" in raw\_path else os.path.basename(raw\_path)  
    pdf\_path \= os.path.realpath(os.path.join(ALLOWED\_PDF\_DIR, rel\_path))

### **FINDING-P5-06: Tokenizer SystemExit Crashing Host Validator**

* **Dimension:** 2 (Fix Chain Integrity)  
* **Severity:** SIGNIFICANT  
* **Classification:** \[CORRECTIVE\]  
* **Description:** P4-11 added a directory check in backend/shared/tokenizer.py that executes raise SystemExit(...) if /app/models/... does not exist. P4-09 designed validate\_ledger.py to use try: ... except ImportError: to fall back to a local model path when executed on the host OS. Because SystemExit inherits from BaseException (not Exception), it bypasses the except ImportError block. The validator crashes instantly on the host OS before the fallback can trigger.  
* **Proof:** Operator runs python validate\_ledger.py on host. try block evaluates import backend.shared.tokenizer. tokenizer.py evaluates os.path.isdir("/app/models/...") \-\> False. raise SystemExit fires. Interpreter immediately stops. Local fallback is dead code.  
* **Fix:** Raise RuntimeError instead of SystemExit.

Python

\# backend/shared/tokenizer.py  
if not os.path.isdir(\_MODEL\_PATH):  
    raise RuntimeError(f"Fatal: tokenizer directory not found at {\_MODEL\_PATH}")

### **FINDING-P5-07: Orphan Assistant Guard \+ Truncation Poisons Context**

* **Dimension:** 2 (Fix Chain Integrity)  
* **Severity:** SIGNIFICANT  
* **Classification:** \[SUBTRACTIVE\]  
* **Description:** P4-03 prevents stripping an orphaned assistant message if len(truncated) \== 1. P4-02 then hard-truncates this single oversized message using TOKENIZER.decode(tokens\[:8000\]). If an oversized assistant message is the only thing left in the history, these two fixes combine to inject an assistant role immediately following the system prompt (violating ChatML role alternating expectations) containing sliced, fundamentally invalid JSON. The LLM will heavily penalize its own broken history context, inducing massive hallucination.  
* **Proof:** Eviction leaves truncated \= \[{assistant: 9000}\]. P4-03 keeps it. P4-02 decodes and slices the string at 8000 tokens mid-JSON block. Prompt assembly pushes system \-\> assistant(broken JSON) \-\> user. LLM generation fails or outputs invalid format.  
* **Fix:** An empty history array is perfectly safe (it acts as a DAG reset). Remove the len \> 1 guard and always strip an orphaned assistant message. Remove P4-02 hard truncation entirely.

Python

\# backend/routes/chat.py  
\# \[SUBTRACTIVE\] Remove the P4-03 len(truncated) \> 1 guard  
if truncated and truncated\[0\]\["role"\] \== "assistant":  
    chat\_history\_tokens\_removed \= len(TOKENIZER.encode(truncated\[0\]\["content"\]))  
    truncated.pop(0)  
    running \-= chat\_history\_tokens\_removed

---

## **VERDICTS**

1. **FINAL VERDICT:** **CONDITIONAL PASS**  
2. **EXACT FIXES REQUIRED:** Apply the 7 specific code patches detailed in Findings P5-01 through P5-07.  
3. **CONFIDENCE SCORES:**  
   * **Dimension 1 (P4 Code Review):** 100%  
   * **Dimension 2 (Fix Chain Integrity):** 95%  
   * **Dimension 3 (Frontend State Consistency):** 100% *(Note: P4-04's use of .textContent is VERIFIED SAFE. It successfully neutralizes XSS while preserving \<B+\>/\<12V\> FSM terminal tags, unlike DOMPurify which stripped them).*  
   * **Dimension 4 (Numerical/Math):** 100%  
   * **Dimension 5 (Convergence Assessment):** 95%  
   * **Dimension 6 (Infrastructure):** 90%  
4. **RESIDUAL RISK:**  
   * **Asyncio Event Loop Starvation:** Concurrent bulk ingestion processing (CPU-bound Docling threading) scaling against active web requests may cause ASGI healthchecks to timeout, triggering Docker container cycling.  
   * **vLLM PagedAttention Fragmentation:** Sustained 32K context continuous inference over 48+ hours of uptime may fragment the KV cache on RTX 4090 consumer cards, necessitating scheduled cron restarts.  
   * **httpx Ephemeral Port Exhaustion:** Even with a persistent connection pool, unclosed async sockets during massive Qdrant batch insert failures could exhaust the host's TIME\_WAIT limit.

## **INTEGRITY CHECKLIST**

* \[x\] No finding overlaps with the 67 items in the cumulative fix changelog  
* \[x\] Every finding includes a concrete execution trace  
* \[x\] No \[SUBTRACTIVE\] finding without proof of breakage (P5-07 includes concrete trace)  
* \[x\] All scenario traces (U through X) complete with predicted outcomes  
* \[x\] At least one finding per dimension (Dimension 3 cleared explicitly)  
* \[x\] Budget math independently computed for all edge-case scenarios  
* \[x\] Convergence assessment in Dimension 5 includes a quantitative verdict

