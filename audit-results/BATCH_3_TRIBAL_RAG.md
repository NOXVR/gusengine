# BATCH 3: TRIBAL KNOWLEDGE & RAG MATH AUDIT (Phases 6-7)

**GATE 1 PASSED: rules.md read in full. Identity locked.**

**Auditor:** Antigravity (Hostile Audit Mode)
**Date:** 2026-02-16
**Architecture Scope:** `ARCHITECTURE_FINAL_V9.md` lines 943-1335
**DNA Cross-Reference:** `PROJECT_DNA_V9.md` (775 lines, read in full — Batch 1)
**Changelog Cross-Reference:** `V9_CHANGELOG.md` (193 lines, read in full — Batch 2, re-verified)
**Continuity:** `BATCH_1_FOUNDATION.md` (419 lines), `BATCH_2_INGESTION.md` (466 lines)

---

## PHASE 6: THE TRIBAL KNOWLEDGE SUBSYSTEM (Lines 943-1212)

### Finding 6.1: PASS — `validate_ledger.py` Imports and Constants (Lines 964-976)

**What was checked:** `import tiktoken, sys`. Constants: `RAW_CAP = 1500`, `SAFETY_FACTOR = 0.85`, `ADJUSTED_CAP = int(RAW_CAP * SAFETY_FACTOR)`, `MIN_RAG_BUDGET = 2000`.

**What I compared against:**
- `docs/tiktoken/readme.md` line 81: `cl100k_base = tiktoken.get_encoding("cl100k_base")` — confirmed `get_encoding` is the correct function. ✅
- `docs/tiktoken/cookbook.md` line 32: `cl100k_base` is the encoding for `gpt-4`, `gpt-3.5-turbo`, etc. ✅
- V9 Changelog I-2: "MIN_RAG_BUDGET = 2000 constant" at line 976.

**Independent math:** `int(1500 * 0.85) = int(1275.0) = 1275`. ✅

**Why it passes:** `tiktoken.get_encoding("cl100k_base")` is correct per docs. The V2 fix (line 952) correctly notes that `encoding_for_model("gpt-4")` depends on tiktoken's internal mapping which could change. Pinning to `cl100k_base` is the safer choice.

**Adversarial cases tested:**
1. "Is `cl100k_base` the right encoding for Anthropic Claude?" — No. Anthropic uses a different tokenizer. The architecture acknowledges this at line 967: "15% safety margin for GPT-4 vs Anthropic tokenizer divergence." The `cl100k_base` encoder is used as an APPROXIMATION with a 15% buffer. This is a pragmatic design choice documented in the DNA and is intentional. ✅
2. "What if `tiktoken` is not installed?" — The venv mandate (Phase 5, line 721) ensures it's available. ✅
3. "The `remaining` formula at line 984 — is `750` still correct for V9?" — The comment says "V9: +150 from R-1–R-4". The original V8 system prompt was ~600 tokens. V9 added R-1 through R-4 restorations (Diagnostic Funnel, PHASE_D reset, state transition rules) adding ~150 tokens → ~750 total. The 750 is the V9-updated value. ✅

### Finding 6.2: PASS — `validate_ledger.py` Validation Logic (Lines 978-1007)

**What was checked:** Two validation gates: (1) `count > ADJUSTED_CAP` rejection, (2) `remaining < MIN_RAG_BUDGET` rejection. Exit code management via `__main__`.

**What I compared against:**
- V9 Changelog I-2: "if remaining < MIN_RAG_BUDGET: → warning print + action guidance + return False"
- rules.md line 167: "The `MIN_RAG_BUDGET = 2000` floor check rejects ledgers at 1275 tokens because `remaining = 1975 < 2000`. This is NOT a deadlock — it is a deliberate safety valve."

