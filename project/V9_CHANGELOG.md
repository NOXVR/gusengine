# V9 CHANGELOG — Priority 1: RESTORE Items

**Date:** 2026-02-16
**Baseline:** ARCHITECTURE_FINAL_V8.md (frozen)
**Target:** ARCHITECTURE_FINAL_V9.md

---

## R-1: "DO NOT TRUST USER'S ASSUMPTIONS" directive

| Field | Value |
|:------|:------|
| **VFINAL Source** | `SECTION_B_VFINAL_BLUEPRINT_PART2.md`, line 15 |
| **V9 Target Line** | 1207 (before edit) → 1207 (after edit) |
| **Text Added** | `YOU DO NOT TRUST THE USER'S ASSUMPTIONS.` inserted between `YOU DO NOT CONVERSE FREELY.` and `YOU ONLY OUTPUT STRICT JSON MATCHING THE SCHEMA BELOW.` |

---

## R-2: DIAGNOSTIC FUNNEL methodology

| Field | Value |
|:------|:------|
| **VFINAL Source** | `SECTION_B_VFINAL_BLUEPRINT_PART2.md`, lines 23–25 |
| **V9 Target Line** | Inserted after line 1221 (after EPISTEMOLOGICAL OVERRIDE rule 4), before DAG STATE TRANSITION MATRIX |
| **Text Added** | `THE DIAGNOSTIC FUNNEL (ANSWER-PATH PROMPTING):` block — "never jump to conclusion", "no open-ended questions", "YOU MUST PROVIDE THE ANSWERS" |

---

## R-3: PHASE_D reset-to-PHASE_A instruction

| Field | Value |
|:------|:------|
| **VFINAL Source** | `SECTION_B_VFINAL_BLUEPRINT_PART2.md`, line 35 |
| **V9 Target Line** | Inserted after line 1226 (after PHASE_D transition rule), within DAG STATE TRANSITION MATRIX |
| **Text Added** | `- After PHASE_D, if the user sends any new message, RESET to PHASE_A_TRIAGE for the new symptom.` |

---

## R-4: answer_path_prompts 2–5 cardinality constraint

| Field | Value |
|:------|:------|
| **VFINAL Source** | `SECTION_B_VFINAL_BLUEPRINT_PART2.md`, lines 32–41 |
| **V9 Target Line** | Inserted after DAG STATE TRANSITION MATRIX section (after line 1227), as standalone blocks |
| **Text Added** | `STATE TRANSITION RULES:` block (2-5 mutually exclusive options, PHASE_D completion rules) + `STATE TRANSITION ENFORCEMENT:` block (completed_state/required_next_state handling, PHASE_ERROR fallback) |

---

## R-5: Torn-copy rationale for container stop

| Field | Value |
|:------|:------|
| **VFINAL Source** | `SECTION_B_VFINAL_BLUEPRINT_PART2.md`, lines 208–209 |
| **V9 Target Line** | 1307 (before edit) — Phase 10 IMPORTANT callout |
| **Text Added** | `The container is stopped before backup to prevent torn copies of LanceDB/SQLite databases. Downtime is ~2-5 minutes at 2 AM.` prepended to existing callout text |

---

## R-6: "Previous steps" self-containment fix

| Field | Value |
|:------|:------|
| **VFINAL Source** | N/A (self-containment fix) |
| **V9 Target Line** | 1300 (before edit) — Phase 9 Agent Skills section |
| **Text Removed** | `*(Deploy remaining skills from previous steps using this identical injection process. Toggle ON in UI).*` |
| **Text Added** | `> [!NOTE]` callout: The 3 additional agent skills (VIN-Lookup, Purchase-Router, Draft-Tribal-Knowledge) are provided in **Appendix A: Agent Skill Definitions** (to be added in Priority 2). Each skill follows this identical sandbox injection pattern. |

---

# V9 CHANGELOG — Priority 2: RE-IMPLEMENT Items

**Date:** 2026-02-16
**Baseline:** ARCHITECTURE_FINAL_V8.md (frozen)
**Target:** ARCHITECTURE_FINAL_V9.md

---

## I-1: `preprocess_markdown_tables()` function restored

| Field | Value |
|:------|:------|
| **VFINAL Source** | `SECTION_B_VFINAL_BLUEPRINT_PART2.md`, lines 391–416 (complete function definition) |
| **V9 Target Lines** | Function definition inserted at line 763 (Phase 5 `sync_ingest.py`, after `CHUNKS_DIR` config, before dedup query). Function call inserted at line 822–828 (upload loop, before API submission). `import re` added to import line 745. |
| **Text Added** | (a) 30-line `preprocess_markdown_tables(md_content, max_rows=20)` function definition with V9 RECOVERY attribution comment. Splits oversized markdown tables at `max_rows=20`, re-injecting header rows into each sub-table to prevent chunk explosion. (b) 7-line conditional call block: `if filename.lower().endswith('.md'):` reads, preprocesses, and writes back the markdown content before API upload. (c) `re` added to imports. |

