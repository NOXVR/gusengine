# V10 Phase 10 — Third Auditor Fix List

**Source:** AUDIT_P10_FINDINGS.md (Third Auditor)
**Total Findings:** 9 (all valid, 0 duplicates)
**Subtractive:** 0

> [!CAUTION]
> Findings P10-22, P10-23, P10-24 are **regressions introduced by prior P10 fixes**.
> P10-04 added `threading.Lock()` to llm.py without `import threading`.
> P10-17 added `os.environ.get()` to client.py without `import os`.
> P10-20 added `threading.Lock()` to pipeline.py without `import threading`.
> All three crash the application at startup — **system completely inoperable**.

---

## CRITICAL (4) — Apply one at a time

| ID | Type | Summary | Impact |
|:---|:-----|:--------|:-------|
| P10-22 | `[ADDITIVE]` | Add `import threading` to `llm.py` | Startup crash — NameError |
| P10-23 | `[ADDITIVE]` | Add `import os` to `client.py` | Startup crash — NameError |
| P10-24 | `[ADDITIVE]` | Add `import threading` to `pipeline.py` | Startup crash — NameError |
| P10-25 | `[CORRECTIVE]` | Wire `qdrant_ingest_client` into `ingest.py` for writes/cleanup | Thread safety defeated |

## SIGNIFICANT (3) — Apply 3 at a time

| ID | Type | Summary |
|:---|:-----|:--------|
| P10-26 | `[CORRECTIVE]` | Add `_manifest_lock` to partial-failure manifest write in `ingest_pdf()` |
| P10-28 | `[ADDITIVE]` | Add Docker healthcheck to frontend container |
| P10-30 | `[ADDITIVE]` | Close Qdrant clients in `cleanup_clients()` shutdown handler |

## MINOR (2)

| ID | Type | Summary |
|:---|:-----|:--------|
| P10-27 | `[CORRECTIVE]` | Fix budget comment to include `user_query_tokens` (~50) |
| P10-29 | `[CORRECTIVE]` | Use `qdrant_ingest_client` for `create_collection` in startup hook |
