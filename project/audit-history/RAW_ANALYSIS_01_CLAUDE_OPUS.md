# V9 TARGETED HOSTILE AUDIT — COMPREHENSIVE RESULTS

**Date:** 2026-02-16
**Auditor:** Claude Opus 4.6 (Hostile Auditor Mode)
**Document Under Audit:** ARCHITECTURE_FINAL_V9.md
**Engineering Standard:** ZERO TOLERANCE

---

## INTEGRITY VERIFICATION

| Check | Expected | Actual | Status |
|:------|:---------|:-------|:-------|
| SHA-256 | B291D6CC1F447246ADD8D251CA2B457E2E27C0AEE91E95BA990C6177C09E399F | b291d6cc1f447246add8d251ca2b457e2e27c0aee91e95ba990c6177c09e399f | **✅ MATCH** |
| Lines | 1936 | 1936 (wc reports 1937 with trailing newline) | **✅ MATCH** |
| Bytes | 111904 | 111904 | **✅ MATCH** |
| Files loaded | 7 | 7 | **✅ ALL PRESENT** |

---

## SECTION 1: ITEM-BY-ITEM FINDINGS (20 Items)

### R-1: "DO NOT TRUST THE USER'S ASSUMPTIONS"

| Field | Value |
|:------|:------|
| **Verdict** | **PASS** |
| **V9 Line** | 1276 |
| **Content** | `YOU DO NOT TRUST THE USER'S ASSUMPTIONS.` inserted between `YOU DO NOT CONVERSE FREELY.` and `YOU ONLY OUTPUT STRICT JSON MATCHING THE SCHEMA BELOW.` |
| **VFINAL Match** | Verbatim match to VFINAL Part 2, line 15 |
| **V8 Damage** | None. V8 line 1207 had the two clauses on one line; V9 inserts the new clause between them. Surrounding content intact. |
| **Markdown Structure** | Inside `text` code fence (opens line 1274, closes line 1331). Correct. |

---

### R-2: DIAGNOSTIC FUNNEL

| Field | Value |
|:------|:------|
| **Verdict** | **PASS** |
| **V9 Lines** | 1291–1292 |
| **Content** | `THE DIAGNOSTIC FUNNEL (ANSWER-PATH PROMPTING):` block — "never jump to conclusion", "no open-ended questions", "YOU MUST PROVIDE THE ANSWERS" |
| **Location** | After EPISTEMOLOGICAL OVERRIDE rule 4 (line 1289), before DAG STATE TRANSITION MATRIX (line 1294). Correct. |
| **VFINAL Match** | Verbatim match to VFINAL Part 2, lines 23–24 |
| **V8 Damage** | None. V8 had no content between EPISTEMOLOGICAL OVERRIDE rule 4 and DAG MATRIX. V9 inserts cleanly. |
| **Markdown Structure** | Inside system prompt `text` code fence. Correct. |

---

### R-3: PHASE_D Reset-to-PHASE_A

| Field | Value |
|:------|:------|
| **Verdict** | **PASS** |
| **V9 Line** | 1299 |
| **Content** | `- After PHASE_D, if the user sends any new message, RESET to PHASE_A_TRIAGE for the new symptom.` |
| **VFINAL Match** | PASS-ADAPTED: VFINAL line 35 says `PHASE_A`, V9 uses `PHASE_A_TRIAGE` (V9 full state identifier convention). Intentional adaptation documented in FIDELITY_AUDIT_MASTER. |
| **V8 Damage** | None. Inserted after V8's PHASE_D transition rule (V8 line 1226). |
| **Markdown Structure** | Inside system prompt `text` code fence. Correct. |

---

### R-4: STATE TRANSITION RULES + ENFORCEMENT

| Field | Value |
|:------|:------|
| **Verdict** | **PASS** |
| **V9 Lines** | 1302–1310 |
| **Content** | `STATE TRANSITION RULES:` block (2–5 mutually exclusive options, PHASE_D completion rules) + `STATE TRANSITION ENFORCEMENT:` block (completed_state/required_next_state handling, PHASE_ERROR fallback) |
| **VFINAL Match** | Verbatim match to VFINAL Part 2, lines 32–41 |
| **V8 Damage** | None. Inserted after DAG MATRIX section, before ZERO-RETRIEVAL SAFEGUARD. |
| **Markdown Structure** | Inside system prompt `text` code fence. Correct. |

---

### R-5: Torn-Copy Rationale

| Field | Value |
|:------|:------|
| **Verdict** | **PASS** |
| **V9 Lines** | 1390–1391 |
| **Content** | `The container is stopped before backup to prevent torn copies of LanceDB/SQLite databases. Downtime is ~2-5 minutes at 2 AM.` prepended to existing V8 callout. |
| **VFINAL Match** | Core clause matches VFINAL Part 2, lines 208–209. V8 operational details (/usr/bin/docker, semicolons) retained. PASS-ADAPTED per fidelity audit. |
| **V8 Damage** | None. V8 line 1307 callout text preserved after the prepended rationale. |
| **Markdown Structure** | Inside `> [!IMPORTANT]` callout. Correct. |