---

## I-2: `MIN_RAG_BUDGET` floor check restored

| Field | Value |
|:------|:------|
| **VFINAL Source** | `SECTION_B_VFINAL_BLUEPRINT_PART2.md`, lines 500–521 (`MIN_RAG_BUDGET = 2000` constant and `if rag_budget < MIN_RAG_BUDGET` guard) |
| **V9 Target Lines** | Constant inserted at line 972 (Phase 6 `validate_ledger.py`, after `ADJUSTED_CAP` calculation). Floor check inserted at lines 991–993 (after existing `count > ADJUSTED_CAP` rejection). Print label added at line 985. |
| **Text Added** | (a) `MIN_RAG_BUDGET = 2000` constant with 3-line attribution comment. (b) `print(f"Minimum RAG budget floor: {MIN_RAG_BUDGET}")` in output block. (c) 3-line floor check: `if remaining < MIN_RAG_BUDGET:` → warning print + action guidance + `return False`. Adapted to V8 variable names (`remaining` instead of VFINAL's `rag_budget`). |

---

## I-3: @VIN-Lookup agent skill created in Appendix A

| Field | Value |
|:------|:------|
| **VFINAL Source** | `SECTION_B_VFINAL_BLUEPRINT_PART2.md`, lines 83–111 (complete `plugin.json` + `handler.js`) |
| **V9 Target Lines** | New Appendix A section starting at line 1564, after Phase 12 deployment-complete marker and before V8 CONSOLIDATED DIFF. Skill definition at line 1570. |
| **Text Added** | `### Skill: @VIN-Lookup` section with description, `mkdir -p` for directory creation, quoted heredoc (`cat << 'EOF'`) for `plugin.json` and `handler.js`, `docker restart`. Does NOT use `$INTERNAL_KEY` — calls public NHTSA API only. |

---

## I-4: @Purchase-Router agent skill created in Appendix A

| Field | Value |
|:------|:------|
| **VFINAL Source** | `SECTION_B_VFINAL_BLUEPRINT_PART2.md`, lines 149–170 (complete `plugin.json` + `handler.js`) |
| **V9 Target Lines** | Appendix A, after @VIN-Lookup. Skill definition at line 1609. |
| **Text Added** | `### Skill: @Purchase-Router` section with description, `mkdir -p`, quoted heredoc for `plugin.json` and `handler.js`, `docker restart`. Generates vendor search links for missing FSMs. No API key required. |

---

## I-5: @Draft-Tribal-Knowledge agent skill created in Appendix A

| Field | Value |
|:------|:------|
| **VFINAL Source** | `SECTION_B_VFINAL_BLUEPRINT_PART2.md`, lines 172–192 (complete `plugin.json` + `handler.js`) |
| **V9 Target Lines** | Appendix A, after @Purchase-Router. Skill definition at line 1641. |
| **Text Added** | `### Skill: @Draft-Tribal-Knowledge` section with description, `mkdir -p`, quoted heredoc for `plugin.json` and `handler.js`, `docker restart`. Formats undocumented fixes into FAULT SIGNATURE structure for MASTER_LEDGER.md. No API key required. |

---

## I-3/I-4/I-5: R-6 NOTE callout updated

| Field | Value |
|:------|:------|
| **V9 Target Line** | 1365 (Phase 9 Agent Skills [!NOTE] callout) |
| **Text Changed** | Removed "(to be added in Priority 2)" and "inject API key via `sed`, restart container, toggle ON in UI". Replaced with accurate description: these skills do NOT require `$INTERNAL_KEY`, use quoted heredocs, and direction to toggle ON in Settings → Agent Skills. |

---

# V9 CHANGELOG — Priority 3: DOCUMENT Items

**Date:** 2026-02-16
**Baseline:** ARCHITECTURE_FINAL_V8.md (frozen)
**Target:** ARCHITECTURE_FINAL_V9.md

---

## D-1: `renderGusResponse()` reference implementation

| Field | Value |
|:------|:------|
| **VFINAL Source** | `SECTION_B_VFINAL_BLUEPRINT_PART2.md`, lines 281–346 (complete 65-line UI rendering function) |
| **V9 Target Lines** | New Appendix B section inserted after Appendix A (line 1672 before edit → line 1685 after edit), before V8 CONSOLIDATED DIFF ANALYSIS |
| **Text Added** | Complete `renderGusResponse(gus, containerEl, textInputEl)` function with: error/RETRIEVAL_FAILURE state handling, state badge display, mechanic instructions rendering, NotebookLM-style citation bubbles, answer-path prompt buttons with `sendToAnythingLLM()` integration, text input disable/enable control, and PHASE_D completion state. Includes `> [!NOTE]` explaining this is a reference implementation — the deployed system uses AnythingLLM's built-in chat UI. |

---

## D-2: `sendToAnythingLLM()` reference implementation

| Field | Value |
|:------|:------|
| **VFINAL Source** | `SECTION_B_VFINAL_BLUEPRINT_PART2.md`, lines 348–371 (complete 20-line API integration function) |
| **V9 Target Lines** | Appendix B, after `renderGusResponse()` section |
| **Text Added** | Complete `sendToAnythingLLM(message)` async function showing: fetch to `workspace/${WORKSPACE_SLUG}/chat` endpoint, Authorization Bearer header, JSON body with `mode: "chat"`, response parsing via `parseGusResponse()`, and re-render via `renderGusResponse()`. Includes `> [!WARNING]` that `YOUR_SERVER_IP` and `YOUR_INTERNAL_API_KEY` must be replaced. |

---

## D-3: CSS class name specification (styling contract)

| Field | Value |
|:------|:------|
| **VFINAL Source** | `SECTION_B_VFINAL_BLUEPRINT_PART2.md`, lines 281–346 (CSS class names and DOM IDs extracted from function body) |
| **V9 Target Lines** | Appendix B, after `sendToAnythingLLM()` section |
| **Text Added** | Two tables documenting the styling contract. CSS Classes table: 8 classes (`gus-error`, `gus-state-badge`, `gus-instructions`, `gus-citations`, `gus-citation-bubble`, `gus-buttons`, `gus-answer-btn`, `gus-complete`) with element types and purposes. DOM Element IDs table: 2 IDs (`gus-container`, `symptom-input`) with element types and purposes. |

---

## D-4: Archive ledger lifecycle

| Field | Value |
|:------|:------|
| **VFINAL Source** | `SECTION_B_VFINAL_BLUEPRINT_PART2.md`, lines 516–518 (archive action text referencing `MASTER_LEDGER_ARCHIVE.md`) |
| **V9 Target Lines** | Line 989 (before edit) — Phase 6 `validate_ledger.py`, after the "Archive oldest entries and retry." rejection message |
| **Text Added** | `> [!NOTE]` block documenting the `MASTER_LEDGER_ARCHIVE.md` concept: old entries are moved to a non-pinned archive file that is still uploaded and embedded in the workspace, participates in vector search (discoverable via RAG retrieval), but does NOT consume the fixed context token budget on every query. Preserves historical tribal knowledge while freeing pinned context budget. |

---

## D-5: API key insertion guide

| Field | Value |
|:------|:------|
| **VFINAL Source** | `SECTION_B_VFINAL_BLUEPRINT_PART1.md`, lines 404–412 (Phase 4 UI configuration with navigation paths) |
| **V9 Target Lines** | Line 1217 (before edit) — Phase 7 (LLM & Embedding Configuration), after item 4 (Mistral OCR chunk token size) |
| **Text Added** | `> [!IMPORTANT]` callout with a 4-row table listing exact UI navigation paths for: Anthropic (Settings → AI Providers → Anthropic → Insert API Key), Voyage AI (Settings → Embedding Preference → Voyage AI → Insert API Key), Mistral (Settings → Document Handling → Mistral OCR), and Cohere (Settings → AI Providers → Reranking → Cohere → Insert API Key). Each row includes the key required. |

---

# V9.1 CHANGELOG — Hostile Audit Fixes

**Date:** 2026-02-17
**Source:** `MASTER_AUDIT_VERDICT.md` Section 5 (Recommendations)
**Target:** ARCHITECTURE_FINAL_V9.md

---

## V9.1-F1: Add missing plugin.json fields [MEDIUM → REQUIRED]

| Field | Value |
|:------|:------|
| **Audit Finding** | B4 9.2 — All 4 plugin.json missing `schema` and `imported` fields |
| **Verification Doc** | `docs/anythingllm/agent-skills-plugin-json.md` — `schema: "skill-1.0.0"` REQUIRED (line 342), `imported` must be `true` (line 425) |
| **V9 Target Lines** | 1356–1360 (Manual-Status), 1598–1605 (VIN-Lookup), 1637–1644 (Purchase-Router), 1669–1676 (Draft-TK) |
| **Text Added** | `"schema": "skill-1.0.0"` and `"imported": true` inserted after `"version"` in each plugin.json |

---

## V9.1-F2: Add try/catch to 2 agent skill handlers [MEDIUM → REQUIRED]

| Field | Value |
|:------|:------|
| **Audit Finding** | B4 9.3 — @Purchase-Router and @Draft-Tribal-Knowledge handlers missing try/catch |
| **Verification Doc** | `docs/javascript/errors.md` — standard JS error handling pattern |
| **V9 Target Lines** | 1655–1660 (Purchase-Router handler.js), 1689–1694 (Draft-TK handler.js) |
| **Text Added** | `try { ... } catch (e) { return \`ERROR: ${e.message}\`; }` wrapping existing handler body in each skill |

---

## V9.1-F3: Update version reference V8 → V9 [LOW → RECOMMENDED]

| Field | Value |
|:------|:------|
| **Audit Finding** | B5 12.2 — Closing statement says "V8 ARCHITECTURE" not "V9" |
| **Verification Doc** | N/A (cosmetic fix) |
| **V9 Target Line** | 1584 |
| **Text Changed** | `THE V8 ARCHITECTURE` → `THE V9 ARCHITECTURE` |

---

## V9.1-F4: Prevent duplicate API key entries [LOW → RECOMMENDED]

| Field | Value |
|:------|:------|
| **Audit Finding** | B1 3.4 — Duplicate `INTERNAL_API_KEY` entries possible via `>>` append |
| **Verification Doc** | `docs/bash/sed.md` — `sed -i` in-place editing with address-based deletion confirmed (lines 274–280, 796–800) |
| **V9 Target Line** | 304 (Phase 3 API key setup) |
| **Text Added** | `sed -i '/^INTERNAL_API_KEY=/d' $HOME/diagnostic_engine/.env` inserted before `echo >> .env` |

---

## V9.1-F5: Add error handling to verify_ingestion.py [LOW → RECOMMENDED]

| Field | Value |
|:------|:------|
| **Audit Finding** | B2 5.7 — `verify_ingestion.py` missing try/except around API call |
| **Verification Doc** | `docs/python-requests/quickstart.md` — `requests.exceptions.RequestException` is the base exception (line 584) |
| **V9 Target Line** | 920 (Phase 5 verify_ingestion.py) |
| **Text Added** | `try: ... except requests.RequestException as e: print(f"ERROR: Cannot reach API: {e}"); sys.exit(1)` wrapping the `requests.get()` call |

---

# V9.2 CHANGELOG — Watermark Deprecation & Citation Strategy

**Date:** 2026-02-24
**Source:** Production testing during multipass build (Phases 4, 7, 8)
**Target:** ARCHITECTURE_FINAL_V9.md

---

## V9.2-W1: Deprecate [[ABSOLUTE_PAGE: N]] watermarking pipeline

| Field | Value |
|:------|:------|
| **Finding** | PDF watermarking provides zero diagnostic accuracy benefit — purely citation UX. LLM reasons from semantic content; page numbers do not influence diagnostic decisions. |
| **Root Causes** | (1) Ingestion bottleneck: 2+ hrs per corpus update via Mistral OCR rate limits. (2) Chunk boundary problem: 400-char text splitter separates watermarks from content. (3) Zero accuracy benefit. |
| **V9 Lines Changed** | 323 (Phase 4 goal), 438-450 (chunk_pdf docstring), 1273-1290 (citation strategy), 1326-1328 (JSON example) |
| **Resolution** | Document-level citations via `sources[].title`. FSM docs average 4.7 pages. Filename convention (e.g., `07.4.1-411`) encodes section number as locator. |
| **System Prompt** | Replaced WATERMARK-FIRST dual-layer rules with V9.2 document-level rules. |
| **Daemon Code** | Watermark code in `chunk_pdf()` preserved but marked SKIPPED at runtime. |

---

## V9.3-R1: RAG Pipeline Reassessment & Deprecation

| Field | Value |
|:------|:------|
| **Finding** | Competitive benchmarking against NotebookLM (identical 514-PDF corpus, validated by working mechanics) revealed 7 CRITICAL capability gaps in the V9 RAG pipeline. |
| **Deprecated** | `chunk_pdf()` 5-page splitting, `sync_ingest.py` flat upload, RecursiveTextSplitter 400/20, TopN=4, Cohere reranking (untested), watermark citations, Voyage AI (sole retrieval) |
| **Not Deprecated** | Infrastructure (Phases 1-3), DAG state machine (Phase 8), Agent Skills (Phase 9), Ops tooling (Phases 10-12) |
| **V9 Lines Added** | New section "V9.3 — RAG PIPELINE REASSESSMENT & DEPRECATION NOTICE" inserted after Phase 12 deployment-complete marker |
| **Next Step** | V10 investigation: structural document parsing, multimodal ingestion, intelligent retrieval, dual-layer architecture |
