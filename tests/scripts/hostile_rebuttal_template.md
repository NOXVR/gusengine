# Hostile Finding Rebuttal Template

Use this template to evaluate each finding from the hostile analysis.

## For Each Hostile Finding:

### 1. Is it TECHNICALLY VALID?
Does the finding cite a **real** technical error in Gus's diagnostic?
- YES: Gus said something factually wrong or prescribed an incorrect procedure
- NO: Gus's response is technically sound, the auditor is applying unreasonable standards

### 2. Is it a REASONABLE EXPECTATION?
Would a **real mechanic** in a shop agree that Gus's response was inadequate?
- YES: A working mechanic would say "that's wrong" or "that misses the obvious cause"
- NO: Only an LLM trying to find fault would flag this — a mechanic would say "yeah, that works"

### 3. Is it FABRICATED SPECIFICITY?
Is the auditor demanding something that **the answer key itself doesn't require?**
- YES: The auditor is demanding specific part numbers, exact sequences, or exhaustive lists that the answer key doesn't contain
- NO: The auditor is pointing to a genuinely missing diagnostic step or incorrect reasoning

### 4. VERDICT
- **ACCEPT** → Genuine issue. Update the scorecard and adjust accuracy.
- **REJECT** → Fabricated or unreasonable. Document why and move on.
- **INVESTIGATE** → Plausible but needs domain expert review. Flag for manual check.

---

## Rebuttal Log

| Finding # | Issue # | Proposed Downgrade | Confidence | Technically Valid? | Reasonable? | Fabricated Specificity? | Verdict |
|-----------|---------|-------------------|------------|-------------------|-------------|------------------------|---------|
| 1 | | | | | | | |
| 2 | | | | | | | |
| ... | | | | | | | |

## Final Tally

- Total hostile findings: ___
- ACCEPTED: ___ (genuine issues that change accuracy)
- REJECTED: ___ (fabricated or unreasonable)
- INVESTIGATE: ___ (need further review)
- **Adjusted accuracy: ___%**
