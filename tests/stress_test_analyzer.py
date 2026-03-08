"""
GusEngine Stress Test Analyzer v3 — Decision Tree Forensics
=============================================================
Reads JSONL logs and generates a forensic accuracy/consistency report.

NEW in v2:
  - Determinism analysis (identical query repeats)
  - Paraphrase consistency (same scenario, different wording)
  - Component-level diagnosis stability scoring
  - Response fingerprint drift tracking
  - Full failure forensics with response diffs

Usage:
    python stress_test_analyzer.py --input results/run_*.jsonl
    python stress_test_analyzer.py --input results/run_*.jsonl --output results/report.md
"""
import argparse
import glob
import json
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime


def load_entries(input_patterns: list[str]) -> list[dict]:
    entries = []
    for pattern in input_patterns:
        for path in sorted(glob.glob(pattern)):
            with open(path, "r", encoding="utf-8") as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        entries.append(json.loads(line))
                    except json.JSONDecodeError:
                        print(f"WARNING: Skipping malformed line in {path}:{line_num}")
    return entries


def jaccard_similarity(set_a: set, set_b: set) -> float:
    """Jaccard index between two sets (0.0 = disjoint, 1.0 = identical)."""
    if not set_a and not set_b:
        return 1.0
    union = set_a | set_b
    if not union:
        return 1.0
    return len(set_a & set_b) / len(union)


