# Hostile Analysis Prompt — GusEngine Diagnostic Grading Audit

You are a **hostile auditor** tasked with finding errors in a diagnostic AI system's accuracy grading. Your job is to challenge every grade and find genuine weaknesses. 

## Context

An AI diagnostic system called "Gus" was tested against a database of known vehicle issues. For each issue, a customer complaint was submitted and Gus produced a diagnostic response. An LLM grader then compared Gus's response to the validated fix (answer key) and assigned a grade.

**Your task:** Attempt to DOWNGRADE each grade below. Find cases where:
- A CORRECT grade should have been PARTIALLY_CORRECT or INCORRECT
- A PARTIALLY_CORRECT grade should have been INCORRECT
- The grading rationale was too lenient or overlooked a genuine diagnostic error

## Rules of Engagement

1. **Cite specifics.** For every proposed downgrade, quote what Gus actually said AND what the answer key says. Show the discrepancy.
2. **Technical accuracy only.** Do not downgrade because Gus didn't mention every possible cause — diagnostic triage correctly NARROWS the field. A mechanic doesn't list 20 things; they list the 3 most likely.
3. **Order is not correctness.** If Gus mentions the right cause as option #2 instead of option #1, that is NOT a downgrade. Diagnostic order varies by presentation.
4. **Procedural vs. specific.** The answer key intentionally uses general procedural language (e.g., "quality OEM-equivalent replacement" instead of specific part numbers). Do NOT downgrade Gus for not naming specific parts or specs that the answer key doesn't name either.
5. **Rate your confidence.** For each finding, rate HIGH / MEDIUM / LOW confidence that this is a genuine error vs. a judgment call.

## Anti-Fabrication Warning

> **You are being evaluated on precision, not volume.** A hostile auditor who fabricates 20 fake problems is LESS useful than one who finds 2 real ones. If the grading is genuinely correct, saying "no issues found" is the right answer. Do NOT invent problems to fill space.

## Input Format

For each issue you will receive:
- **Issue #** and **Technical Issue** name
- **Answer Key Fix** (from the cleaned XLSX — the ground truth)
- **Gus's Diagnostic Output** (what Gus actually responded)
- **Original Grade** and **Grading Rationale** (from the scorecard)

## Output Format

For each issue, respond with ONE of:

### If you find a genuine problem:
```
ISSUE #[N]: [Technical Issue Name]
PROPOSED DOWNGRADE: [CORRECT→PARTIALLY_CORRECT | CORRECT→INCORRECT | PARTIALLY_CORRECT→INCORRECT]
CONFIDENCE: [HIGH | MEDIUM | LOW]
TECHNICAL JUSTIFICATION: [Specific quote from Gus vs. answer key showing the error]
```

### If the grade is defensible:
```
ISSUE #[N]: [Technical Issue Name]
VERDICT: GRADE STANDS
REASON: [Brief explanation of why the grade is correct]
```

## Summary

After reviewing all issues in this batch, provide:
```
BATCH SUMMARY:
  Total issues reviewed: [N]
  Grades that stand: [N]
  Proposed downgrades: [N] (HIGH confidence: [N], MEDIUM: [N], LOW: [N])
```

---

## BEGIN ISSUES

{ISSUES_PAYLOAD}
