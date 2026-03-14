import json

log = [json.loads(l) for l in open('tests/results/run_20260309_163545.jsonl', 'r', encoding='utf-8')]
roots = [e for e in log if e.get('branch_id', 0) == 0 and e.get('turn', 1) == 1]
corpus = json.load(open('tests/accuracy_corpus.json', 'r', encoding='utf-8'))
queries = {q['id']: q for q in corpus['queries']}

# Show 5 strong examples with complaint + response + options
for idx in [7, 25, 49, 62, 99]:
    e = roots[idx]
    q = queries.get(e['query_id'], {})
    print(f"{'='*70}")
    print(f"QUERY #{idx+1}: {e['query_id']}")
    print(f"COMPLAINT: {e.get('query_text', '')[:200]}")
    print(f"ACTUAL ISSUE: {q.get('technical_issue', 'N/A')}")
    print(f"VALIDATED FIX: {q.get('validated_fix', 'N/A')[:200]}")
    print(f"SUBSYSTEMS: {e.get('intersecting_subsystems', [])}")
    print(f"INSTRUCTIONS: {e.get('mechanic_instructions', '')[:300]}")
    paths = e.get('answer_paths', [])
    print(f"OPTIONS ({len(paths)}):")
    for j, p in enumerate(paths):
        print(f"  {j+1}. {p}")
    print()
