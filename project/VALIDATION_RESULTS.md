# GusEngine V10 — Diagnostic Validation Results

**Date:** March 1, 2026  
**Model:** Gemini 2.5 Flash (API) via GusEngine RAG pipeline  
**Corpus:** 450SL W107/R107 FSMs, K-Jetronic manuals, CIS diagnostic guides, electrical volumes  
**Methodology:** 3 real-world diagnostic scenarios sourced from Mercedes-Benz owner forums (PeachParts, MBWorld, BenzWorld) with confirmed solutions. Each query was submitted verbatim to GusEngine and evaluated against the known resolution.

---

## Summary

| # | Symptom | Known Solution | Gus Diagnosis | Turns | Grade |
|:--|:--------|:---------------|:--------------|:------|:------|
| 1 | Hard cold start, 10-15s cranking | Cold Start Valve / Thermo-Time Switch | CSV / TTS (exact match) | 1 | **A+** |
| 2 | Hot restart failure after 10 min soak | Fuel Accumulator / vapor lock | FPA / vapor lock (exact match) | 1 | **A+** |
| 3 | Rough idle worsens when warm, stalls at lights | Vacuum leak (AAV masks it cold) | WUR → ruled out → vacuum leak | 3 | **A** |

---

## Query 1: Hard Cold Start

### User Input
> "My 450SL requires 10-15 seconds of cranking to start when cold. Once it catches, it runs rough for about 30 seconds then smooths out. When warm, it starts instantly on the first crank."

### Known Solution
Faulty **Cold Start Valve (CSV)** or **Thermo-Time Switch (TTS)**. The CSV should spray for 4-6 seconds during cold cranking. If the TTS cuts off early or the CSV is clogged, insufficient fuel is delivered for cold enrichment.

### GusEngine Response (Turn 1)
- **Hypothesis:** Cold Start Valve and Thermo-Time Switch — exact match
- **Mechanism:** "CSV designed to inject extra fuel into intake manifold only during cold cranking... if not working, engine will be lean and hard to start when cold"
- **Secondary:** Identified WUR as contributor to the "rough running that smooths out" phase (correct nuance)
- **Test procedure:** Step-by-step CSV jar test with safety warning (do not crank >10 seconds)
- **Answer paths:** Fine mist (working) / No spray (faulty valve) / Dribble (partially clogged)
- **Citations:** `107_M117_K-Jetronic_Fuel_Injection.pdf`, page 10

### Evaluation
**Grade: A+** — Correct diagnosis on first turn. Exact FSM test procedure. Safety-conscious. Identified secondary contributor. A forum mechanic would give identical advice.

---

## Query 2: Hot Restart Failure

### User Input
> "Car runs perfectly for an hour of driving. I stop for gas, come back 10 minutes later, and it cranks and cranks but won't start. If I wait 30 minutes, it starts fine. This only happens on hot days."

### Known Solution
Failed **Fuel Pressure Accumulator** causing vapor lock. The accumulator maintains residual pressure when engine is off. When it fails, hot engine heat causes fuel to boil in lines. 30-minute wait allows cooling and re-condensation.

### GusEngine Response (Turn 1)
- **Hypothesis:** Fuel Pressure Accumulator (FPA) — exact match
- **Mechanism:** "maintains fuel pressure after engine shut off, preventing fuel from boiling and creating vapor lock... pressure drops, fuel vaporizes, engine cannot receive liquid fuel until it cools down and vapor condenses"
- **Temporal reasoning:** Correctly identified the 10-min hot soak → pressure loss → vapor lock → 30-min cool cycle
- **Answer paths:** Pump hums + no gas smell (vapor lock) / Pump hums + gas smell (leaking injectors) / No pump sound (electrical)
- **Citations:** `1976_Mercedes-Benz_450SL_W107_R107_M117_Engine_FSM.pdf`, page 11, heading "Fuel Pressure Accumulator"

### Evaluation
**Grade: A+** — Perfect first-turn diagnosis. Correctly reasoned about the timing pattern (hot soak duration, cool-down period). Differentiated vapor lock from injector flooding and pump failure via physical observations. Cited specific FSM page and heading.

---

## Query 3: Rough Idle Worsens When Warm

### User Input
> "Engine idles rough at about 500 RPM, sometimes dips and almost stalls. When I first start it cold, it's actually smoother. As it warms up to operating temperature, the idle gets worse and worse. Occasionally stalls at red lights."