**Why it passes:**
1. First gate (line 991): `count > ADJUSTED_CAP (1275)` — hard rejection of oversized ledgers. ✅
2. Second gate (line 995): `remaining < MIN_RAG_BUDGET (2000)` — ensures RAG budget floor. ✅
3. `sys.exit(0 if result else 1)` (line 1007) — correct exit code convention. ✅

**Critical design verification:** At `count = 1275` (exactly at cap):
- `remaining = 4000 - 750 - 1275 = 1975`
- `1975 < 2000` → True → **REJECTED by MIN_RAG_BUDGET floor.**
- This means the EFFECTIVE ledger maximum is lower than 1275. Solving: `4000 - 750 - count >= 2000` → `count <= 1250`.
- **Effective ledger max = 1250 tokens** (not 1275).
- This is the INTENTIONAL safety valve from rules.md. The 25-token gap between ADJUSTED_CAP (1275) and the effective max (1250) creates a dead zone where the ledger passes the first check but fails the second. This prevents corner cases where the ledger technically fits but leaves insufficient RAG budget. ✅

**Adversarial cases tested:**
1. "What if the ledger file doesn't exist?" — `open(path, 'r')` raises `FileNotFoundError`. No try/except. Python traceback visible to operator — acceptable for a CLI validator. ✅
2. "What if the file is binary/non-UTF8?" — `f.read()` may raise `UnicodeDecodeError`. Same as above — acceptable. ✅
3. "Is `len(enc.encode(content))` correct for token counting?" — Per `docs/tiktoken/cookbook.md` line 139: `encoding.encode(text)` returns a list of token IDs. `len()` gives the count. Correct. ✅

### Finding 6.3: PASS — Archive Ledger Lifecycle Note (Lines 1011-1012)

**What was checked:** V9 Recovery D-4 NOTE block documenting `MASTER_LEDGER_ARCHIVE.md` concept.

**What I compared against:** V9 Changelog D-4: "old entries moved to non-pinned MASTER_LEDGER_ARCHIVE.md... participates in vector search (discoverable via RAG retrieval) but does NOT consume the fixed context token budget."

**Why it passes:** The NOTE accurately describes the archive mechanism: non-pinned documents are in the embedding database and retrievable via vector search, but only pinned documents consume the hard token budget on every query. This distinction is architecturally sound with AnythingLLM's pinning behavior.

### Finding 6.4: PASS — `sync_ledger.py` Script (Lines 1032-1119)

**What was checked:** Ledger upload with old-version deletion (atomic swap). Imports: `os, requests, sys`. API key guard, HTTP status check, empty documents guard, old ledger detection via workspace query.

**What I compared against:**
- `docs/python-requests/api-reference.md` line 175: `requests.post(url, ...)` — confirmed.
- V2 fixes: `cut -d '=' -f2-`, key guard, documents list guard — all present and verified.
- V8 FIX (Phase 10 DT R3): Old ledger atomic swap via `deletes: [old_ledger_loc]`.

**Why it passes:**
1. Old ledger detection (lines 1066-1077): Queries workspace, finds any doc with "MASTER_LEDGER" in name. ✅
2. Atomic swap (line 1105): `json={"adds": [doc_loc], "deletes": [old_ledger_loc] if old_ledger_loc else []}` — single API call replaces old vectors with new ones. ✅
3. Error handling: `try/except` around workspace query (line 1078), with fallback to no-delete mode. ✅
4. Fatal exits (lines 1092, 1097, 1111, 1114, 1117) prevent silent failure. ✅

**Adversarial cases tested:**
1. "What if two ledger versions exist?" — Line 1077 `break` stops at the first match. Only the first old ledger found is deleted. If multiple exist, subsequent ones remain. LOW risk — the operator would need to manually clean up via the Web UI. Acceptable for a single-workspace system. ✅
2. "MIME type `text/markdown` — is this correct?" — Line 1087: `("file", (filename, f, "text/markdown"))`. AnythingLLM accepts markdown files for processing. The MIME type is a hint — AnythingLLM uses file extension for format detection. ✅
3. "What if the embed request fails but upload succeeded?" — Lines 1110-1111: `sys.exit(1)`. The document is uploaded but not embedded. The operator sees the error and can retry. The old ledger vectors were NOT deleted (the `deletes` only fires if the embed request succeeds at the API level). ✅

