# V10 Phase 11 — Opus 4.6 Fix List (8th Auditor)

**Source:** P11_AUDIT_FINDINGS.md (8th auditor — Opus 4.6)
**Total Findings:** 6 (2 duplicates, 4 new)

---

## Duplicate Findings (SKIP)

| Auditor ID | Matches | Status |
|:-----------|:--------|:-------|
| P11-01 | Our P11-01 (ingest_pdf_background import) | ✅ Already applied |
| P11-02 | Our P11-10 (dead qdrant_client import) | ✅ Already applied |

---

## New Findings (4)

### SIGNIFICANT (1)

| ID | Type | Summary |
|:---|:-----|:--------|
| OP-P11-03 | `[CORRECTIVE]` | Gusengine `start_period: 60s` doesn't cover ~303s max startup retry loop |

### MINOR (3)

| ID | Type | Summary |
|:---|:-----|:--------|
| OP-P11-04 | `[CORRECTIVE]` | Validator `remaining_no_chat` omits user query tokens — refines P11-09 |
| OP-P11-05 | `[CORRECTIVE]` | Backup cron stops only gusengine, not frontend → 502s during window |
| OP-P11-06 | `[ADDITIVE]` | `hybrid_search` type hint `query_sparse: dict` should be `Optional[dict]` |
