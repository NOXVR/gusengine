"""
GusEngine Stress Test Runner v3 — Full Decision Tree Exploration
=================================================================
Fires diagnostic queries at the live GusEngine API, then explores
EVERY branch of the diagnostic decision tree by forking on each
answer_path_prompt Gus offers.

Key behaviors:
  - Initial query → Gus returns N answer_path_prompts
  - Runner forks into N separate conversation branches
  - Each branch follows its own path to PHASE_D_CONCLUSION (or dead end)
  - Every branch is logged as a separate conversation thread
  - --repeat N runs the entire tree N times for determinism testing
  - --paraphrases tests same scenario with different wording

Tree exploration is BFS with configurable limits:
  --max-branches    Max total branches per query (default 12)
  --max-depth       Max conversation depth (default 5)

Usage:
    python stress_test_runner.py --api-url http://5.78.132.233:8888 --limit 5
    python stress_test_runner.py --api-url http://5.78.132.233:8888 --mode full
"""
import argparse
import json
import os
import sys
import time
import uuid
import glob
import hashlib
from collections import deque
from datetime import datetime, timezone

try:
    import requests
except ImportError:
    print("ERROR: 'requests' package required. Install with: pip install requests")
    sys.exit(1)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CORPUS_PATH = os.path.join(SCRIPT_DIR, "stress_test_corpus.json")
RESULTS_DIR = os.path.join(SCRIPT_DIR, "results")

CONTINUABLE_STATES = {"PHASE_A_TRIAGE", "PHASE_B_FUNNEL", "PHASE_C_TESTING"}
TERMINAL_STATES = {"PHASE_D_CONCLUSION", "PHASE_ERROR", "RETRIEVAL_FAILURE", "VEHICLE_MISMATCH"}