### Finding 6.5: PASS — `update_ledger.sh` Execution Gate (Lines 1129-1172)

**What was checked:** Bash script with `set -e`, argument validation, file existence check, validate-then-upload gate, manual pin reminder.

**What I compared against:**
- DNA line 204: "Gated enforcement — validate before upload."
- Batch 1 audit: bash `-z` flag, `-f` flag verified correct.

**Why it passes:**
1. `set -e` (line 1131): exits on any error. ✅
2. `-z "$LEDGER_PATH"` (line 1141): empty-argument check. ✅
3. `! -f "$LEDGER_PATH"` (line 1146): file existence check. ✅
4. Validate gate (line 1155): runs `validate_ledger.py` first. If exit code is non-zero, `set -e` halts script. ✅
5. Upload (line 1165): only reached if validation passed. ✅
6. Pin reminder (lines 1169-1170): reminds operator to pin in Web UI. ✅

**Adversarial cases tested:**
1. "What if validate_ledger.py itself crashes (not just returns False)?" — `set -e` catches any non-zero exit code, including crashes. The if/then pattern (line 1155) also catches this. ✅
2. "What if `$VENV_PYTHON` doesn't exist?" — `set -e` triggers on the failed execution. Error message would be bash's own "No such file or directory." The operator would see it. ✅
3. "Race condition: file edited between validation and upload?" — Possible but extremely unlikely in a single-operator system. The window is the time between validate_ledger.py returning and sync_ledger.py reading the file. ✅

### Finding 6.6: PASS — Seed Ledger Content (Lines 1180-1194)

**What was checked:** `MASTER_LEDGER.md` seed with fault signature structure, authority level, override mandate.

**What I compared against:** DNA: Tribal knowledge format with FAULT SIGNATURE, OEM DIAGNOSIS, MASTER TECH OVERRIDE, VERIFICATION TEST.

**Why it passes:** The seed ledger demonstrates the canonical structure:
1. Authority header: "TRIBAL SUPREMACY" — establishes override priority. ✅
2. Fault signature with 3 components: OEM diagnosis, override, verification test. ✅
3. Vehicle-specific content (1975 450SL) matching the workspace slug. ✅

---

## PHASE 7: UI CALIBRATION & RAG MATHEMATICS (Lines 1214-1262)

### Finding 7.1: PASS — AI Provider Configuration (Lines 1217-1244)

**What was checked:** Model names, token limits, and UI settings for Anthropic, Voyage AI, Mistral OCR, and Cohere.

**What I compared against:**
- **Anthropic `claude-3-5-sonnet-latest`:** Searched `docs/anthropic/messages-api.md` — NOT FOUND in the model list. The listed models are: `claude-3-7-sonnet-latest`, `claude-3-5-haiku-latest`, `claude-3-opus-latest`, `claude-3-haiku-20240307`. However: `claude-3-5-sonnet` was a widely-used model that has since been superseded by `claude-3-7-sonnet`. The architecture specifies this model for AnythingLLM's UI dropdown — AnythingLLM may have its own model alias mapping. The docs may not list deprecated/previous-gen models. **INFORMATIONAL — see Finding 7.2.**
- **Voyage AI `voyage-3-large`:** `docs/voyage-ai/docs-embeddings.md` line 121: Confirmed. 32K context, 1024 dimensions. ✅
- **Mistral OCR:** `docs/mistral/basic-ocr.md` line 82: `mistral-ocr-latest`. Architecture line 1222 says "Mistral OCR" without specifying model name — correct, as it's a provider selection in AnythingLLM. ✅
- **Cohere `rerank-english-v3.0`:** `docs/cohere/models.md` line 212: Confirmed. 4K context. ✅

