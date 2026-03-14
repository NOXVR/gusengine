# Hostile Analysis — Browser Prompt (Per Vehicle)

Copy this prompt into Claude / ChatGPT / Gemini. Upload the 3 files listed below.

---

## Files to Upload

For **each vehicle**, upload these 3 files:

### 1965 Ford Mustang
1. `1965_Ford_Mustang_Issues_Cleaned.xlsx` — The answer key (100+ known issues with validated fixes)
2. `accuracy_scorecard.md` — The grading results (each issue graded CORRECT / PARTIALLY_CORRECT / INCORRECT)
3. `run_20260309_163545.jsonl` — Gus's raw diagnostic outputs (what the AI actually said)

### 1976 Mercedes 450SL
1. `1976_Mercedes_450SL_Issues_Cleaned.xlsx`
2. `accuracy_scorecard_450sl.md`
3. `run_20260311_190826.jsonl`

### MerCruiser 5.0/5.7
1. `MerCruiser_5.0_5.7_Issues_Cleaned.xlsx`
2. `accuracy_scorecard_mercruiser.md`
3. `run_20260311_225329.jsonl`

### Cessna 172 Skyhawk
1. `Cessna_172_Skyhawk_Issues_Cleaned.xlsx`
2. `accuracy_scorecard_cessna172.md`
3. `run_20260312_133607.jsonl`

---

## Prompt (copy below this line)

---

I am attaching 3 files for your review. Here is what each one is:

**File 1 — The Answer Key (XLSX):**
This spreadsheet contains a database of known mechanical issues for [VEHICLE NAME]. Column H ("Validated Fixes") contains the ground-truth repair procedure for each issue. These fixes have been cleaned to remove specific part numbers, brand names, and torque specs — they describe the correct *procedure* in general terms, deferring to the factory service manual for exact specifications.

**File 2 — The Grading Scorecard (MD):**
This is the result of grading an AI diagnostic system called "Gus" against the answer key. For each issue, a customer complaint was submitted to Gus, and Gus produced a diagnostic response. An LLM grader then compared Gus's response to the answer key and assigned a grade:
- **CORRECT** — Gus's diagnostic path leads to the validated fix
- **PARTIALLY_CORRECT** — Gus's path is reasonable but doesn't directly target the primary cause
- **INCORRECT** — Gus's path is wrong
- **NOT_APPLICABLE** — Issue was outside scope (vehicle mismatch, cosmetic, etc.)

The scorecard shows a 100% diagnostic accuracy across all applicable queries. Your job is to challenge this.

**File 3 — Gus's Raw Output (JSONL):**
This contains Gus's actual diagnostic responses in JSON format. Each line is one diagnostic interaction. Key fields:
- `query_id` — matches the scorecard's Query ID column
- `response_parsed.diagnostic_reasoning` — Gus's reasoning
- `response_parsed.mechanic_instructions` — what Gus told the mechanic to do
- `response_parsed.answer_path_prompts` — the diagnostic options Gus presented

Note: The JSONL contains multiple entries per query_id (BFS decision tree branches). The **first entry** for each query_id is the initial triage — this is what was graded.

---

## Your Task: Hostile Audit

You are a **hostile auditor**. Your job is to find cases where the grading was **too lenient**. For every graded issue, compare:
1. What the **answer key** says the fix should be (XLSX Column H)
2. What **Gus actually said** (JSONL response_parsed)
3. What **grade was given** and **why** (scorecard)

Then determine: **Does the grade hold, or should it be downgraded?**

## Rules

1. **Cite specifics.** For every proposed downgrade, quote what Gus said vs. what the answer key says.
2. **Technical accuracy only.** Don't downgrade because Gus didn't list every possible cause — diagnostic triage correctly narrows the field.
3. **Order is not correctness.** If Gus put the right cause as option #2 instead of #1, that's NOT wrong.
4. **The answer key is procedural.** It intentionally uses generic language ("per the service manual"). Don't fault Gus for not naming things the answer key doesn't name.
5. **Anti-fabrication warning: You are being evaluated on PRECISION, not volume.** A hostile auditor who invents 20 fake problems is less useful than one who finds 2 real ones. If the grading is genuinely correct, say so. Do NOT invent problems to fill space.

## Output Format

For EVERY graded issue (skip NOT_APPLICABLE), output one of:

**If the grade should be downgraded:**
```
ISSUE #[N]: [Issue Name]
CURRENT GRADE: [CORRECT or PARTIALLY_CORRECT]
PROPOSED DOWNGRADE: [new grade]
CONFIDENCE: [HIGH / MEDIUM / LOW]
EVIDENCE: [Quote from Gus's output vs. quote from answer key showing the discrepancy]
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