def load_corpus(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def response_fingerprint(parsed: dict) -> str:
    key_fields = {
        "current_state": parsed.get("current_state", ""),
        "mechanic_instructions": parsed.get("mechanic_instructions", ""),
        "diagnostic_reasoning": parsed.get("diagnostic_reasoning", ""),
        "intersecting_subsystems": sorted(parsed.get("intersecting_subsystems", [])),
        "answer_path_count": len(parsed.get("answer_path_prompts", [])),
    }
    return hashlib.sha256(json.dumps(key_fields, sort_keys=True).encode()).hexdigest()[:16]


def extract_components_mentioned(text: str) -> list[str]:
    components = [
        "carburetor", "choke", "accelerator pump", "float", "needle valve",
        "fuel pump", "fuel filter", "fuel line", "distributor", "ignition coil",
        "condenser", "points", "spark plug", "rotor", "cap",
        "starter", "solenoid", "alternator", "generator", "voltage regulator",
        "battery", "ignition switch", "neutral safety switch",
        "master cylinder", "wheel cylinder", "brake drum", "brake shoe",
        "thermostat", "water pump", "radiator", "fan", "heater core",
        "head gasket", "valve seal", "piston ring", "bearing",
        "oil pump", "oil filter", "PCV valve",
        "governor", "modulator", "valve body", "torque converter", "band",
        "ball joint", "tie rod", "steering box", "shock absorber", "spring",
        "exhaust manifold", "muffler",
    ]
    text_lower = text.lower()
    return [c for c in components if c in text_lower]


def grade_response(query: dict, parsed: dict, is_adversarial: bool) -> tuple[str, str, list, list]:
    state = parsed.get("current_state", "UNKNOWN")
    if is_adversarial:
        expected_state = query.get("expected_state")
        if expected_state:
            if state == expected_state:
                return "ADVERSARIAL_PASS", f"Correctly returned {state}", [], []
            return "ADVERSARIAL_FAIL", f"Expected {expected_state}, got {state}", [], []
        if state not in ("PHASE_ERROR", "UNKNOWN"):
            return "ADVERSARIAL_PASS", f"Handled gracefully with state {state}", [], []
        return "ADVERSARIAL_NEUTRAL", f"Returned {state}", [], []

    keywords = query.get("known_answer_keywords", query.get("expected_keywords", []))
    if not keywords:
        if state in CONTINUABLE_STATES | TERMINAL_STATES:
            has_cit = len(parsed.get("source_citations", [])) > 0
            if has_cit or state in ("PHASE_ERROR", "RETRIEVAL_FAILURE"):
                return "BEHAVIORAL_PASS", f"Valid state {state}", [], []
            return "BEHAVIORAL_WARN", f"State {state}, no citations", [], []
        return "BEHAVIORAL_FAIL", f"Invalid state: {state}", [], []

    response_text = json.dumps(parsed).lower()
    hits = [kw for kw in keywords if kw.lower() in response_text]
    misses = [kw for kw in keywords if kw.lower() not in response_text]
    if state in ("RETRIEVAL_FAILURE", "PHASE_ERROR"):
        return "FAIL", f"{state}", hits, misses
    ratio = len(hits) / len(keywords) if keywords else 1.0
    if ratio >= 0.75:
        return "PASS", f"{len(hits)}/{len(keywords)} kw", hits, misses
    if ratio >= 0.4:
        return "PARTIAL", f"{len(hits)}/{len(keywords)} kw", hits, misses
    return "FAIL", f"{len(hits)}/{len(keywords)} kw", hits, misses


def send_chat(api_url: str, message: str, vehicle_id: str,
              chat_history: list[dict], timeout: int = 120) -> tuple[dict, float, str, dict, dict]:
    """Send a chat request. Returns (parsed_response, latency_ms, raw_response, http_meta, rag_context)."""
    payload = {"message": message, "vehicle_id": vehicle_id, "chat_history": chat_history}
    start = time.perf_counter()
    http_meta = {"status_code": 0, "content_length": 0, "error": None}
    try:
        resp = requests.post(f"{api_url}/api/chat", json=payload, timeout=timeout)
        latency_ms = (time.perf_counter() - start) * 1000
        http_meta["status_code"] = resp.status_code
        http_meta["content_length"] = len(resp.content)
        resp.raise_for_status()
        data = resp.json()
        raw = data.get("response", "{}")
        rag_context = data.get("rag_context", {})
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            parsed = {"current_state": "PARSE_ERROR", "raw": raw[:500]}
        return parsed, latency_ms, raw, http_meta, rag_context
    except requests.exceptions.Timeout:
        latency_ms = (time.perf_counter() - start) * 1000
        http_meta["error"] = "TIMEOUT"
        return {"current_state": "TIMEOUT"}, latency_ms, "", http_meta, {}
    except requests.exceptions.ConnectionError as e:
        latency_ms = (time.perf_counter() - start) * 1000
        http_meta["error"] = str(e)[:200]
        return {"current_state": "CONNECTION_ERROR"}, latency_ms, "", http_meta, {}
    except Exception as e:
        latency_ms = (time.perf_counter() - start) * 1000
        http_meta["error"] = str(e)[:200]
        return {"current_state": "RUNNER_ERROR"}, latency_ms, "", http_meta, {}


def write_log_entry(log_file, entry: dict):
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def build_log_entry(run_id, query_id, scenario_id, repeat_num, branch_id, branch_path,
                    turn, message, query_meta, vehicle_id, chat_history,
                    parsed, latency_ms, raw, http_meta, rag_context,
                    grade, grade_detail, kw_hits, kw_misses):
    """Build a complete atomic log entry with RAG context forensics."""
    # Compute citation source from RAG context (the real citations Qdrant found)
    rag_sources = rag_context.get("sources", [])
    rag_chunk_count = rag_context.get("chunk_count", 0)
    rag_tokens = rag_context.get("total_tokens_used", 0)

    # Forensic: if LLM said RETRIEVAL_FAILURE but RAG found chunks, that's an LLM problem
    current_state = parsed.get("current_state", "UNKNOWN")
    failure_origin = None
    if current_state == "RETRIEVAL_FAILURE":
        if rag_chunk_count > 0:
            failure_origin = "LLM_HALLUCINATION"  # LLM said failure despite having context
        elif rag_context:  # We have rag_context field but chunk_count is 0
            failure_origin = "SEARCH_EMPTY"  # Search returned nothing
        else:
            failure_origin = "UNKNOWN"  # Old API without rag_context
    return {
        "run_id": run_id,
        "query_id": query_id,
        "conversation_id": f"{query_id}_r{repeat_num}_b{branch_id}",
        "scenario_id": scenario_id,
        "repeat_num": repeat_num,
        "branch_id": branch_id,
        "branch_path": branch_path,
        "turn": turn,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "query_text": message,
        "query_category": query_meta.get("category", ""),
        "query_system": query_meta.get("system", ""),
        "query_difficulty": query_meta.get("difficulty", ""),
        "vehicle_id": vehicle_id,
        "chat_history_length": len(chat_history),
        "response_raw": raw,
        "response_parsed": parsed,
        "response_fingerprint": response_fingerprint(parsed),
        "response_valid_json": parsed.get("current_state") != "PARSE_ERROR",
        "response_valid_state": parsed.get("current_state", "") in CONTINUABLE_STATES | TERMINAL_STATES,
        "current_state": parsed.get("current_state", "UNKNOWN"),
        "has_citations": len(parsed.get("source_citations", [])) > 0,
        "citation_count": len(parsed.get("source_citations", [])),
        "citations": parsed.get("source_citations", []),
        "has_answer_paths": len(parsed.get("answer_path_prompts", [])) > 0,
        "answer_path_count": len(parsed.get("answer_path_prompts", [])),
        "answer_paths": parsed.get("answer_path_prompts", []),
        "intersecting_subsystems": parsed.get("intersecting_subsystems", []),
        "components_mentioned": extract_components_mentioned(json.dumps(parsed)),
        "mechanic_instructions": parsed.get("mechanic_instructions", ""),
        "diagnostic_reasoning": parsed.get("diagnostic_reasoning", ""),
        "latency_ms": round(latency_ms, 1),
        "http_status": http_meta["status_code"],
        "response_bytes": http_meta["content_length"],
        "http_error": http_meta["error"],
        "grade": grade,
        "grade_detail": grade_detail,
        "keyword_hits": kw_hits,
        "keyword_misses": kw_misses,
        # RAG context forensics
        "rag_chunk_count": rag_chunk_count,
        "rag_tokens_used": rag_tokens,
        "rag_sources": rag_sources,
        "failure_origin": failure_origin,
    }


def explore_decision_tree(api_url: str, vehicle_id: str, query_id: str, query_text: str,
                          query_meta: dict, run_id: str, repeat_num: int,
                          log_file: str, delay: float, follow_ups: list = None,
                          scenario_id: str = None, max_branches: int = 12, max_depth: int = 5):
    """
    Explore the FULL decision tree for a query using BFS.

    For each turn, Gus may offer N answer_path_prompts. We fork into
    N branches, each continuing as a separate conversation. This produces
    a tree of conversations, all logged individually.

    Returns total number of API calls made.
    """
    is_adversarial = query_meta.get("category") == "adversarial"
    available_follow_ups = list(follow_ups or [])
    api_calls = 0

    # BFS queue items: (branch_id, branch_path_list, chat_history, depth)
    # branch_path_list tracks which choices were taken: ["root", "choice_1_of_3", ...]
    queue = deque()
    queue.append((0, ["root"], [], 1))
    next_branch_id = 1

    while queue and next_branch_id <= max_branches:
        branch_id, branch_path, chat_history, depth = queue.popleft()

        if depth > max_depth:
            continue

        # Determine the message for this turn
        if depth == 1:
            message = query_text
        else:
            # The message is embedded in the branch_path — it's the last choice text
            message = branch_path[-1]

        # Send to API
        parsed, latency_ms, raw, http_meta, rag_context = send_chat(api_url, message, vehicle_id, chat_history)
        api_calls += 1
        current_state = parsed.get("current_state", "UNKNOWN")

        # Grade (only turn-1 gets keyword grading; follow-up turns get structural grading)
        if depth == 1:
            grade, grade_detail, kw_hits, kw_misses = grade_response(query_meta, parsed, is_adversarial)
        else:
            # Grade follow-up turns: check for valid state and citations
            if current_state in CONTINUABLE_STATES | TERMINAL_STATES:
                has_cit = len(parsed.get("source_citations", [])) > 0
                grade = "TREE_PASS" if has_cit else "TREE_NOCITE"
            else:
                grade = "TREE_ERROR"
            grade_detail = f"depth={depth} state={current_state}"
            kw_hits, kw_misses = [], []

        # Build and write log entry
        path_str = " > ".join(branch_path)
        entry = build_log_entry(
            run_id, query_id, scenario_id, repeat_num, branch_id, path_str,
            depth, message, query_meta, vehicle_id, chat_history,
            parsed, latency_ms, raw, http_meta, rag_context,
            grade, grade_detail, kw_hits, kw_misses,
        )
        write_log_entry(log_file, entry)

        # Print progress (ASCII-safe for Windows cp1252)
        icon = {"PASS": "+", "ADVERSARIAL_PASS": "+", "BEHAVIORAL_PASS": "+",
                "TREE_PASS": "+", "PARTIAL": "~", "BEHAVIORAL_WARN": "~",
                "TREE_NOCITE": "~"}.get(grade, "X")
        indent = "  " * depth
        r_tag = f"R{repeat_num}" if repeat_num > 1 else ""
        branch_tag = f"B{branch_id}" if branch_id > 0 else "root"
        print(f"{indent}[{icon}] {branch_tag} d{depth}: {current_state} ({latency_ms:.0f}ms) "
              f"-- {grade} | {message[:50]}...")

        # If terminal state or no more input required, this branch is done
        if current_state in TERMINAL_STATES:
            time.sleep(delay * 0.3)
            continue
        if not parsed.get("requires_input", False):
            time.sleep(delay * 0.3)
            continue

        # Build updated chat history for child branches
        new_history = list(chat_history)
        new_history.append({"role": "user", "content": message})
        new_history.append({"role": "assistant", "content": parsed.get("mechanic_instructions", raw[:500])})

        # Get all answer paths Gus offered
        answer_paths = parsed.get("answer_path_prompts", [])

        # Also check corpus follow_ups for this state
        corpus_choices = []
        for fu in available_follow_ups:
            if fu.get("trigger_state") == current_state:
                corpus_choices.append(fu["response"])

        # Merge: corpus follow_ups first (they're the "right" answer), then Gus's options
        all_choices = []
        for c in corpus_choices:
            all_choices.append(("corpus", c))
        for i, ap in enumerate(answer_paths):
            all_choices.append((f"choice_{i+1}_of_{len(answer_paths)}", ap))

        # If no choices available, branch is dead
        if not all_choices:
            continue

        # Enqueue branches for each choice (within budget)
        for choice_label, choice_text in all_choices:
            if next_branch_id > max_branches:
                break
            child_path = branch_path + [f"[{choice_label}] {choice_text[:60]}"]
            queue.append((next_branch_id, child_path, new_history, depth + 1))
            next_branch_id += 1

        time.sleep(delay * 0.5)

    time.sleep(delay)
    return api_calls


def main():
    parser = argparse.ArgumentParser(description="GusEngine Stress Test v3 — Decision Tree Explorer")
    parser.add_argument("--api-url", required=True)
    parser.add_argument("--vehicle-id", default="1965_ford_mustang")
    parser.add_argument("--corpus", default=CORPUS_PATH)
    parser.add_argument("--delay-seconds", type=float, default=2.0)
    parser.add_argument("--limit", type=int, default=0, help="Max queries (0=all)")
    parser.add_argument("--repeat", type=int, default=1, help="Repeat each query N times")
    parser.add_argument("--max-branches", type=int, default=12, help="Max branches per query tree")
    parser.add_argument("--max-depth", type=int, default=5, help="Max conversation depth")
    parser.add_argument("--paraphrases", action="store_true")
    parser.add_argument("--paraphrases-only", action="store_true")
    parser.add_argument("--mode", choices=["quick", "standard", "full"], default="standard",
                        help="quick=5 queries; standard=all; full=all+paraphrases+3 repeats")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--category", help="Filter by category")
    parser.add_argument("--system", help="Filter by FSM system")
    parser.add_argument("--timeout", type=int, default=120)
    args = parser.parse_args()

    if args.mode == "quick":
        if args.limit == 0:
            args.limit = 5
    elif args.mode == "full":
        args.paraphrases = True
        if args.repeat == 1:
            args.repeat = 3

    corpus_data = load_corpus(args.corpus)
    queries = corpus_data["queries"]
    paraphrase_groups = corpus_data.get("paraphrase_groups", [])

    # Build job list
    jobs = []
    if not args.paraphrases_only:
        for q in queries:
            if args.category and q.get("category") != args.category:
                continue
            if args.system and q.get("system") != args.system:
                continue
            jobs.append((q["id"], q["query"], q, q.get("follow_ups", []), None))

    if args.paraphrases or args.paraphrases_only:
        for pg in paraphrase_groups:
            if args.system and pg.get("system") != args.system:
                continue
            for variant in pg["variants"]:
                meta = {
                    "category": "paraphrase",
                    "system": pg["system"],
                    "difficulty": "medium",
                    "known_answer_keywords": pg.get("expected_keywords", []),
                }
                jobs.append((variant["id"], variant["query"], meta, [], pg["scenario_id"]))

    if args.limit > 0:
        jobs = jobs[:args.limit]

    # Resume
    if args.resume:
        completed = set()
        if os.path.isdir(RESULTS_DIR):
            for path in glob.glob(os.path.join(RESULTS_DIR, "run_*.jsonl")):
                with open(path, "r", encoding="utf-8") as f:
                    for line in f:
                        try:
                            e = json.loads(line)
                            if e.get("turn") == 1 and e.get("branch_id", 0) == 0:
                                completed.add(f"{e['query_id']}_r{e.get('repeat_num', 1)}")
                        except:
                            pass
        before = len(jobs)
        # Filter to jobs that have at least one incomplete repeat
        filtered = []
        for j in jobs:
            for r in range(1, args.repeat + 1):
                if f"{j[0]}_r{r}" not in completed:
                    filtered.append(j)
                    break
        jobs = filtered
        print(f"Resume: skipping {before - len(jobs)} completed queries")

    if not jobs:
        print("No queries to run.")
        return

    # Health check
    print(f"\nConnecting to {args.api_url}...")
    try:
        h = requests.get(f"{args.api_url}/api/health", timeout=10)
        print(f"  API: {h.json()}")
    except Exception as e:
        print(f"  WARNING: health check failed: {e}\n")

    run_id = uuid.uuid4().hex[:8]
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(RESULTS_DIR, exist_ok=True)
    log_file = os.path.join(RESULTS_DIR, f"run_{ts}.jsonl")

    est_calls = len(jobs) * args.repeat * min(args.max_branches, 5)
    print(f"\n{'='*60}")
    print(f"  STRESS TEST v3 — Decision Tree Explorer")
    print(f"  Run ID: {run_id}")
    print(f"  Target: {args.api_url}")
    print(f"  Vehicle: {args.vehicle_id}")
    print(f"  Queries: {len(jobs)} × {args.repeat} repeats")
    print(f"  Max branches/query: {args.max_branches}")
    print(f"  Max depth: {args.max_depth}")
    print(f"  Est. API calls: ~{est_calls}")
    print(f"  Log: {log_file}")
    print(f"{'='*60}\n")

    start_time = time.time()
    total_calls = 0

    for i, (qid, qtext, qmeta, follow_ups, scenario_id) in enumerate(jobs, 1):
        for repeat in range(1, args.repeat + 1):
            r_tag = f" R{repeat}/{args.repeat}" if args.repeat > 1 else ""
            s_tag = f" [{scenario_id}]" if scenario_id else ""
            print(f"\n[{i}/{len(jobs)}]{r_tag}{s_tag} {qid}: {qtext[:65]}...")
            calls = explore_decision_tree(
                args.api_url, args.vehicle_id, qid, qtext, qmeta,
                run_id, repeat, log_file, args.delay_seconds,
                follow_ups=follow_ups, scenario_id=scenario_id,
                max_branches=args.max_branches, max_depth=args.max_depth,
            )
            total_calls += calls

    elapsed = time.time() - start_time
    print(f"\n{'='*60}")
    print(f"  RUN COMPLETE")
    print(f"  Duration: {elapsed:.0f}s ({elapsed/60:.1f} min)")
    print(f"  Total API calls: {total_calls}")
    print(f"  Log: {log_file}")
    print(f"  Analyze: python stress_test_analyzer.py --input {log_file}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