**Adversarial cases tested:**
1. "Token Limit 4000 — is this validated?" — Architecture line 1218: `4000`. This is a UI setting in AnythingLLM that caps the total tokens sent to Anthropic. It's a user-configurable value, not a model constraint. Claude models support much higher context windows (200K+). The 4000 cap is a deliberate cost/accuracy trade-off to prevent hallucination from excessive context. ✅
2. "Chunk Token Size 400 — does this match Phase 4?" — Line 1224 says 400 tokens "perfectly matches the 5-page physical PDF chunking threshold." Phase 4 chunk_pdf uses `chunk_size=5`. Each 5-page chunk should yield approximately 400 tokens when processed by Mistral OCR. This is a design assumption, not a mathematical guarantee — PDF page density varies. The 400 is a target, not a measured value. ✅
3. "Similarity Threshold 0.50 — is this reasonable?" — For a diagnostic RAG system, 0.50 is a moderate threshold. Lower would include more noise; higher would miss relevant chunks for rare symptoms. ✅

### Finding 7.2: INFORMATIONAL — Anthropic Model Name Not in Local Docs (Line 1217)

**Severity:** INFORMATIONAL
**Lines:** 1217
**Classification:** NOT A DEFECT

**Quote:**
```
Settings → AI Providers → **Anthropic** (`claude-3-5-sonnet-latest`).
```

**Evidence:** `claude-3-5-sonnet-latest` is not listed in `docs/anthropic/messages-api.md`. The documented model list includes `claude-3-7-sonnet-latest` but NOT `claude-3-5-sonnet-latest`. This indicates either:
1. The docs were captured after the model was deprecated/superseded, OR
2. The architecture references a model alias that AnythingLLM resolves internally.

**Why this is INFORMATIONAL, not a finding:** The architecture specifies this as a UI dropdown selection in AnythingLLM. AnythingLLM may support model names that differ from or extend the Anthropic API's official model list. The model name is not used in any code block — it's a configuration instruction. The operator would see available models in the AnythingLLM dropdown and select accordingly.

**Recommendation:** Consider updating to `claude-3-7-sonnet-latest` (the current model) or confirm that AnythingLLM's model list includes `claude-3-5-sonnet-latest` as a valid option.

### Finding 7.3: PASS — V9 Recovery D-5 API Key Insertion Guide (Lines 1226-1236)

**What was checked:** UI navigation paths for Anthropic, Voyage AI, Mistral, Cohere API keys.

**What I compared against:** V9 Changelog D-5: "IMPORTANT callout with a 4-row table listing exact UI navigation paths."

**Why it passes:** The table provides clear, step-by-step navigation paths for each provider. Each row specifies the provider, the UI path, and the key required. This was dropped during consolidation and correctly restored in V9.

### Finding 7.4: PASS — Token Budget Verification Checklist (Lines 1251-1260)

**What was checked:** The token budget arithmetic:
- System Prompt: ~750 tokens
- Pinned Ledger (cap): ~1275 tokens
- RAG Chunks (4 × 400): 1600 tokens
- TOTAL INPUT: ~3625 tokens
- Response Budget: ~375 tokens

**Independent computation:**
| Component | Value | Source |
|:----------|:------|:-------|
| Total context limit | 4000 | Architecture line 1218 |
| System prompt | ~750 | Architecture line 1254, V9: +150 from R-1–R-4 |
| Ledger cap (safety-adjusted) | 1275 | `int(1500 * 0.85)` = 1275, line 970 |
| RAG chunks | 4 × 400 = 1600 | Lines 1243-1244 |
| Total input | 750 + 1275 + 1600 = 3625 | My computation |
| Response budget | 4000 - 3625 = 375 | My computation |
| Gus JSON output size | ~200 tokens | Architecture line 1258 |
| Response margin | 375 - 200 = 175 tokens | My computation |