---

### R-6: "Previous Steps" Self-Containment Fix

| Field | Value |
|:------|:------|
| **Verdict** | **PASS** |
| **V9 Lines** | 1383–1384 |
| **Content** | `> [!NOTE]` callout replacing V8 line 1300's `*(Deploy remaining skills from previous steps...)*` with explicit Appendix A reference and accurate skill descriptions. |
| **V8 Change** | V8 line 1300 text DELETED (intentional, per changelog). Replaced with self-contained NOTE. |
| **Accuracy** | NOTE correctly states: skills do NOT require `$INTERNAL_KEY`, use quoted heredocs, and directs to Settings → Agent Skills. Matches actual Appendix A content. |
| **Markdown Structure** | Inside `> [!NOTE]` callout. Correct. |

---

### I-1: `preprocess_markdown_tables()` Restored

| Field | Value |
|:------|:------|
| **Verdict** | **PASS** |
| **V9 Lines** | Function: 763–791. Call site: 822–831. Import: 745 (`re` added). |
| **Content** | 30-line function splitting oversized tables at `max_rows=20` with header re-injection. 7-line conditional call block for `.md` files. |
| **VFINAL Match** | All logic character-identical to VFINAL Part 2, lines 391–416. Docstring expanded with V9 RECOVERY attribution. PASS-ADAPTED. |
| **CF-1 Annotation** | Lines 824–826: 3-line comment explaining the call site is dormant (glob targets *.pdf only). Correctly annotated. |
| **V8 Damage** | V8 line 745 `import os, sys, time, requests, glob` → V9 adds `, re`. No other V8 content damaged. Upload loop at line 820 (`print(f"Uploading: {filename}")`) intact from V8 line 790. |
| **Markdown Structure** | Inside `sync_ingest.py` Python code block. Correct. |

---

### I-2: `MIN_RAG_BUDGET` Floor Check Restored

