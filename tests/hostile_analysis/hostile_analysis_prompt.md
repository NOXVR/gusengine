# Hostile Analysis — Browser Prompt

Copy this prompt into Claude / ChatGPT / Gemini. Upload the files listed for your vehicle.

---

## Files to Upload

Upload ALL files for a single vehicle at once:

1. **Answer Key** (CSV) — the ground-truth validated fixes
2. **Scorecard** (MD) — the grading results  
3. **Gus Output Parts** (TXT) — Gus's diagnostic outputs, split into ~25-query chunks

Upload ALL gus_diagnostic_output_part*.txt files for the vehicle — each part covers a different set of queries.

---

## Prompt (copy everything below this line)

---

I am uploading files for a hostile accuracy audit of an AI diagnostic system called "Gus." Here is what each file is:

**Answer Key (CSV):** A database of known mechanical issues. The "Validated Fixes" column contains the ground-truth repair procedure for each issue — cleaned to use general procedural language, deferring to the factory service manual for exact specifications.

**Scorecard (MD):** The grading results. For each issue, a customer complaint was submitted to Gus, and an LLM grader compared Gus's response to the answer key and assigned a grade:
- **CORRECT** — Gus's diagnostic path leads to the validated fix
- **PARTIALLY_CORRECT** — Gus's path is reasonable but misses the primary cause
- **INCORRECT** — Gus's path is wrong
- **NOT_APPLICABLE** — Out of scope

The scorecard reports 100% accuracy (counting PARTIALLY_CORRECT as pass). Your job is to challenge this.

**Gus Output (TXT parts):** Gus's actual diagnostic responses in JSON format. Each entry contains:
- `query_id` — matches the scorecard's Query ID column
- `technical_issue` — the issue name
- `query_text` — the customer complaint submitted  
- `response_parsed.diagnostic_reasoning` — Gus's reasoning
- `response_parsed.mechanic_instructions` — what Gus told the mechanic
- `response_parsed.answer_path_prompts` — the diagnostic options Gus presented
- `response_parsed.source_citations` — FSM sources Gus referenced
- `branch_id` / `branch_path` / `turn` — position in the diagnostic decision tree

Some queries have multiple entries (BFS decision tree branches). The **first entry** for each query_id (branch_id 0, turn 0) is the initial triage — this is what was graded. Subsequent entries show follow-up branches.

## Your Task: Hostile Audit

You are a **hostile auditor**. For every graded issue, compare:
1. What the **answer key** says the fix should be (CSV "Validated Fixes" column)
2. What **Gus actually said** (TXT files — response_parsed)
3. What **grade was given** and **why** (scorecard)

Then determine: **Does the grade hold, or should it be downgraded?**

## Rules

1. **Cite specifics.** For every proposed downgrade, quote what Gus said vs. what the answer key says.
2. **Technical accuracy only.** Don't downgrade because Gus didn't list every possible cause — diagnostic triage correctly narrows the field.
3. **Order is not correctness.** If Gus listed the right cause as option #2 instead of #1, that's NOT wrong.
4. **The answer key is procedural.** It uses generic language ("per the service manual"). Don't fault Gus for not naming things the answer key doesn't name.
5. **Anti-fabrication warning: You are being evaluated on PRECISION, not volume.** A hostile auditor who invents 20 fake problems is less useful than one who finds 2 real ones. If the grading is genuinely correct, say so. Do NOT invent problems to fill space.

## Output Format

For EVERY graded issue (skip NOT_APPLICABLE), output one of:

**If the grade should be downgraded:**
```
ISSUE #[N]: [Issue Name]
CURRENT GRADE: [grade]
PROPOSED DOWNGRADE: [new grade]
CONFIDENCE: [HIGH / MEDIUM / LOW]
EVIDENCE: [Quote from Gus vs. answer key showing the discrepancy]
```

**If the grade holds:**
```
ISSUE #[N]: [Issue Name]
VERDICT: GRADE STANDS
```

At the end, provide:
```
HOSTILE AUDIT SUMMARY
=====================
Total issues reviewed: [N]
Grades that stand: [N]
Proposed downgrades: [N]
  - HIGH confidence: [N]
  - MEDIUM confidence: [N]  
  - LOW confidence: [N]
Original accuracy: [X]%
Proposed adjusted accuracy: [Y]%
```
