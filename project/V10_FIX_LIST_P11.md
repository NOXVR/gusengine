# V10 Phase 11 — Fix List

**Source:** P11_HOSTILE_AUDIT_FINDINGS.md (6th auditor)
**Total Findings:** 14 (1 withdrawn = 13 actionable)
**Subtractive:** 0

> [!CAUTION]
> Two more import regressions. P11-01 is another 8th instance of the same systemic
> failure class — `ingest_pdf_background` used at line 1184 but never imported.
> P11-03 is the same class as P8-02 — `logger` used throughout `main.py` with no
> `import logging`.

---

## CRITICAL (2) — Apply one at a time

| ID | Type | Summary | Impact |
|:---|:-----|:--------|:-------|
| P11-01 | `[ADDITIVE]` | Add `from backend.ingestion.pipeline import ingest_pdf_background` to `ingest.py` | NameError on every POST /api/ingest |
| P11-03 | `[ADDITIVE]` | Add `import logging` + `logger` to `main.py` startup hook | NameError at startup → crash |

## SIGNIFICANT (6) — Apply 3 at a time

| ID | Type | Summary |
|:---|:-----|:--------|
| P11-02 | `[CORRECTIVE]` | `ensure_qdrant_collection()` read probe should use `qdrant_ingest_client` |
| P11-05 | `[CORRECTIVE]` | Budget diagram: add "no chat" scenario line |
| P11-06 | `[CORRECTIVE]` | Add `RuntimeError` to embed client exception handler |
| P11-07 | `[CORRECTIVE]` | Add `RuntimeError` to LLM client exception handler |
| P11-09 | `[CORRECTIVE]` | Validator: replace static FRAMEWORK_OVERHEAD=250 with dynamic formula |
| P11-12 | `[CORRECTIVE]` | Frontend healthcheck: don't follow redirect, check for 301 directly |

## MINOR (5)

| ID | Type | Summary |
|:---|:-----|:--------|
| P11-04 | `[CORRECTIVE]` | Remove dead `UnexpectedResponse` import in `main.py` |
| P11-08 | `[CORRECTIVE]` | Move `_get_client()` call inside try block in `embed_text()` |
| P11-10 | `[CORRECTIVE]` | Remove dead `qdrant_client` import in `ingest.py` |
| P11-13 | `[CORRECTIVE]` | Move SEPARATOR_TOKENS to module scope (perf) |
| P11-14 | `[CORRECTIVE]` | Consolidate parser.py imports at module level |
| P11-15 | `[ADDITIVE]` | Add client separation documentation comment to `clients.py` |