| Field | Value |
|:------|:------|
| **Verdict** | **PASS** |
| **V9 Lines** | Constant: 975. Print label: 988. Floor check: 994–997. |
| **Content** | `MIN_RAG_BUDGET = 2000` constant with attribution comment. Floor check: `if remaining < MIN_RAG_BUDGET:` → warning + action guidance + `return False`. |
| **VFINAL Match** | Constant value (2000) identical. Variable name adapted (`remaining` vs VFINAL's `rag_budget`). System prompt token constant updated per CF-4. PASS-ADAPTED. |
| **CF-4 Update** | Line 983: `remaining = 4000 - 750 - count`. Matches Phase 7 checklist (750). |
| **V8 Damage** | V8 line 935: `remaining = 4000 - 600 - count` → V9: `4000 - 750 - count` (explicit CF-4 change). V8 `print` block and `if count > ADJUSTED_CAP` logic intact. V8 `APPROVED`/`return True` and `__main__` block intact. |
| **Markdown Structure** | Inside `validate_ledger.py` Python code block (opens line 955, closes line 1008). Correct. |

---

### I-3: @VIN-Lookup Agent Skill

| Field | Value |
|:------|:------|
| **Verdict** | **PASS** (with security finding — see Audit G) |
| **V9 Lines** | 1589–1624 |
| **Content** | `plugin.json` + `handler.js` with quoted heredoc (`cat << 'EOF'`), `mkdir -p`, `docker restart`. |
| **VFINAL Match** | Character-identical to VFINAL Part 2, lines 83–111. V9 adds `mkdir -p` directory creation (safety improvement over VFINAL). |
| **API Key** | NO `$INTERNAL_KEY`, NO `sed`, NO `REPLACE_ME_KEY`. Calls public NHTSA API only. Correct. |
| **Markdown Structure** | Inside Appendix A bash code block. Correct. |

---

### I-4: @Purchase-Router Agent Skill

| Field | Value |
|:------|:------|
| **Verdict** | **PASS** |
| **V9 Lines** | 1628–1656 |
| **Content** | `plugin.json` + `handler.js`. Uses `encodeURIComponent()` for search query. |
| **VFINAL Match** | Character-identical to VFINAL Part 2, lines 149–170. |
| **API Key** | None required. Correct. |
| **Markdown Structure** | Inside Appendix A bash code block. Correct. |

---

### I-5: @Draft-Tribal-Knowledge Agent Skill

| Field | Value |
|:------|:------|
| **Verdict** | **PASS** |
| **V9 Lines** | 1660–1687 |
| **Content** | `plugin.json` + `handler.js`. Formats fixes into FAULT SIGNATURE structure. |
| **VFINAL Match** | Character-identical to VFINAL Part 2, lines 172–192. |
| **API Key** | None required. Correct. |
| **Markdown Structure** | Inside Appendix A bash code block. Correct. |

---

### D-1: `renderGusResponse()` Reference Implementation

| Field | Value |
|:------|:------|
| **Verdict** | **PASS** |
| **V9 Lines** | 1707–1781 |
| **Content** | 66-line UI rendering function with error handling, state badge, mechanic instructions, citation bubbles, answer-path buttons, text input control, completion state. |
| **VFINAL Match** | Character-perfect copy of VFINAL Part 2, lines 281–346. |
| **CF-3 XSS Warning** | Present at lines 1704–1705 before the code block. Documents innerHTML risk and mandates DOMPurify/.textContent. Correct. |
| **Markdown Structure** | Inside Appendix B JavaScript code block. Correct. |

---

### D-2: `sendToAnythingLLM()` Reference Implementation

| Field | Value |
|:------|:------|
| **Verdict** | **PASS** |
| **V9 Lines** | 1795–1819 |
| **Content** | 20-line async function with fetch, Authorization header, JSON parsing, re-render. |
| **VFINAL Match** | Character-perfect copy of VFINAL Part 2, lines 348–371. |
| **Warning** | `> [!WARNING]` at lines 1792–1793 about placeholder replacement. Correct. |
| **Markdown Structure** | Inside Appendix B JavaScript code block. Correct. |

---

### D-3: CSS Class Specification

| Field | Value |
|:------|:------|
| **Verdict** | **PASS** |
| **V9 Lines** | 1824–1849 |
| **Content** | 8 CSS classes + 2 DOM IDs in two tables. |
| **Accuracy** | All class names and element types verified against D-1 code: `gus-error`, `gus-state-badge`, `gus-instructions`, `gus-citations`, `gus-citation-bubble`, `gus-buttons`, `gus-answer-btn`, `gus-complete`, `gus-container`, `symptom-input`. All correct. |
| **Markdown Structure** | Markdown tables in Appendix B. Correct. |

---

### D-4: Archive Ledger Lifecycle NOTE

| Field | Value |
|:------|:------|
| **Verdict** | **PASS** |
| **V9 Lines** | 1010–1011 |
| **Content** | `> [!NOTE]` documenting `MASTER_LEDGER_ARCHIVE.md` concept: non-pinned, vector-searchable, does not consume pinned context budget. |
| **CF-2 Fix Verified** | Python code block closes at line 1008 (`\`\`\``). NOTE starts at line 1010. D-4 is OUTSIDE the code block. CF-2 fix confirmed. |
| **V8 Damage** | None. V8 had no content between the code block close and "Run with:" at V8 line 957. V9 inserts the NOTE cleanly between them (V9 line 1013: "**Run with:**"). |
| **Markdown Structure** | `> [!NOTE]` callout between code blocks. Correct. |

---

### D-5: API Key Insertion Guide

| Field | Value |
|:------|:------|
| **Verdict** | **PASS** |
| **V9 Lines** | 1225–1235 |
| **Content** | `> [!IMPORTANT]` callout with 4-row table: Anthropic, Voyage AI, Mistral, Cohere. Each with UI navigation path and key description. |
| **VFINAL Match** | Navigation paths match VFINAL Part 1, lines 404–412 (Settings → AI Providers → Anthropic, Settings → Embedding Preference → Voyage AI, Settings → Document Handling → Mistral OCR, Settings → AI Providers → Reranking → Cohere). All 4 providers and model identifiers correct. |
| **V8 Damage** | None. Inserted between V8 item 4 (Mistral OCR, line 1221) and V8 item 5 (Reranking, V9 line 1239). V8 content above and below intact. |
| **Markdown Structure** | `> [!IMPORTANT]` callout in Phase 7 section. Correct. |

---

### CF-1: Dead Code Annotation

| Field | Value |
|:------|:------|
| **Verdict** | **PASS** |
| **V9 Lines** | 824–826 |
| **Content** | 3-line comment: `# NOTE: Currently dormant — the glob at line 812 targets *.pdf only. / # This branch will activate if .md files are added to extracted_manuals/ / # or if the glob is expanded to include *.md files in a future version.` |
| **Accuracy** | Line 812 glob: `glob.glob(os.path.join(CHUNKS_DIR, "*.pdf"))` — correctly identified as PDF-only. Annotation is factually accurate. |

---

### CF-2: D-4 NOTE Moved Outside Code Block

| Field | Value |
|:------|:------|
| **Verdict** | **PASS** |
| **Evidence** | Python code block: opens line 955, closes line 1008. D-4 NOTE: starts line 1010. No markdown callouts inside the Python block. `validate_ledger.py` is structurally intact: `return False` (line 997) → `print("APPROVED.")` (line 998) → `return True` (line 999) — no interruptions. |

---

### CF-3: XSS WARNING Added

| Field | Value |
|:------|:------|
| **Verdict** | **PASS** |
| **V9 Lines** | 1704–1705 |
| **Content** | `> [!WARNING]` callout before `renderGusResponse()` code block. Documents `.innerHTML` XSS risk, identifies `gus.mechanic_instructions` and `gus.current_state` as LLM-controlled data sources, mandates DOMPurify or `.textContent` for custom deployments. Notes that deployed system uses AnythingLLM's built-in UI (which handles its own sanitization). |
| **Completeness** | All innerHTML interpolation sites documented. Risk mitigation guidance provided. |

---

### CF-4: Token Budget Updated

| Field | Value |
|:------|:------|
| **Verdict** | **PASS** |
| **Changes Verified** | (1) `validate_ledger.py` line 983: `remaining = 4000 - 750 - count` ✅ (2) Phase 7 checklist line 1253: `~750 tokens` ✅ (3) Phase 7 TOTAL: `~3625 tokens` ✅ (4) Phase 7 Response Budget: `~375 tokens` ✅ |
| **Internal Consistency** | All four values are mutually consistent: 750 + 1275 + 1600 = 3625. 4000 - 3625 = 375. |

---

## SECTION 2: CROSS-CUTTING FINDINGS

### AUDIT A: TOKEN BUDGET MATHEMATICAL PROOF

**Verdict: PASS with OBSERVATION**

**Character-based token estimation:**

| Metric | V8 | V9 | Delta |
|:-------|:---|:---|:------|
| System prompt chars | 3,066 | 4,070 | +1,004 |
| System prompt words | 406 | 547 | +141 |
| Claimed tokens | ~600 | ~750 | +150 |

**Estimation method:** V8 was validated at ~600 tokens for 3,066 characters (ratio: 5.1 chars/token). Applying the same ratio to V9: 4,070 / 5.1 ≈ **798 tokens**.

**Budget proof with claimed 750:**

```
750 (prompt) + 1275 (max ledger) + 1600 (4 × 400 RAG) = 3625
4000 - 3625 = 375 remaining
Gus JSON ~200 tokens → 175 safety margin ✓
```

**Budget proof with estimated 800:**

```
800 (prompt) + 1275 (max ledger) + 1600 (4 × 400 RAG) = 3675
4000 - 3675 = 325 remaining
Gus JSON ~200 tokens → 125 safety margin (tighter but viable)
```

**MIN_RAG_BUDGET floor check verification:**

At max ledger (1275): `remaining = 4000 - 750 - 1275 = 1975`. Since `1975 < 2000` (MIN_RAG_BUDGET), the floor check triggers correctly, prints warning, and returns `False`. ✅

With estimated 800-token prompt: actual remaining = `4000 - 800 - 1275 = 1925`. The code computes 1975 (using 750), which still triggers the floor check. The floor check is conservative — it fires at a *higher* remaining value than reality, which is the safe direction. ✅

**OBSERVATION F-TOK-1:** The ~750 token claim is likely ~50 tokens low based on character ratio analysis. The budget proof holds in both scenarios, but the safety margin narrows from 175 to ~125 tokens. The Phase 7 checklist correctly instructs the operator to verify via `docker logs` post-deployment. This is not a blocking finding because (a) the "~750" notation acknowledges approximation, (b) the 15% safety margin on the ledger cap already absorbs tokenizer variance, and (c) the MIN_RAG_BUDGET floor check fails safe.

---

### AUDIT B: STATE MACHINE CONSISTENCY

**Verdict: PASS**

**End-to-end trace:**

| Step | Action | V9 Evidence |
|:-----|:-------|:------------|
| 1 | User types "Hot start vapor lock" | System prompt line 1295: symptom → PHASE_A_TRIAGE, requires_input: true |
| 2 | User clicks answer button | `buildUserMessage` (line 1460) fires. `currentState="PHASE_A_TRIAGE"` → `next="PHASE_B_FUNNEL"`. Sends `required_next_state: "PHASE_B_FUNNEL"`. ✅ |
| 3 | LLM receives required_next_state | System prompt line 1307–1310: "MUST set current_state to value of required_next_state." ✅ |
| 4 | LLM loops in PHASE_B | `buildUserMessage` line 1480–1486: PHASE_B sends `required_next_state: null`. System prompt line 1297: "MAY loop" for further isolation. ✅ |
| 5 | LLM advances to PHASE_C | System prompt line 1297: "MUST advance to PHASE_C_TESTING when isolated." ✅ |
| 6 | User confirms → PHASE_D | `buildUserMessage` line 1489: `next="PHASE_D_CONCLUSION"`. System prompt line 1298: requires_input=false. ✅ |
| 7 | PHASE_D: no buttons rendered | `renderGusResponse` line 1754: `if (gus.requires_input && gus.answer_path_prompts.length > 0)` — false. Falls to else block (line 1772–1780). Text input re-enabled. `buildUserMessage()` NOT called. ✅ |
| 8 | User types new symptom | Free text submitted as new message. System prompt R-3 (line 1299): "RESET to PHASE_A_TRIAGE for the new symptom." ✅ |

**nextStates fallback analysis:** `nextStates[currentState] || "PHASE_D_CONCLUSION"` (line 1473). Fires for any state not in the map (PHASE_A, PHASE_B, PHASE_C, PHASE_ERROR are mapped). An unrecognized state would conclude the diagnostic gracefully. RETRIEVAL_FAILURE is correctly excluded — `requires_input: false` means no buttons, so `buildUserMessage` is never called. ✅

**R-2 vs PHASE_B looping conflict check:** R-2 says "never jump to a conclusion." R-4 says 2–5 mutually exclusive options. System prompt line 1297 says "MAY loop...MUST advance when isolated." These are complementary, not contradictory: R-2 prevents premature PHASE_D; PHASE_B looping ensures thorough isolation; R-4 constrains the option cardinality. No conflict. ✅

---

### AUDIT C: AGENT SKILL PATTERN CONSISTENCY

**Verdict: PASS (with security finding F-SEC-1 for VIN-Lookup)**

| Check | Manual-Status | VIN-Lookup | Purchase-Router | Draft-Tribal |
|:------|:-------------|:-----------|:----------------|:-------------|
| Quoted heredoc `'EOF'` | ✅ Lines 1354, 1362 | ✅ Lines 1596, 1607 | ✅ Lines 1635, 1646 | ✅ Lines 1667, 1678 |
| `mkdir -p` | ✅ Line 1352 | ✅ Line 1594 | ✅ Line 1633 | ✅ Line 1665 |
| `docker restart` | ✅ Line 1379 | ✅ Line 1623 | ✅ Line 1655 | ✅ Line 1686 |
| Uses `$INTERNAL_KEY` | ✅ (lines 1344, 1378) | ❌ (correct) | ❌ (correct) | ❌ (correct) |
| Uses `sed`/`REPLACE_ME_KEY` | ✅ (line 1378) | ❌ (correct) | ❌ (correct) | ❌ (correct) |

**R-6 NOTE (line 1383–1384):** Accurately states 3 skills in Appendix A, no `$INTERNAL_KEY` required, quoted heredocs, `mkdir -p`, `docker restart`, toggle ON in Settings. ✅

**VIN-Lookup input sanitization (F-SEC-1):**
- Line 1610: `if (!vin || vin.length < 5) return "Error: Invalid VIN.";` — blocks empty/short inputs
- Line 1611: `if (vin.length < 17)` — routes to classic chassis message
- Line 1613: `fetch(\`https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/${vin}?format=json\`)` — **`vin` is NOT URL-encoded before interpolation**
- A 17+ character string containing `#`, `?`, `&`, `/`, or URL-encoded payloads would pass the length check and corrupt the request URL
- Real VINs are alphanumeric only, so exploitation risk is low in practice, but the code lacks defense-in-depth
- **Compare:** Purchase-Router (line 1649) correctly uses `encodeURIComponent()` for its URL parameter

---

### AUDIT D: CODE BLOCK INTEGRITY

**Verdict: PASS**

| Code Block | Opens | Closes | Callouts Inside? | Status |
|:-----------|:------|:-------|:-----------------|:-------|
| `validate_ledger.py` | Line 955 | Line 1008 | None (D-4 NOTE at line 1010 is OUTSIDE) | ✅ |
| `sync_ingest.py` | Line 738 | ~Line 868 | None. `preprocess_markdown_tables()` correctly inside at 763–791. CF-1 annotation at 824–826 is a code comment, not a markdown callout. | ✅ |
| System prompt `text` block | Line 1274 | Line 1331 | None. R-1 through R-4 all inside. | ✅ |
| Manual-Status bash block | Line 1342 | Line 1381 | None | ✅ |
| VIN-Lookup bash block | Line 1593 | Line 1624 | None | ✅ |
| Purchase-Router bash block | Line 1632 | Line 1656 | None | ✅ |
| Draft-Tribal-Knowledge bash block | Line 1664 | Line 1687 | None | ✅ |
| `renderGusResponse()` JS block | Line 1707 | Line 1782 | None | ✅ |
| `sendToAnythingLLM()` JS block | Line 1795 | Line 1820 | None | ✅ |

Every opening ` ``` ` has a matching closing ` ``` `. No markdown callouts appear inside any fenced code block. No V9-added content breaks any V8 code block.

---

### AUDIT E: V8 REGRESSION CHECK

**Verdict: PASS**

| Modification Site | V8 Lines Above | V8 Lines Below | Damage? |
|:-----------------|:---------------|:---------------|:--------|
| R-1 (line 1276) | V8 1206: `PRIME DIRECTIVE...` ✅ | V8 1207 remainder: `YOU ONLY OUTPUT STRICT JSON...` ✅ | None |
| R-2 (lines 1291–1292) | V8 1220: Rule 4 (MASTER_LEDGER truth) ✅ | V8 1222: DAG STATE TRANSITION ✅ | None |
| R-3 (line 1299) | V8 1226: PHASE_D rule ✅ | V8 1227: required_next_state rule ✅ | None |
| R-4 (lines 1302–1310) | V8 1227: required_next_state rule ✅ | V8 1229: ZERO-RETRIEVAL SAFEGUARD ✅ | None |
| R-5 (lines 1390–1391) | V8 1306: `> [!IMPORTANT]` tag ✅ | V8 1307 remainder (path/semicolon text) ✅ | None (text prepended, not replaced) |
| R-6 (lines 1383–1384) | V8 1298: closing ` ``` ` ✅ | V8 1302: Phase 10 heading ✅ | V8 line 1300 DELETED (intentional) |
| I-1 func (lines 763–791) | V8 761: `CHUNKS_DIR = ...` ✅ | V8 763: dedup query block ✅ | None (content shifted down) |
| I-1 call (lines 822–831) | V8 790: `print(f"Uploading...")` ✅ | V8 791: `with open(chunk_path, 'rb')...` ✅ | None |
| I-1 import (line 745) | V8 745: `import os, sys, time, requests, glob` | V9: adds `, re` | Expected addition |
| I-2 constant (line 975) | V8 927: `ADJUSTED_CAP = ...` ✅ | V8 929: `def validate(path):` ✅ | None |
| I-2 floor check (lines 994–997) | V8 942–943: `if count > ADJUSTED_CAP` block ✅ | V8 945: `print("APPROVED.")` ✅ | None |
| I-2 formula (line 983) | V8 935: same line position | V9: `750` replaces `600` | Explicit CF-4 change |
| D-4 (lines 1010–1011) | V8 955: closing ` ``` ` ✅ | V8 957: "**Run with:**" ✅ | None |
| D-5 (lines 1225–1235) | V8 1167: Item 4 (Mistral OCR) ✅ | V8 1170: Item 5 (Reranking) ✅ | None |
| I-3 (lines 1589–1624) | V8 had nothing here (new appendix) | V8 diff table follows at 1852 ✅ | None |
| I-4 (lines 1628–1656) | After I-3 in new appendix | N/A | None |
| I-5 (lines 1660–1687) | After I-4 in new appendix | N/A | None |
| D-1 (lines 1707–1781) | New Appendix B section | N/A | None |
| D-2 (lines 1795–1819) | After D-1 in Appendix B | N/A | None |
| D-3 (lines 1824–1849) | After D-2 in Appendix B | V8 diff table at 1852 ✅ | None |

**Total V8 lines checked:** ~200 context lines across 20 modification sites.
**V8 damages found:** 0 (beyond the 2 explicitly documented changes: R-6 text replacement, CF-4 formula update).

---

### AUDIT F: DNA CROSS-REFERENCE

**Verdict: FAIL (1 critical inconsistency)**

| V9 Item | DNA Reference | Match? | Notes |
|:--------|:-------------|:-------|:------|
| R-1 (trust assumptions) | DNA line 28: Gus "does not hallucinate, does not guess" | ✅ | Consistent with epistemological philosophy |
| R-2 (diagnostic funnel) | DNA line 259: "2-5 mutually exclusive options required" | ✅ | Funnel methodology consistent |
| R-3 (PHASE_D reset) | DNA line 237: "User sends new message after PHASE_D → PHASE_A_TRIAGE (reset)" | ✅ | Exact match |
| R-4 (state transitions) | DNA lines 229–238: State transition rules table | ✅ | All states and transitions match |
| R-5 (torn-copy) | DNA line 215: "Gating exists" + archival concept | ✅ | Consistent |
| R-6 (Appendix A ref) | DNA line 299: "defined in Appendix A" + quoted heredocs | ✅ | Exact match |
| I-1 (preprocess tables) | DNA line 560: "text-level defense...splitting oversized tables at max_rows=20" | ⚠️ | DNA says "provides the text-level defense" (active voice). CF-1 annotates call site as "currently dormant." See F-DNA-2. |
| I-2 (MIN_RAG_BUDGET) | DNA line 210: "MIN_RAG_BUDGET = 2000 floor check" | ✅ | Matches V9 constant and logic |
| I-3/I-4/I-5 (agent skills) | DNA lines 289–291: All 4 skills listed with API key requirements | ✅ | Matches V9 Appendix A |
| D-1/D-2 (frontend ref) | DNA lines 268–280: parseGusResponse, buildUserMessage, renderGusResponse described | ✅ | Architecture consistent |
| D-3 (CSS classes) | DNA line 730: "No custom frontend" gap noted | ✅ | Consistent — reference implementation, not deployed |
| D-4 (archive ledger) | DNA line 215: "old entries can be moved to MASTER_LEDGER_ARCHIVE.md" | ✅ | Exact concept match |
| D-5 (API key guide) | DNA lines 741–744: Lists all 4 external service dependencies | ✅ | Consistent |
| CF-4 (token budget) | DNA line 715: **"600 (system prompt)"** | **❌ FAIL** | **V9 uses 750. DNA overflow proof is stale.** |

#### F-DNA-1: DNA Overflow Proof Uses Stale 600-Token Value (CRITICAL)

**DNA line 715:**
```
600 (system prompt) + 1,275 (ledger cap) + 1,600 (RAG max) = 3,475
4,000 - 3,475 = 525 tokens remaining for response
```

**V9 Phase 7 checklist (line 1253):**
```
System Prompt: ~750 tokens
TOTAL INPUT: ~3625 tokens
Response Budget: ~375 tokens
```

The DNA is labeled `PROJECT_DNA_V9.md` and serves as the design authority document. Its overflow proof contradicts V9 by 150 tokens. This inconsistency means anyone reading the DNA will believe the response budget is 525 tokens when it is actually 375 — a 40% overstatement of the safety margin.

**Note:** DNA line 210 correctly references `MIN_RAG_BUDGET = 2000` and DNA line 720 correctly describes the floor check. The inconsistency is isolated to the overflow proof block at line 715.

#### F-DNA-2: preprocess_markdown_tables() Active vs. Dormant (OBSERVATION)

DNA line 560 describes the function as providing "the text-level defense." V9's CF-1 annotation (lines 824–826) states the call site is "currently dormant." The function EXISTS and would activate if `.md` files are ingested, so the DNA description is architecturally accurate — the defense is present and ready. The dormant annotation clarifies the current operational state. This is a documentation nuance, not a contradiction. **Non-blocking.**

---

### AUDIT G: SECURITY REVIEW

**Verdict: PASS with 1 significant finding**

#### G-1: XSS Analysis (renderGusResponse)

| Line | innerHTML Usage | Data Source | LLM-Controlled? | Sanitized? | Risk |
|:-----|:---------------|:------------|:-----------------|:-----------|:-----|
| 1717 | `containerEl.innerHTML = ''` | Empty string | No | N/A | None |
| 1721 | `${gus.current_state}`, `${gus.mechanic_instructions}` | LLM JSON | **Yes** | **No** | **XSS via malicious RAG document** |
| 1735 | `${gus.mechanic_instructions}` | LLM JSON | **Yes** | **No** | **XSS via malicious RAG document** |
| 1742 | `'<h4>Sources:</h4>'` | Static | No | N/A | None |
| 1778 | `'<h3>✅ DIAGNOSTIC COMPLETE</h3>'` | Static | No | N/A | None |

**CF-3 WARNING (lines 1704–1705):** Present and comprehensive. Documents the XSS risk, identifies LLM-controlled data sources, mandates DOMPurify or .textContent for custom deployments, notes the deployed system uses AnythingLLM's built-in UI. ✅

**State badge (line 1729):** Uses `.textContent` (safe). ✅
**Citation bubbles (line 1746):** Uses `.textContent` (safe). ✅
**Answer buttons (line 1763):** Uses `.textContent` (safe). ✅

#### G-2: VIN-Lookup Input Sanitization (F-SEC-1)

**FINDING:** VIN-Lookup `handler.js` (line 1613) interpolates the `vin` parameter directly into the NHTSA URL without `encodeURIComponent()`:

```javascript
const response = await fetch(`https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/${vin}?format=json`);
```

**Validation present:**
- `!vin || vin.length < 5` → rejects empty/very short inputs
- `vin.length < 17` → routes to classic chassis bypass

**Validation absent:**
- No character content validation (alphanumeric check)
- No `encodeURIComponent()` before URL interpolation
- A 17+ character input containing `?`, `#`, `&`, `/`, or `%`-encoded payloads would pass all checks and corrupt the request URL

**Comparison:** Purchase-Router (line 1649) correctly uses `encodeURIComponent()`. The inconsistency makes this a pattern violation.

**Practical risk:** VINs are alphanumeric (0-9, A-Z excluding I, O, Q). Real-world exploitation is unlikely but defense-in-depth is absent. In a system handling $250K+ vehicles, this is a standards gap.

#### G-3: Regex ReDoS Analysis (preprocess_markdown_tables)

Line 773: `re.match(r'\|[\s\-:]+\|', lines[i + 1])`

- Character class `[\s\-:]` with `+` quantifier
- No nested quantifiers. No overlapping alternation.
- Linear time complexity. **Not vulnerable to ReDoS.** ✅

Line 778: `lines[i].strip().startswith('|')` — string operation, not regex. ✅

#### G-4: API Key Leakage Search

Full-document search for `$INTERNAL_KEY`, `INTERNAL_KEY`, `REPLACE_ME_KEY`:

| Line | Context | Inside Manual-Status Block? | Leakage? |
|:-----|:--------|:----------------------------|:---------|
| 42 | V2 changelog description | Documentation | No |
| 307, 310, 314 | Phase 3 container setup | Key creation block | No |
| 1340, 1344, 1347, 1367, 1378 | Phase 9 Manual-Status | **Yes** | No |
| 1384 | R-6 NOTE (describes pattern) | Documentation | No |
| 1534, 1535 | Phase 12 verification checklist | Verification script | No |
| 1587 | Appendix A NOTE | Documentation | No |
| 1910, 1932 | Diff analysis table | Documentation | No |

**No API key leakage detected.** All references are either (a) inside the Manual-Status skill block, (b) in the Phase 3 key creation block, (c) in the Phase 12 verification checklist, or (d) in documentation describing the pattern. ✅

---

## SECTION 3: V8 REGRESSION SUMMARY

| Metric | Value |
|:-------|:------|
| Total V8 context lines checked | ~200 |
| V8 lines damaged | **0** |
| Intentional V8 changes | 2 (R-6 text replacement at line 1383, CF-4 formula update at line 983) |
| Both documented in changelog | ✅ |

**No V8 regressions detected.**

---

## SECTION 4: DNA CONSISTENCY SUMMARY

| Metric | Value |
|:-------|:------|
| Total DNA cross-references | 16 |
| DNA matches | 14 |
| DNA contradictions | **1 (F-DNA-1: overflow proof)** |
| DNA observations | 1 (F-DNA-2: active vs. dormant) |

---

## SECTION 5: CRITICAL FINDINGS

### F-DNA-1: DNA Overflow Proof Uses Stale Value [BLOCKS DEPLOYMENT]

- **Location:** PROJECT_DNA_V9.md, line 715
- **Issue:** DNA states `600 (system prompt)` in its overflow proof. V9 uses `750`. The overflow proof total (3,475) and remaining (525) are wrong. Correct values: 3,625 total, 375 remaining.
- **Impact:** Design authority document is inconsistent with the deployed architecture. Any engineer reading the DNA will misjudge the token budget by 150 tokens.
- **Fix Required:** Update DNA line 715 to `750 (system prompt) + 1,275 (ledger cap) + 1,600 (RAG max) = 3,625`. Update remaining to `375`. Update safety buffer to `175`.

### F-SEC-1: VIN-Lookup Missing encodeURIComponent [BLOCKS DEPLOYMENT]

- **Location:** ARCHITECTURE_FINAL_V9.md, line 1613
- **Issue:** `vin` parameter interpolated directly into NHTSA URL without URL encoding. Length checks provide no character validation.
- **Impact:** A crafted 17+ character input with URL-special characters could corrupt the fetch request. Inconsistent with Purchase-Router's defensive pattern (line 1649).
- **Fix Required:** Change line 1613 to `fetch(\`https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/${encodeURIComponent(vin)}?format=json\`)`.

---

## SECTION 6: NON-BLOCKING OBSERVATIONS

### F-TOK-1: System Prompt Token Estimate May Be Slightly Low

- **Location:** V9 Phase 7 checklist (line 1253), validate_ledger.py (line 983)
- **Issue:** Claimed ~750 tokens; character-ratio analysis suggests ~800. Budget proof holds with narrower margin (125 vs. 175 safety tokens).
- **Mitigation:** Phase 7 checklist already instructs post-deployment verification via `docker logs`. 15% safety margin on ledger cap absorbs tokenizer variance.
- **Recommendation:** After deployment, verify actual token count and update if needed.

### F-DNA-2: preprocess_markdown_tables() Active Voice vs. Dormant Annotation

- **Location:** DNA line 560 ("provides the text-level defense") vs. V9 CF-1 (lines 824–826, "currently dormant")
- **Impact:** Documentation nuance only. Function exists and would activate if .md files are ingested. Not a contradiction.

---

## FINAL VERDICT: **BLOCKED**

**2 findings must be resolved before deployment:**

| # | Finding | File | Line | Severity | Fix |
|:--|:--------|:-----|:-----|:---------|:----|
| 1 | **F-DNA-1** | PROJECT_DNA_V9.md | 715 | CRITICAL | Update overflow proof from 600→750, 3475→3625, 525→375 |
| 2 | **F-SEC-1** | ARCHITECTURE_FINAL_V9.md | 1613 | SIGNIFICANT | Add `encodeURIComponent(vin)` to NHTSA fetch URL |

**Confidence level if fixed:** HIGH. All 20 V9 modifications are correctly placed, textually accurate, and structurally sound. No V8 regressions. No code block damage. State machine traces correctly. Token budget proof holds. Security is documented. The two findings are surgical fixes with zero blast radius.

**Items verified: 20/20 PASS | Cross-cutting audits: 6/7 PASS, 1 FAIL (DNA) | Fidelity audit: 16/16 still hold**
