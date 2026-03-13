# GusEngine: Pre-Sale Readiness Checklist
**Objective**: Everything you must have in hand BEFORE initiating contact with any potential acquirer.

---

## Referenced Assets (Already Completed)

These documents already exist and form the foundation of your sales package:

| Document | Path | Purpose |
|:---|:---|:---|
| AI Diagnostic Whitepaper v2 | [AI_Diagnostic_WhitePaper_v2.docx (2).pdf](file:///I:/Backups/lilypixel/AI_Diagnostic_WhitePaper_v2.docx%20(2).pdf) | Technical capability overview |
| 121 Common Issues Proof | [GusEngine — 121 Common Issues.pdf](file:///I:/Backups/lilypixel/GusEngine%20%E2%80%94%20121%20Common%20Issues.pdf) | Accuracy benchmark evidence |
| Investor-Grade Whitepaper | [Investor-Grade AI Diagnostic System Whitepaper.pdf](file:///I:/Backups/lilypixel/Investor-Grade%20AI%20Diagnostic%20System%20Whitepaper.pdf) | Full business proposal |
| MVP Integrity Audit | [mvp_integrity_audit.md](file:///C:/Users/Zach/.gemini/antigravity/brain/cadf3f55-2378-4f02-b90e-6c9b5e73aa74/mvp_integrity_audit.md) | Honest engineering gap analysis |
| Investor Proposal Prompt | [investor_proposal_prompt.md](file:///C:/Users/Zach/.gemini/antigravity/brain/42a093be-655e-44ed-b045-8993c663e358/investor_proposal_prompt.md) | Deep research prompt for white paper generation |

---

## 1. PROVISIONAL PATENT APPLICATION (Critical — Do First)

> [!CAUTION]
> **The U.S. is a "first to file" jurisdiction.** If you publicly demo GusEngine without a provisional patent filed, someone could theoretically file before you. The provisional gives you a **"Patent Pending"** label and 12 months of priority.

### What to File

A **Provisional Patent Application** with the USPTO. Cost: **$320** (micro entity) or **$640** (small entity). No attorney required for filing, but recommended for claims drafting.

### Claims to Include

Based on GusEngine's novel architecture, the following are potentially patentable:

1. **Deterministic Diagnostic State Machine with RAG Grounding** — A method for generating automotive diagnostic procedures using a directed acyclic graph (DAG) state machine that constrains LLM output to structured states (Triage → Funnel → Testing → Conclusion), where each state transition requires physical verification and every diagnostic claim is traceable to a specific page in a digitized Factory Service Manual.

2. **Hybrid Tribal Knowledge Override System** — A system that layers empirically verified "master technician" knowledge atop factory service manual data in a strict authority hierarchy, where tribal knowledge entries are validated, token-budgeted, and injected into every LLM context window as overriding authority.

3. **Multi-Vehicle Diagnostic Firewall** — A pre-LLM text-based linting system that prevents cross-vehicle diagnostic contamination by detecting vehicle entity mismatches before any AI processing, using vehicle-scoped vector collections, identity injection, and per-vehicle master ledgers.

4. **Answer-Path Diagnostic Funnel** — A structured multi-choice diagnostic methodology where the AI system never asks open-ended questions but instead provides 2-5 mutually exclusive physical observation options at each decision point, forcing convergence toward a specific component-level diagnosis through elimination.

5. **Multi-Pass Self-Verification Architecture (V11)** — A method for autonomous diagnostic quality assurance in which a first LLM pass generates a diagnostic draft, a second LLM pass independently verifies the draft against four mandatory checks (complaint echo-back, differential breadth coverage, physics/logic plausibility, and test-to-component traceability), and a conditional third LLM pass automatically revises the draft to correct any failures detected by the verification pass — all without human intervention and invisible to the end user. *(Added 2026-03-13)*

6. **Cognitive Query Expansion for Mechanical System Diagnostics (Proposed)** — A pre-retrieval reasoning step in which the LLM, prior to any vector database search, generates multiple subsystem-specific search queries by reasoning about the physical systems that could produce the reported symptoms — mimicking a master mechanic's causal reasoning ("what changes between idle and highway?") rather than relying on raw semantic text similarity. Each expanded query independently searches the vector database, and results are deduplicated and merged to produce a broader retrieval context that covers subsystems a single symptom-based search would miss. *(Proposed 2026-03-13)*

7. **Deployment Integrity Verification for Distributed AI Diagnostic Systems** — An automated startup-time health verification system that cross-references a vehicle registry against a vector database, verifying that each registered diagnostic domain has a corresponding vector collection with a non-zero point count, and emitting structured health status banners with per-collection granularity — ensuring that deployment events (container rebuilds, infrastructure migrations) cannot silently degrade diagnostic coverage. *(Added 2026-03-13)*

### Innovation Changelog

| Date | Claim | Innovation | Evidence |
|:---|:---|:---|:---|
| 2026-03-13 | #5 | V11 Multi-Pass Self-Verification | Deployed, logs prove 3-pass execution with automatic revision |
| 2026-03-13 | #6 | Cognitive Query Expansion | Designed, pending implementation |
| 2026-03-13 | #7 | Deployment Integrity Verification | Deployed, logs prove 6/6 collection health check |
| | | *Future entries will be appended here* | |

### How to File

- **Option A (Cheapest)**: File yourself at [USPTO EFS-Web](https://patentcenter.uspto.gov/). Write a detailed specification (your architecture doc IS the spec). Pay $320.
- **Option B (Recommended)**: Hire a patent attorney for claims drafting only (~$2,000-4,000). They write the claims; you provide the architecture docs.
- **Timeline**: Can be done in 1-2 weeks. The provisional is intentionally loose — it establishes your filing date.

### What "Patent Pending" Gets You

- Legal priority date for 12 months
- The right to label all materials **"Patent Pending"**
- Psychological leverage in negotiations — acquirers take IP more seriously
- You have 12 months to convert to a full (non-provisional) patent

---

## 2. BUSINESS ENTITY

> [!IMPORTANT]
> You should not sell IP as an individual. The asset should be owned by a legal entity.

### What You Need

- **LLC or Corp** — If you don't already have one, form an LLC in your state. Cost: $50-150 depending on state.
- **IP Assignment Agreement** — A simple document that says "I, [Name], assign all rights to GusEngine to [LLC Name]." This makes the LLC the owner of the IP, which is what you sell.
- **EIN** — Federal tax ID for the entity. Free from IRS.gov.
- **Operating Agreement** — Even for a single-member LLC, have one on file.

---

## 3. NDA / CONFIDENTIALITY FRAMEWORK

> [!WARNING]
> **Never demo or share architecture details without a signed NDA.** The whitepapers are designed to be safe (they describe capabilities, not implementation). The architecture docs, code, and system prompt are NOT safe to share without an NDA.

> [!CAUTION]
> **The Hard Truth About NDAs**: NDAs against large corporations are *practically* unenforceable for a solo inventor. Not legally — technically they're binding. But practically: litigation costs $500K+ to pursue, they have 50 lawyers to your one, they can claim "independent development" and you'd need to prove otherwise, and by the time you'd win in court (3-5 years), the market has moved on. **The deal structure itself must be your protection, not the NDA alone.** See Section 6 (Tiered Disclosure) for how to architect this.

### What You Need

- **Mutual NDA template** — Standard 2-page mutual NDA. Covers:
  - Definition of confidential information
  - Exclusions (publicly known info)
  - Term (typically 2-3 years)
  - Remedy (injunctive relief)
- **Tiered disclosure model** (see Section 6 for full structure):
  - **Tier 1 (Pre-NDA)**: Whitepapers, 3-minute demo video, accuracy proof, public-facing materials only
  - **Tier 2 (Post-NDA, pre-LOI)**: Accuracy scorecards, live demo access (via YOUR API), financial projections — **NO architecture, NO code, NO system prompt**
  - **Tier 3 (Post-LOI + breakup fee)**: Code review in escrow, architecture docs, system prompt — **ONLY after financial commitment**

### Where to Get One

- [Cooley GO NDA Generator](https://www.cooleygo.com/documents/form-mutual-nda/) — free, VC-standard
- Or have your IP attorney draft one (~$500)

---

## 4. IP DOCUMENTATION & CLEAN ROOM AUDIT

### What Acquirers Will Ask

| Question | Your Answer | Evidence |
|:---|:---|:---|
| Who owns the code? | You (assigned to LLC) | IP Assignment Agreement |
| Any open-source license contamination? | No GPL-copyleft in core logic | Dependency audit |
| Any third-party IP claims? | No | You built it |
| Are the FSMs legally acquired? | Yes — purchased physical manuals, digitized under fair use / right-to-repair | Purchase receipts |
| Any employee/contractor IP claims? | No — sole developer | |

### What to Prepare

- [ ] **Bill of materials**: List every dependency (Qdrant, FastAPI, BGE-M3, Gemini API) with license type (Apache 2.0, MIT, etc.)
- [ ] **FSM acquisition receipts**: Keep receipts for any manuals purchased
- [ ] **Git history**: Your commit history IS your proof of authorship. Don't rewrite it.
- [ ] **No work-for-hire issues**: Confirm GusEngine was not built during employment under a contract that assigns IP to an employer

---

## 5. THE THREE-MINUTE VIDEO

### Why Three Minutes

An acquirer's first filter is a human watching a video. If they can't understand the value in 3 minutes, they won't read the whitepaper.

### Structure

| Segment | Duration | Content |
|:---|:---|:---|
| **The Problem** | 30 sec | "Master technicians are retiring. Their knowledge dies with them. The $400B repair industry runs on tribal knowledge that's never been captured." |
| **The Solution** | 30 sec | "GusEngine is an AI diagnostic engine that reasons like a master mechanic — grounded in the actual factory service manual, not guesses." |
| **Live Demo** | 90 sec | Screen recording: type a symptom → show the diagnostic funnel → follow answer paths → reach a citation-backed conclusion. **Show the FSM page citation.** |
| **The Evidence** | 15 sec | Flash the 121-query accuracy score. "100% diagnostic accuracy across 121 common issues." |
| **The Ask** | 15 sec | "This technology applies to every vehicle ever made, plus marine, aviation, heavy equipment, and military. We're exploring strategic acquisition." |

### Production Tips

- Record from the **deployed live system** (not localhost)
- Use OBS or Loom
- No music, no transitions — clean, professional, fast
- Show the **customer vehicle system** briefly (VIN dropdown → modification → query that uses the modification)
- End with the "Patent Pending" label on screen

---

## 6. DATA ROOM — TIERED DISCLOSURE MODEL

> [!CAUTION]
> **Never give a potential acquirer full backend access in a data room.** GusEngine's architecture is elegant but simple — an experienced AI engineer could understand and replicate the plumbing in 2-3 weeks. The deal structure itself must protect you. A legitimate acquirer who insists on seeing source code before an LOI is either unsophisticated or fishing.

### The Principle: Show the WHAT, Not the HOW

| ✅ Show This | ❌ Don't Show This (Until Tier 3) |
|:------------|:----------------------------------|
| Accuracy benchmarks (100% across 4 domains) | `system_prompt.txt` |
| Demo videos of live diagnostics | `parser.py` / chunking strategy |
| Multi-domain proof (car → boat → plane → tractor) | Architecture diagrams |
| Cost analysis ($0.003/query) | Qdrant collection structure |
| Patent filing summary | Source code |
| Time-to-onboard a new vehicle (<1 hour) | Overlap chunking approach |

### Tier 1 — "Teaser" (Pre-NDA)

Shared freely with any potential acquirer. Contains **zero implementation detail.**

- Investor whitepaper (capabilities, not architecture)
- 3-minute demo video
- Top-line accuracy claims ("100% across 4 domains")
- Market opportunity summary
- Patent Pending notice

### Tier 2 — "Data Room" (Post-NDA, Pre-LOI)

The standard data room. Shared after NDA is signed. Contains **proof of performance but no implementation.**

```
GusEngine_DataRoom/
├── 01_Executive/
│   ├── Investor_Whitepaper.pdf
│   ├── 3_Minute_Demo.mp4
│   └── MVP_Integrity_Audit.pdf
├── 02_Accuracy_Proof/
│   ├── Mustang_Scorecard.md          (121 issues, 100%)
│   ├── Mercedes_450SL_Scorecard.md
│   ├── MerCruiser_Marine_Scorecard.md
│   ├── Cessna_172_Scorecard.md       (101 issues)
│   ├── Ford_Tractor_Scorecard.md
│   ├── Grading_Methodology.md
│   └── Live_Demo_API_Access.txt      (they query YOUR API)
├── 03_Domain_Breadth/
│   ├── Multi_Domain_Summary.pdf      (automotive, marine, aviation, agriculture)
│   └── Onboarding_Speed_Evidence.pdf (new vehicle in <1 hour)
├── 04_Legal/
│   ├── Patent_Pending_Receipt.pdf
│   ├── Patent_Claims_Summary.pdf     (claims, NOT implementation)
│   ├── IP_Assignment_Agreement.pdf
│   ├── Dependency_Licenses.md
│   └── FSM_Purchase_Receipts/
├── 05_Financial/
│   ├── Operating_Cost_Analysis.pdf   ($0.003/query)
│   ├── Revenue_Projections.xlsx
│   └── Comparable_Transactions.md
└── [NO CODE. NO ARCHITECTURE. NO SYSTEM PROMPT.]
```

### Tier 3 — "Technical Due Diligence" (Post-LOI + Breakup Fee + Escrow)

> [!IMPORTANT]
> Code access happens **only after** the buyer has signed a Letter of Intent that includes a **breakup fee** ($50K-$250K). This makes "steal it and walk" financially and legally costly.

This tier is conducted under controlled conditions:

- **Code goes into third-party escrow** (Iron Mountain, Harbinger, or equivalent)
- Their engineers review in a supervised, read-only environment
- No file copies, no USB drives, no screenshots
- Breakup fee is forfeited if they walk away after accessing this tier

Tier 3 contents:

```
[ESCROW — Read-Only Access]
├── Architecture_Overview.pdf
├── System_Prompt.txt
├── Source_Code/
│   └── [Full repository snapshot]
├── Vector_DB_Schema.md
└── Deployment_Runbook.md
```

### Why This Model Works

This three-tier model is **standard practice** in tech IP/asset sales. It exists precisely because:

1. NDAs alone are insufficient protection against well-resourced acquirers
2. The breakup fee creates real financial consequences for bad-faith access
3. Third-party escrow prevents unauthorized copying
4. A legitimate buyer will accept this — anyone who pushes back is a red flag

---

## 7. THE SIMPLICITY PARADOX — Protecting Elegant Architecture

> [!WARNING]
> GusEngine's greatest strength is also its greatest vulnerability: the architecture is simple enough that a competent AI engineer could replicate the *plumbing* in 2-3 weeks.

### What's Actually Simple

At its core, GusEngine is: PDF → chunked embeddings → vector search → structured prompt → LLM → diagnostic state machine. That's it.

### What's NOT Simple (Your Real Value)

1. **The system prompt is distilled expertise, not code.** Months of iteration across 4+ domains tuned the diagnostic phases, answer-path structure, and failure handling. A competitor starting fresh would spend the same months rediscovering every edge case.

2. **The proof is the moat.** You have validated 100% accuracy across automotive, marine, aviation, and agriculture — 4 completely unrelated domains. Nobody else has this proof. The insight that "this simple approach actually produces mechanic-grade diagnostics" is non-obvious.

3. **The validation methodology is proprietary.** The 100-issue databases with expert-verified fixes, paraphrase variants, LLM-as-judge grading — that's test infrastructure worth real money.

4. **Time advantage compounds.** You're live, validated, and multi-domain today. Even if they started replicating after seeing the architecture, they're 6+ months from proving it works.

### The Google Analogy

PageRank was a simple algorithm — literally a matrix multiplication. Any grad student could replicate it. But Google was worth billions because they **proved it worked at scale**, they got there **first**, and the insight was non-obvious before they demonstrated it.

GusEngine is in the same position. The buyer isn't paying for complexity — they're paying for:
- A validated, working solution they didn't build
- The patent rights to prevent competitors
- The 6-12 month head start over anyone who starts today
- The insight that simplicity IS the product (it scales trivially to any new domain)

### Strategic Positioning

Frame the simplicity as a feature, not a weakness:

> *"GusEngine can onboard any mechanical system with a factory service manual in under one hour, with zero model fine-tuning and zero domain-specific training. This means every vehicle, vessel, aircraft, and piece of heavy equipment ever manufactured is an addressable market — with no additional R&D cost per vehicle."*

That's not a vulnerability. That's a scaling story worth billions.

---

## 8. LEGAL COUNSEL

> [!IMPORTANT]
> You need ONE attorney, not a firm. Look for a solo practitioner or small firm specializing in **IP transactions / tech M&A**.

### What They Do

- Draft or review the NDA
- File the provisional patent (or review your self-filed one)
- Review the asset purchase agreement when a buyer makes an offer
- Advise on deal structure (asset sale vs. equity sale vs. licensing)
- **Draft the LOI with breakup fee clause** (critical for Tier 3 protection)
- **Set up third-party code escrow** for technical due diligence

### Budget

- Provisional patent filing: $2,000-4,000
- NDA review: $500
- LOI with breakup fee clause: $1,500-3,000
- Code escrow setup: $1,000-2,000
- Asset purchase agreement review: $3,000-7,000
- **Total pre-sale legal budget: ~$8,000-16,000**

### Finding One

- [USPTO Patent Attorney Search](https://oedci.uspto.gov/OEDCI/) — find registered patent attorneys in your area
- Alternatively, ask for referrals from local tech startup networks or SCORE mentors

---

## 9. EXECUTION ORDER (Timeline)

| Week | Action | Cost |
|:---|:---|:---|
| **Week 1** | Form LLC (if not done), get EIN | $50-150 |
| **Week 1** | Execute IP Assignment Agreement (self → LLC) | $0 |
| **Week 1-2** | File provisional patent (self or attorney) | $320-4,000 |
| **Week 2** | Prepare Mutual NDA template | $0-500 |
| **Week 2** | Run dependency license audit | $0 |
| **Week 2-3** | Record 3-minute demo video | $0 |
| **Week 3** | Assemble Tier 1 + Tier 2 data room (NO code/architecture) | $0 |
| **Week 3** | Identify and retain IP attorney | $500 retainer |
| **Week 3** | Research code escrow providers (Iron Mountain, EscrowTech) | $0 |
| **Week 4** | **Ready to initiate contact** | |

> [!TIP]
> **Total minimum budget to be "sale-ready": ~$500-1,000** (self-filed patent + LLC formation). With attorney for full LOI/escrow setup: ~$8,000-16,000.

---

## Do NOT Do Before Filing the Provisional

- ❌ Post the demo video publicly
- ❌ Share the architecture document with anyone (even under NDA — file first)
- ❌ Write about the system on social media with technical details
- ❌ Open-source any component

**File the provisional patent FIRST. Everything else follows.**
