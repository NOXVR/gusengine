# V10 Phase 11 — Deep Think Fix List

**Source:** FINDING-P11-01_ Fatal Import Regression... (7th auditor)
**Total Findings:** 4 (2 duplicates, 2 new)

---

## Duplicate Findings (SKIP)

| Auditor ID | Matches | Status |
|:-----------|:--------|:-------|
| DT-P11-01 | P11-01 (ingest_pdf_background import) | ✅ Already applied |
| DT-P11-03 | P11-03 (logger in main.py) | ✅ Already applied |

---

## New Findings (2)

### CRITICAL (1)

| ID | Type | Summary |
|:---|:-----|:--------|
| DT-P11-02 | `[ADDITIVE]` | Docling layout models (`ds4sd/docling-models`) not pre-downloaded; `HF_HUB_OFFLINE=1` blocks download → first PDF parse crashes |

### ⚠️ MINOR — SUBTRACTIVE (1)

| ID | Type | Summary |
|:---|:-----|:--------|
| DT-P11-04 | `[SUBTRACTIVE]` | Dead `import DOMPurify from 'dompurify'` — never called since P4-04 switched to `.textContent`. Removal also requires removing `npm install dompurify` from setup script. |

> [!CAUTION]
> **DT-P11-04 is `[SUBTRACTIVE]`.** Per workflow rules, this requires explicit user approval.
> - **What will be deleted:** `import DOMPurify from 'dompurify'` statement and `npm install dompurify` command
> - **What depends on it:** Nothing. DOMPurify.sanitize() is never called. All XSS defense is via `.textContent`.
> - **What breaks:** Nothing functional. The dead import just wastes ~50KB bundle size.
> - **Auditor rationale:** Valid. P4-04 eliminated all innerHTML usage; DOMPurify is orphaned.