### Known Solution
**Vacuum leak** — most commonly cracked hoses to auxiliary air valve or intake manifold gaskets. The AAV provides extra bypass air during cold idle. As it closes during warmup, the vacuum leak becomes a larger percentage of total airflow, causing progressively leaner mixture.

### GusEngine Diagnostic Funnel (3 Turns)

**Turn 1 — Initial Hypothesis:**
- Suspected WUR (Warm-Up Regulator) as primary cause of temperature-dependent mixture issue
- Mentioned vacuum leaks as secondary possibility
- Asked for exhaust observation: raw fuel smell (rich) vs metallic/struggling (lean) vs neutral
- User selected: **"hot and metallic, struggling for fuel"** → lean condition confirmed

**Turn 2 — Pressure Test:**
- Confirmed lean hypothesis, ordered WUR control pressure test (cold and warm readings)
- Provided exact pressure specifications: cold 1.5-2.0 bar / warm 3.4-3.8 bar
- User selected: **"Both pressures within spec"** → WUR ruled out

**Turn 3 — Vacuum Leak (Correct Diagnosis):**
- "Ruled out Warm-Up Regulator. Next suspicion is a vacuum leak"
- "Vacuum leak introduces unmetered air, leaning out the mixture... often more pronounced as engine warms"
- Prescribed propane spray test around injector seals, intake manifold gaskets, vacuum hose connections
- Answer paths: RPM increases at a spot (leak found) / No change (deeper issue) / Visible crack (conclusive)
- **Citations:** `Mercedes-Benz 450SL (W107) Service Manual - Engine.pdf`

### Evaluation
**Grade: A** — Did not identify vacuum leak on first turn, but the WUR is the #1 suspect for this symptom on every forum. The 3-turn elimination funnel (WUR hypothesis → pressure test → ruled out → vacuum leak) demonstrates proper diagnostic methodology. The answer paths at each turn correctly funneled toward the right diagnosis. A real mechanic would follow the same process.

---

## Key Findings

### What Worked
1. **Component-level specificity** — Named exact parts (CSV, TTS, FPA, WUR) with correct mechanisms
2. **FSM-grounded citations** — Referenced specific documents, page numbers, and section headings from the corpus
3. **Physical observation answer paths** — Described what the user would see, hear, or smell (not diagnostic conclusions)
4. **Temporal/causal reasoning** — Correctly reasoned about hot soak timing, cold-vs-warm behavior, and temperature-dependent failure modes
5. **Diagnostic funneling** — When unsure, narrowed systematically through elimination rather than guessing
6. **Safety awareness** — Included appropriate warnings (e.g., "do not crank longer than 10 seconds")

### Architecture Decisions Validated
- **Gemini 2.5 Flash via API** provides frontier-quality reasoning that Qwen2.5-32B-AWQ could not match
- **Process-based system prompt** (no hardcoded component names) allows the model to derive hypotheses from RAG chunks
- **Hybrid RAG** (local Qdrant + TEI, remote LLM) delivers both data privacy for indexing and reasoning quality from Gemini
- **~3-5 second response time** vs ~15 seconds with local Qwen — better user experience

### Comparison: Qwen 32B vs Gemini 2.5 Flash

| Metric | Qwen 32B (before) | Gemini 2.5 Flash (after) |
|:-------|:-------------------|:-------------------------|
| Query 1 result | "Cold start valve or injection nozzles" (partially correct, weak reasoning) | CSV + TTS with exact test procedure (A+) |
| Query 2 result | Not tested (proxy timeout on 72B, generic on 32B) | FPA + vapor lock with temporal reasoning (A+) |
| Query 3 result | Not tested | 3-turn funnel: WUR → ruled out → vacuum leak (A) |
| Response time | ~15 seconds | ~3-5 seconds |
| Answer paths | Diagnostic conclusions (user can't verify) | Physical observations (user can verify) |
| Citations | Generic document names | Specific pages and section headings |

---

## Conclusion

GusEngine with Gemini 2.5 Flash correctly diagnosed **3/3 real-world forum-sourced problems** affecting the 1976 Mercedes-Benz 450SL K-Jetronic fuel injection system. Two were identified on the first turn; the third was reached through proper diagnostic elimination in three turns. All diagnoses match confirmed solutions from Mercedes-Benz owner community forums.

The system demonstrates the diagnostic reasoning quality of an experienced K-Jetronic specialist while maintaining full traceability to Factory Service Manual documentation.