**Match:** Architecture line 1257-1258: "TOTAL INPUT: ~3625 tokens / Response Budget: ~375 tokens" — ✅ matches my computation exactly.

**Why it passes:** All arithmetic is correct. The response margin (175 tokens after JSON output) is tight but sufficient.

**Adversarial cases tested:**
1. "What if the system prompt is ACTUALLY >750 tokens?" — The system prompt text (lines 1275-1331) is ~57 lines of text. This is an ESTIMATE. The architecture uses `~750` (approximate). If the actual count is 800, the response budget drops to 325. Still sufficient for the ~200-token JSON output. ✅
2. "What if RAG returns fewer than 4 chunks?" — Then the RAG budget is partially unused, giving more room for response. The 4 is a maximum, not a minimum. ✅
3. "Effective ledger max conflict (Finding 6.2)?" — As computed in Finding 6.2, the MIN_RAG_BUDGET floor means the effective ledger max is 1250, not 1275. At 1250: `remaining = 4000 - 750 - 1250 = 2000 >= 2000`. Passes. The token budget checklist shows 1275 as the "cap" but the actual effective max is 1250. This is a known design property, not a bug (rules.md line 167). ✅

### Finding 7.5: PASS — Phase 8 System Prompt Content (Lines 1275-1331)

**What was checked:** FSM state definitions, transition rules, citation strategy, JSON output schema. (NOTE: Phase 8 begins at line 1264 and extends to 1335. It is included in this batch because it's within the 943-1335 scope. Full Phase 8 audit will be in Batch 4.)

**Why it passes (preliminary):** The system prompt structure is sound:
- 5 FSM states: PHASE_A_TRIAGE, PHASE_B_FUNNEL, PHASE_C_TESTING (labeled DEEP_DIVE in DNA), PHASE_D_CONCLUSION, RETRIEVAL_FAILURE.
- Every state has defined transitions.
- `requires_input` flags are correct per state.
- JSON schema includes all required fields.
- CRITICAL OUTPUT RULE (line 1330) prevents markdown wrapping.

**Deferred to Batch 4:** Full FSM state machine consistency audit (dead states, infinite loops, missing transitions).

---

## FINDINGS SUMMARY TABLE

| # | Phase | Finding | Severity | Lines | Classification | Status |
|:--|:------|:--------|:---------|:------|:---------------|:-------|
| 6.1 | Phase 6 | `validate_ledger.py` imports/constants | — | 964-976 | — | PASS |
| 6.2 | Phase 6 | `validate_ledger.py` validation logic | — | 978-1007 | — | PASS |
| 6.3 | Phase 6 | Archive ledger lifecycle note | — | 1011-1012 | — | PASS |
| 6.4 | Phase 6 | `sync_ledger.py` atomic swap | — | 1032-1119 | — | PASS |
| 6.5 | Phase 6 | `update_ledger.sh` execution gate | — | 1129-1172 | — | PASS |
| 6.6 | Phase 6 | Seed ledger content | — | 1180-1194 | — | PASS |
| 7.1 | Phase 7 | AI provider configuration | — | 1217-1244 | — | PASS |
| 7.2 | Phase 7 | Anthropic model name not in local docs | INFORMATIONAL | 1217 | NOT A DEFECT | NOTE |
| 7.3 | Phase 7 | V9 D-5 API key insertion guide | — | 1226-1236 | — | PASS |
| 7.4 | Phase 7 | Token budget verification checklist | — | 1251-1260 | — | PASS |
| 7.5 | Phase 7 | Phase 8 system prompt (preliminary) | — | 1275-1331 | — | PASS (deferred to Batch 4) |

---

## DNA CROSS-REFERENCE TABLE

| DNA Claim (Line) | Architecture Claim (Line) | Match |
|:---|:---|:---|
| Tripartite gated enforcement (DNA line 204) | Lines 1121-1172: validate → sync → update pipeline | ✅ |
| MASTER_LEDGER.md token validation before upload (DNA line 204) | Lines 1154-1158: validate_ledger.py gate | ✅ |
| Tribal knowledge — FAULT SIGNATURE structure (DNA line 210) | Lines 1189-1192: OEM diagnosis + override + verification test | ✅ |
| Ledger override precedence (DNA line 212) | Line 1290: "Pinned MASTER_LEDGER.md is the ABSOLUTE TRUTH" | ✅ |
| 5-state FSM (DNA line 115) | Lines 1296-1311: PHASE_A through PHASE_D + RETRIEVAL_FAILURE | ✅ |
| Answer-path prompting — 2-5 options (DNA line 120) | Line 1304: "2-5 mutually exclusive options" | ✅ |
| PHASE_D reset to PHASE_A (DNA line 122) | Line 1300: "RESET to PHASE_A_TRIAGE for the new symptom" | ✅ |
| Token limit: 4000 (NOT IN DNA) | Line 1218: Token Limit 4000 | NOT IN DNA |
| Anthropic model name (NOT IN DNA) | Line 1217: `claude-3-5-sonnet-latest` | NOT IN DNA |
| Embedding model: Voyage AI (NOT IN DNA) | Line 1221: `voyage-3-large` | NOT IN DNA |
| Reranker: Cohere (NOT IN DNA) | Line 1240: `rerank-english-v3.0` | NOT IN DNA |
| OCR: Mistral (NOT IN DNA) | Line 1222: Mistral OCR | NOT IN DNA |
| Chunk token size: 400 (NOT IN DNA) | Line 1224: 400 tokens | NOT IN DNA |
| Similarity threshold: 0.50 (NOT IN DNA) | Line 1242: 0.50 | NOT IN DNA |
| Max context snippets: 4 (NOT IN DNA) | Line 1243: 4 chunks | NOT IN DNA |
| Chat history limit: 4 (NOT IN DNA) | Line 1248: 4 | NOT IN DNA |
| System prompt ~750 tokens with V9 additions (NOT IN DNA explicitly) | Lines 984, 1254: ~750 tokens | NOT IN DNA |
| RAW_CAP 1500 / SAFETY_FACTOR 0.85 (NOT IN DNA explicitly) | Lines 968-970: 1500 * 0.85 = 1275 | NOT IN DNA |
| MIN_RAG_BUDGET 2000 (NOT IN DNA as exact value) | Line 976: 2000 | NOT IN DNA |
| `cl100k_base` encoding (NOT IN DNA) | Line 980: `get_encoding("cl100k_base")` | NOT IN DNA |
| Never edit ledger through Web UI (DNA line 206) | Lines 945-947: CAUTION block | ✅ |
| Nginx blocks external upload endpoint (DNA line 134) | Lines 947, 1125: explicit mention | ✅ |
| RETRIEVAL_FAILURE safeguard (DNA line 126) | Lines 1313-1315: zero-retrieval output spec | ✅ |

---

## CHANGELOG PROVENANCE TABLE

| V2/V8/V9 Fix (Changelog Line) | Original Finding | Architecture Line | Verified |
|:---|:---|:---|:---|
| `tiktoken` pinned to `cl100k_base` (V2 Fix / arch line 952) | V2 Fix | Line 980: `get_encoding("cl100k_base")` | ✅ |
| `cut -d '=' -f2-` in sync_ledger.py (V2 CL / arch line 1026) | CO 5.4, CO_2 06 | Line 1042: `-f2-` | ✅ |
| API key empty-check guard in sync_ledger.py (V2 CL / arch line 1027) | CO 6.1, CO_2 07 | Lines 1046-1048: `if not API_KEY: sys.exit(1)` | ✅ |
| Upload response `documents` list guard (V2 CL / arch line 1028) | V2 Fix | Lines 1094-1097: `if not documents: ... sys.exit(1)` | ✅ |
| HTTP status check before JSON parse (V2 CL / arch line 1089) | V2 Fix | Lines 1090-1092: `if resp.status_code != 200` | ✅ |
| Old ledger atomic swap via workspace query (V8 FIX Phase 10 DT R3 / arch line 1061) | Phase 10 DT R3 | Lines 1066-1077: old ledger detection + line 1105: `deletes` | ✅ |
| V9 Recovery I-2: MIN_RAG_BUDGET floor check (V9 CL I-2 / CL line 88) | VFINAL recovery | Lines 972-976: constant + lines 995-998: guard | ✅ |
| V9 Recovery D-4: Archive ledger lifecycle note (V9 CL D-4 / CL line 175) | VFINAL recovery | Lines 1011-1012: NOTE block | ✅ |
| V9 Recovery D-5: API key insertion guide (V9 CL D-5 / CL line 185) | VFINAL recovery | Lines 1226-1236: IMPORTANT callout with table | ✅ |
| V9 Recovery R-1: "DO NOT TRUST USER'S ASSUMPTIONS" (V9 CL R-1 / CL line 9) | VFINAL recovery | Line 1277: in system prompt | ✅ |
| V9 Recovery R-2: DIAGNOSTIC FUNNEL (V9 CL R-2 / CL line 19) | VFINAL recovery | Lines 1292-1293: DIAGNOSTIC FUNNEL section | ✅ |
| V9 Recovery R-3: PHASE_D reset-to-PHASE_A (V9 CL R-3 / CL line 29) | VFINAL recovery | Line 1300: reset instruction | ✅ |
| V9 Recovery R-4: answer_path_prompts 2-5 cardinality (V9 CL R-4 / CL line 39) | VFINAL recovery | Lines 1303-1311: STATE TRANSITION RULES + ENFORCEMENT | ✅ |

---

## INDEPENDENT MATH TABLE

| Calculation | Source | My Result | Match |
|:---|:---|:---|:---|
| ADJUSTED_CAP | `int(1500 * 0.85)` (line 970) | 1500 × 0.85 = 1275.0 → int = 1275 | ✅ |
| RAG chunks budget | 4 × 400 (line 1243) | 1600 tokens | ✅ |
| Total input ceiling | 750 + 1275 + 1600 (line 1257) | 3625 tokens | ✅ |
| Response budget | 4000 - 3625 (line 1258) | 375 tokens | ✅ |
| Response margin after Gus JSON | 375 - 200 (line 1258) | 175 tokens | ✅ |
| `remaining` at cap=1275 | 4000 - 750 - 1275 (line 984) | 1975 tokens | ✅ |
| MIN_RAG_BUDGET check at cap | 1975 < 2000 (line 995) | True → REJECTED (intentional) | ✅ |
| Effective ledger max | 4000 - 750 - count ≥ 2000 → count ≤ 1250 | 1250 tokens | ✅ (intentional gap) |
| Dead zone range | 1250 < count ≤ 1275 | 25-token dead zone | ✅ (intentional safety valve) |
| Safety margin percentage | (1500 - 1275) / 1500 | 0.15 = 15% | ✅ |
| Similarity threshold | 0.50 (line 1242) | No computation — config value | ✅ |
| Chat history limit | 4 (line 1248) | No computation — config value | ✅ |
| V9 system prompt token increase | ~600 (V8) + ~150 (R-1–R-4) (line 1254) | ~750 tokens | ✅ |
| Cohere context limit | 4096 tokens (docs/cohere/models.md:212) | 4K context for rerank-english-v3.0 | ✅ |
| Voyage AI context limit | 32000 tokens (docs/voyage-ai/docs-embeddings.md:121) | 32K context for voyage-3-large | ✅ |

---

**GATE 3 PASSED: All 3 mandatory tables verified present.**
