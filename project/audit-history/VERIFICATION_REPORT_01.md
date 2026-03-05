# Verification Report — Analysis #01 (Claude Opus 4.6)

**Verifier:** Antigravity (local)
**Date:** 2026-02-16
**Source Analysis:** RAW_ANALYSIS_01_CLAUDE_OPUS.md
**Analysis Total:** 20 item checks (all PASS) + 7 cross-cutting audits → 2 blocking findings + 2 observations

---

## Finding 1/2: F-DNA-1 — DNA Overflow Proof Uses Stale 600-Token Value

**Auditor's Claim:** DNA line 715 states `600 (system prompt)` in its overflow proof. V9 uses `750`. The overflow proof total (3,475) and remaining (525) are wrong. Correct values: 3,625 total, 375 remaining.

**V9 Actual (lines 1253, 983):**
- Line 1253: `System Prompt: ~750 tokens (V9: +150 from R-1 through R-4 restorations)` ← V9 uses 750
- Line 983: `remaining = 4000 - 750 - count` ← code uses 750

**DNA Actual (lines 677, 693-696, 715-717):**
- Line 677: `~600 tokens` (in diagram)
- Line 693: `TOTAL INPUT: ~3,475 tokens` (in diagram)
- Line 694: `RESPONSE: ~525 tokens remaining` (in diagram)
- Line 696: `MARGIN: ~325 tokens safety buffer` (in diagram)
- Line 715: `600 (system prompt) + 1,275 (ledger cap) + 1,600 (RAG max) = 3,475`
- Line 716: `4,000 - 3,475 = 525 tokens remaining for response`
- Line 717: `Gus JSON output ≈ 200 tokens → 325 token safety buffer ✓`

**Reproduction:** CONFIRMED. I verified independently:
- 750 + 1,275 + 1,600 = 3,625 (not 3,475)
- 4,000 - 3,625 = 375 remaining (not 525)
- Gus JSON ~200 tokens → 175 safety buffer (not 325)

**Genealogy:**
- **V8 era:** `PROJECT_DNA_COMPLETE.md` (Phase 8, line 703) correctly used 600 — system prompt WAS ~600 tokens
- **CF-4 change:** V9's `validate_ledger.py` and Phase 7 checklist updated from 600→750
- **DNA V9 update session:** (conversation `1201e560`) updated DNA header and many references to V9, but the overflow proof block (lines 715-717) and the diagram block (lines 677, 693-696) were NOT updated
- **Not intentional.** This is a sync miss during the DNA V9 update pass.

**ADDITIONAL SCOPE:** Auditor identified line 715 only. My verification found the SAME stale values in the diagram block (lines 677, 693, 694, 696) — a total of 7 stale values across 2 blocks. All must be updated together.

**Verdict:** ✅ CONFIRMED
**Rationale:** (1) Bug reproduced — values are factually wrong. (2) Genealogy shows this is NOT intentional — it's a sync miss from the CF-4 update. (3) Fix is safe — updating 7 numeric values in the DNA document, zero blast radius.

---

## Finding 2/2: F-SEC-1 — VIN-Lookup Missing encodeURIComponent

**Auditor's Claim:** VIN-Lookup `handler.js` (V9 line 1613) interpolates `vin` directly into the NHTSA URL without `encodeURIComponent()`. Purchase-Router (line 1649) correctly uses encoding. Pattern inconsistency and defense-in-depth gap.

**V9 Actual (lines 1607-1620):**
- Line 1610: `if (!vin || vin.length < 5) return "Error: Invalid VIN.";` — length check
- Line 1611: `if (vin.length < 17)` — classic chassis bypass
- Line 1613: `fetch(\`.../${vin}?format=json\`)` — raw interpolation, NO `encodeURIComponent()`

**Purchase-Router Actual (line 1649):**
- `const query = encodeURIComponent(\`${vehicle_data}...\`)` — HAS encoding

**Reproduction:** CONFIRMED. The code uses raw `${vin}` interpolation in the URL. A 17+ character string containing `?`, `#`, `&`, or `/` would corrupt the fetch URL. No character validation exists — only length checks.

**Genealogy:**
- **VFINAL Part 2 (line 102):** Original handler — NEVER had `encodeURIComponent()`. This is the original design.
- **V3 (Phase 4, line 1357):** Same code, no encoding. Survived all V3-V8 hostile audits undetected.
- **Gap Analysis (Phase 8, `07_AGENT_SKILLS.md` line 37):** Described the handler but did NOT flag missing encoding.
- **V9 recovery:** Character-identical copy from VFINAL. Fidelity audit confirmed verbatim match.
- **Claude Deep Reasoning validation:** `CLAUDE_DEEP_REASONING_FINDINGS.md` line 300 — **previously flagged as CF-6 (🟡 LOW severity)**. Recommended `encodeURIComponent(vin)`. Was NOT applied during pre-hostile-audit fixes because classified LOW.
- **Purchase-Router:** Has `encodeURIComponent()` since VFINAL (line 165). Creates pattern inconsistency.
- **Not intentional.** VFINAL author omitted encoding likely because real VINs are alphanumeric. But defense-in-depth requires encoding regardless of expected input format.

**Practical Risk Assessment:** LOW exploitation probability (real VINs are alphanumeric, NHTSA is a public read-only API) but violates zero-tolerance engineering standard. The fix is trivial, zero blast radius, and aligns the VIN-Lookup with the Purchase-Router pattern.

**Verdict:** ✅ CONFIRMED
**Rationale:** (1) Bug reproduced — raw interpolation with no character validation. (2) Genealogy shows NOT intentional — original VFINAL oversight, NOT a design choice. (3) Fix is safe — single-line change, zero blast radius, pattern-consistent with Purchase-Router.

---

## Analysis #01 Summary

| Finding | Verdict | Severity | Fix Scope |
|---------|---------|----------|-----------|
| F-DNA-1 (stale token values in DNA) | ✅ CONFIRMED | CRITICAL | 7 values across 2 blocks in DNA |
| F-SEC-1 (missing encodeURIComponent) | ✅ CONFIRMED | SIGNIFICANT | 1 line in V9 architecture |

**Non-blocking observations (no action required):**
- F-TOK-1: System prompt may be ~800 tokens vs claimed ~750. Budget holds in both cases. Post-deployment verification addresses this.
- F-DNA-2: preprocess_markdown_tables active voice vs dormant annotation. Documentation nuance, not a contradiction.

**2/2 CONFIRMED. 0 DISPUTED. 0 NEEDS-HUMAN.**