def analyze(entries: list[dict], output_path: str | None = None):
    if not entries:
        print("No entries to analyze.")
        return

    # Root entries = depth 1, branch 0 (the initial query per conversation)
    root_entries = [e for e in entries if e.get("turn") == 1 and e.get("branch_id", 0) == 0]
    # All turn-1 entries (includes branch roots at depth>1)
    turn1 = [e for e in entries if e.get("turn") == 1]
    follow_ups = [e for e in entries if e.get("turn", 1) > 1]
    branch_entries = [e for e in entries if e.get("branch_id", 0) > 0]

    lines = []
    def p(text=""):
        lines.append(text)
        print(text)

    p("# GusEngine Forensic Stress Test Report")
    p()
    p(f"**Generated:** {datetime.now().isoformat()}")
    p(f"**Total interactions:** {len(entries)} ({len(root_entries)} root queries, {len(branch_entries)} branch explorations, {len(follow_ups)} follow-ups)")
    run_ids = sorted(set(e.get("run_id", "?") for e in entries))
    p(f"**Run IDs:** {', '.join(run_ids)}")
    repeats_used = max(e.get("repeat_num", 1) for e in entries)
    p(f"**Repeat factor:** {repeats_used}x")
    has_paraphrases = any(e.get("scenario_id") for e in entries)
    p(f"**Paraphrase groups:** {'YES' if has_paraphrases else 'NO'}")
    has_trees = any(e.get("branch_id", 0) > 0 for e in entries)
    p(f"**Decision tree exploration:** {'YES' if has_trees else 'NO'}")
    p()

    # ═══════════════════════════════════════════
    # 1. OVERALL GRADES
    # ═══════════════════════════════════════════
    p("## 1. Overall Grade Summary")
    p()
    grade_counts = Counter(e.get("grade", "?") for e in root_entries)
    total_t1 = len(root_entries) if root_entries else 1
    p("| Grade | Count | Pct |")
    p("|:------|------:|----:|")
    for grade in ["PASS", "PARTIAL", "FAIL", "BEHAVIORAL_PASS", "BEHAVIORAL_WARN",
                  "BEHAVIORAL_FAIL", "ADVERSARIAL_PASS", "ADVERSARIAL_FAIL", "ADVERSARIAL_NEUTRAL"]:
        c = grade_counts.get(grade, 0)
        if c > 0:
            p(f"| **{grade}** | {c} | {c/total_t1*100:.1f}% |")
    for grade, c in sorted(grade_counts.items()):
        if grade not in ["PASS", "PARTIAL", "FAIL", "BEHAVIORAL_PASS", "BEHAVIORAL_WARN",
                         "BEHAVIORAL_FAIL", "ADVERSARIAL_PASS", "ADVERSARIAL_FAIL", "ADVERSARIAL_NEUTRAL"]:
            p(f"| {grade} | {c} | {c/total_t1*100:.1f}% |")
    p()

    # ═══════════════════════════════════════════
    # 2. SYSTEM COVERAGE
    # ═══════════════════════════════════════════
    p("## 2. System Coverage")
    p()
    systems = defaultdict(lambda: {"total": 0, "pass": 0, "partial": 0, "fail": 0})
    for e in root_entries:
        s = e.get("query_system", "Unknown")
        if s in ("Adversarial", ""):
            continue
        systems[s]["total"] += 1
        g = e.get("grade", "")
        if "PASS" in g and "FAIL" not in g:
            systems[s]["pass"] += 1
        elif "PARTIAL" in g or "WARN" in g:
            systems[s]["partial"] += 1
        elif "FAIL" in g:
            systems[s]["fail"] += 1

    p("| System | Total | Pass | Partial | Fail | Rate |")
    p("|:-------|------:|-----:|--------:|-----:|-----:|")
    for s in sorted(systems):
        d = systems[s]
        rate = d["pass"] / d["total"] * 100 if d["total"] else 0
        p(f"| {s} | {d['total']} | {d['pass']} | {d['partial']} | {d['fail']} | {rate:.0f}% |")
    p()

    # ═══════════════════════════════════════════
    # 3. DETERMINISM ANALYSIS (identical repeats)
    # ═══════════════════════════════════════════
    p("## 3. Determinism Analysis (Identical Query Repeats)")
    p()
    if repeats_used <= 1:
        p("*No repeat data — run with `--repeat N` to enable this analysis.*")
    else:
        # Group root entries by query_id (only branch 0 for determinism)
        by_query = defaultdict(list)
        for e in root_entries:
            by_query[e.get("query_id", "?")].append(e)

        determinism_scores = []
        unstable_queries = []

        for qid, group in sorted(by_query.items()):
            if len(group) < 2:
                continue
            # Compare fingerprints
            fingerprints = [e.get("response_fingerprint", "") for e in group]
            unique_fps = set(fingerprints)
            fp_stability = 1.0 if len(unique_fps) == 1 else 1.0 / len(unique_fps)

            # Compare DAG states
            states = [e.get("current_state", "") for e in group]
            state_stable = len(set(states)) == 1

            # Compare components mentioned
            comp_sets = [set(e.get("components_mentioned", [])) for e in group]
            comp_jaccard_scores = []
            for i in range(len(comp_sets)):
                for j in range(i + 1, len(comp_sets)):
                    comp_jaccard_scores.append(jaccard_similarity(comp_sets[i], comp_sets[j]))
            avg_comp_jaccard = sum(comp_jaccard_scores) / len(comp_jaccard_scores) if comp_jaccard_scores else 1.0

            # Compare grades
            grades = [e.get("grade", "") for e in group]
            grade_stable = len(set(grades)) == 1

            score = (fp_stability + (1.0 if state_stable else 0.0) + avg_comp_jaccard + (1.0 if grade_stable else 0.0)) / 4
            determinism_scores.append(score)

            if score < 0.9:
                unstable_queries.append({
                    "query_id": qid,
                    "score": score,
                    "states": states,
                    "grades": grades,
                    "fingerprints": fingerprints,
                    "query_text": group[0].get("query_text", "")[:80],
                })

        if determinism_scores:
            avg_det = sum(determinism_scores) / len(determinism_scores)
            perfect = sum(1 for s in determinism_scores if s >= 1.0)
            p(f"**Average determinism score:** {avg_det:.3f} (1.0 = perfectly identical)")
            p(f"**Perfectly stable queries:** {perfect}/{len(determinism_scores)} ({perfect/len(determinism_scores)*100:.0f}%)")
            p(f"**Unstable queries (< 0.9):** {len(unstable_queries)}")
            p()

            if unstable_queries:
                p("### Unstable Queries")
                p()
                p("| Query | Score | States | Grades |")
                p("|:------|------:|:-------|:-------|")
                for uq in sorted(unstable_queries, key=lambda x: x["score"]):
                    p(f"| {uq['query_id']} | {uq['score']:.2f} | {', '.join(uq['states'])} | {', '.join(uq['grades'])} |")
                p()
    p()

    # ═══════════════════════════════════════════
    # 4. PARAPHRASE CONSISTENCY
    # ═══════════════════════════════════════════
    p("## 4. Paraphrase Consistency (Same Problem, Different Words)")
    p()
    if not has_paraphrases:
        p("*No paraphrase data — run with `--paraphrases` to enable this analysis.*")
    else:
        by_scenario = defaultdict(list)
        for e in root_entries:
            sid = e.get("scenario_id")
            if sid:
                by_scenario[sid].append(e)

        para_scores = []
        inconsistent = []

        for sid, group in sorted(by_scenario.items()):
            if len(group) < 2:
                continue

            # State consistency
            states = [e.get("current_state", "") for e in group]
            state_consistent = len(set(states)) == 1

            # Component consistency (are the same components being diagnosed?)
            comp_sets = [set(e.get("components_mentioned", [])) for e in group]
            j_scores = []
            for i in range(len(comp_sets)):
                for j in range(i + 1, len(comp_sets)):
                    j_scores.append(jaccard_similarity(comp_sets[i], comp_sets[j]))
            avg_j = sum(j_scores) / len(j_scores) if j_scores else 1.0

            # Subsystem consistency
            sub_sets = [set(e.get("intersecting_subsystems", [])) for e in group]
            sub_j_scores = []
            for i in range(len(sub_sets)):
                for j in range(i + 1, len(sub_sets)):
                    sub_j_scores.append(jaccard_similarity(sub_sets[i], sub_sets[j]))
            avg_sub_j = sum(sub_j_scores) / len(sub_j_scores) if sub_j_scores else 1.0

            # Grade consistency
            grades = [e.get("grade", "") for e in group]
            grade_consistent = len(set(grades)) == 1

            score = ((1.0 if state_consistent else 0.3) + avg_j + avg_sub_j + (1.0 if grade_consistent else 0.3)) / 4
            para_scores.append(score)

            if score < 0.85:
                inconsistent.append({
                    "scenario_id": sid,
                    "score": score,
                    "states": states,
                    "component_jaccard": avg_j,
                    "subsystem_jaccard": avg_sub_j,
                    "queries": [e.get("query_text", "")[:60] for e in group],
                    "components": [list(cs) for cs in comp_sets],
                })

        if para_scores:
            avg_para = sum(para_scores) / len(para_scores)
            perfect = sum(1 for s in para_scores if s >= 0.95)
            p(f"**Average paraphrase consistency:** {avg_para:.3f} (1.0 = identical diagnosis)")
            p(f"**Highly consistent scenarios:** {perfect}/{len(para_scores)}")
            p(f"**Inconsistent scenarios (< 0.85):** {len(inconsistent)}")
            p()

            if inconsistent:
                p("### Inconsistent Scenarios")
                p()
                for item in sorted(inconsistent, key=lambda x: x["score"]):
                    p(f"#### {item['scenario_id']} (score: {item['score']:.2f})")
                    p(f"States: {item['states']}")
                    p(f"Component overlap: {item['component_jaccard']:.2f}")
                    for i, q in enumerate(item["queries"]):
                        p(f"- Variant {i+1}: \"{q}\" → components: {item['components'][i]}")
                    p()
    p()

    # ═══════════════════════════════════════════
    # 5. LATENCY
    # ═══════════════════════════════════════════
    p("## 5. Latency Report")
    p()
    lats = sorted(e.get("latency_ms", 0) for e in entries if e.get("latency_ms", 0) > 0)
    if lats:
        n = len(lats)
        p("| Metric | Value |")
        p("|:-------|------:|")
        p(f"| Requests | {n} |")
        p(f"| Average | {sum(lats)/n:.0f}ms |")
        p(f"| p50 | {lats[int(n*0.5)]:.0f}ms |")
        p(f"| p90 | {lats[int(n*0.9)]:.0f}ms |")
        p(f"| p99 | {lats[min(int(n*0.99), n-1)]:.0f}ms |")
        p(f"| Min | {min(lats):.0f}ms |")
        p(f"| Max | {max(lats):.0f}ms |")
    p()

    # ═══════════════════════════════════════════
    # 6. STATE TRANSITIONS & CONVERSATION DEPTH
    # ═══════════════════════════════════════════
    p("## 6. State Transitions & Depth")
    p()
    state_counts = Counter(e.get("current_state", "?") for e in entries)
    p("| State | Count |")
    p("|:------|------:|")
    for s, c in state_counts.most_common():
        p(f"| {s} | {c} |")
    p()
    conv_turns = defaultdict(int)
    for e in entries:
        cid = e.get("conversation_id", "?")
        conv_turns[cid] = max(conv_turns[cid], e.get("turn", 1))
    turn_dist = Counter(conv_turns.values())
    p("| Max Turns | Conversations |")
    p("|----------:|--------------:|")
    for t in sorted(turn_dist):
        p(f"| {t} | {turn_dist[t]} |")
    p()

    # ═══════════════════════════════════════════
    # 7. DECISION TREE EXPLORATION
    # ═══════════════════════════════════════════
    p("## 7. Decision Tree Exploration")
    p()
    if not has_trees:
        p("*No tree data — the runner explores branches automatically when Gus offers answer_path_prompts.*")
    else:
        # Group by query_id + repeat to get trees
        trees = defaultdict(list)
        for e in entries:
            tree_key = f"{e.get('query_id', '?')}_r{e.get('repeat_num', 1)}"
            trees[tree_key].append(e)

        tree_sizes = []
        tree_depths = []
        terminal_states_in_trees = []
        for tree_key, tree_entries in trees.items():
            branches = set(e.get("branch_id", 0) for e in tree_entries)
            tree_sizes.append(len(branches))
            max_depth = max(e.get("turn", 1) for e in tree_entries)
            tree_depths.append(max_depth)
            for e in tree_entries:
                if e.get("current_state") in ("PHASE_D_CONCLUSION",):
                    terminal_states_in_trees.append(tree_key)

        p(f"**Total decision trees explored:** {len(trees)}")
        p(f"**Total branches explored:** {sum(tree_sizes)}")
        p(f"**Trees reaching CONCLUSION:** {len(set(terminal_states_in_trees))}/{len(trees)}")
        p()
        p("| Metric | Value |")
        p("|:-------|------:|")
        p(f"| Avg branches/tree | {sum(tree_sizes)/len(tree_sizes):.1f} |")
        p(f"| Max branches in one tree | {max(tree_sizes)} |")
        p(f"| Avg max depth | {sum(tree_depths)/len(tree_depths):.1f} |")
        p(f"| Max depth reached | {max(tree_depths)} |")
        p()

        # Branch terminal states
        branch_terminals = Counter()
        for e in entries:
            if e.get("branch_id", 0) > 0:
                state = e.get("current_state", "")
                if state in ("PHASE_D_CONCLUSION", "PHASE_ERROR", "RETRIEVAL_FAILURE"):
                    branch_terminals[state] += 1
        if branch_terminals:
            p("### Branch Terminal States")
            p()
            p("| State | Count |")
            p("|:------|------:|")
            for s, c in branch_terminals.most_common():
                p(f"| {s} | {c} |")
        p()

        # Tree grade distribution (how many branches per tree pass/fail)
        p("### Branch-Level Grade Distribution (follow-up turns)")
        p()
        branch_grades = Counter(e.get("grade", "?") for e in entries if e.get("branch_id", 0) > 0)
        if branch_grades:
            p("| Grade | Count |")
            p("|:------|------:|")
            for g, c in branch_grades.most_common():
                p(f"| {g} | {c} |")
        p()
    p()

    # ═══════════════════════════════════════════
    # 8. JSON/SCHEMA COMPLIANCE
    # ═══════════════════════════════════════════
    p("## 8. JSON & Schema Compliance")
    p()
    valid_json = sum(1 for e in entries if e.get("response_valid_json"))
    valid_state = sum(1 for e in entries if e.get("response_valid_state"))
    total = len(entries)
    p(f"- Valid JSON: {valid_json}/{total} ({valid_json/total*100:.1f}%)")
    p(f"- Valid DAG state: {valid_state}/{total} ({valid_state/total*100:.1f}%)")
    p()

    # ═══════════════════════════════════════════
    # 9. RAG CONTEXT & FAILURE FORENSICS
    # ═══════════════════════════════════════════
    p("## 9. RAG Context & Failure Forensics")
    p()

    # Failure origin analysis
    retrieval_failures = [e for e in entries if e.get("current_state") == "RETRIEVAL_FAILURE"]
    if retrieval_failures:
        p("### RETRIEVAL_FAILURE Origin Analysis")
        p()
        origin_counts = Counter(e.get("failure_origin", "UNKNOWN") for e in retrieval_failures)
        p("| Origin | Count | Meaning |")
        p("|:-------|------:|:--------|")
        labels = {
            "SEARCH_EMPTY": "Qdrant returned 0 chunks (embedding/search failure)",
            "LLM_HALLUCINATION": "LLM said failure despite having RAG context",
            "UNKNOWN": "Old API without rag_context (can't determine)",
        }
        for origin, count in origin_counts.most_common():
            p(f"| **{origin}** | {count} | {labels.get(origin, '?')} |")
        p()

    # RAG coverage stats
    entries_with_rag = [e for e in entries if e.get("rag_chunk_count") is not None]
    if entries_with_rag:
        p("### RAG Coverage")
        p()
        chunk_counts = [e.get("rag_chunk_count", 0) for e in entries_with_rag]
        token_counts = [e.get("rag_tokens_used", 0) for e in entries_with_rag]
        zero_chunks = sum(1 for c in chunk_counts if c == 0)
        p("| Metric | Value |")
        p("|:-------|------:|")
        p(f"| Responses with RAG data | {len(entries_with_rag)}/{len(entries)} |")
        p(f"| Avg chunks/response | {sum(chunk_counts)/len(chunk_counts):.1f} |")
        p(f"| Max chunks/response | {max(chunk_counts)} |")
        p(f"| Zero-chunk responses | {zero_chunks} ({zero_chunks/len(entries_with_rag)*100:.0f}%) |")
        p(f"| Avg RAG tokens/response | {sum(token_counts)/len(token_counts):.0f} |")
        p()

    # Source diversity from RAG context
    all_rag_sources = []
    for e in entries_with_rag:
        for s in e.get("rag_sources", []):
            src = s.get("source", "")
            if src:
                all_rag_sources.append(src)
    if all_rag_sources:
        p("### RAG Source Diversity")
        p()
        source_freq = Counter(all_rag_sources)
        p(f"- Unique sources cited by Qdrant: {len(source_freq)}")
        p("- Most referenced sources:")
        for src, count in source_freq.most_common(10):
            p(f"  - {src}: {count} times")
    p()

    # ═══════════════════════════════════════════
    # 10. COMPONENT DIAGNOSIS FREQUENCY
    # ═══════════════════════════════════════════
    p("## 10. Component Diagnosis Frequency")
    p()
    all_components = []
    for e in turn1:
        all_components.extend(e.get("components_mentioned", []))
    if all_components:
        comp_freq = Counter(all_components)
        p("| Component | Times Mentioned |")
        p("|:----------|----------------:|")
        for comp, count in comp_freq.most_common(20):
            p(f"| {comp} | {count} |")
    p()

    # ═══════════════════════════════════════════
    # 11. FAILURE CATALOG
    # ═══════════════════════════════════════════
    p("## 11. Failure Catalog")
    p()
    failures = [e for e in root_entries if e.get("grade") in ("FAIL", "BEHAVIORAL_FAIL", "ADVERSARIAL_FAIL")]
    if failures:
        for f_entry in failures:
            p(f"### {f_entry.get('query_id')} — {f_entry.get('grade')}")
            p(f"- **Query:** {f_entry.get('query_text', '')[:120]}")
            p(f"- **State:** {f_entry.get('current_state')}")
            p(f"- **Detail:** {f_entry.get('grade_detail', '')}")
            misses = f_entry.get("keyword_misses", [])
            if misses:
                p(f"- **Missing keywords:** {', '.join(misses)}")
            instructions = f_entry.get("mechanic_instructions", "")[:200]
            if instructions:
                p(f"- **Gus said:** {instructions}")
            p(f"- **Fingerprint:** {f_entry.get('response_fingerprint', 'N/A')}")
            p()
    else:
        p("No failures recorded. 🎉")
    p()

    # Write report
    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"\nReport written to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="GusEngine Stress Test Analyzer v3")
    parser.add_argument("--input", nargs="+", required=True)
    parser.add_argument("--output", help="Output report path (default: auto)")
    args = parser.parse_args()

    entries = load_entries(args.input)
    print(f"Loaded {len(entries)} log entries\n")

    if not args.output:
        results_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
        os.makedirs(results_dir, exist_ok=True)
        args.output = os.path.join(results_dir, f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md")

    analyze(entries, args.output)


if __name__ == "__main__":
    main()
