import json, sys
sys.stdout.reconfigure(encoding='utf-8')

corpus = json.load(open('tests/stress_test_corpus_mercruiser.json', 'r', encoding='utf-8'))
queries = {q['id']: q for q in corpus['queries']}
log = [json.loads(l) for l in open('tests/results/run_20260311_225329.jsonl', 'r', encoding='utf-8')]
roots = [e for e in log if e.get('branch_id', 0) == 0 and e.get('turn', 1) == 1]

START = int(sys.argv[1]) if len(sys.argv) > 1 else 1
END = int(sys.argv[2]) if len(sys.argv) > 2 else 10

for entry in roots[START-1:END]:
    qid = entry['query_id']
    q = queries.get(qid, {})
    idx = roots.index(entry) + 1
    print('=' * 80)
    print(f'QUERY #{idx}: {qid}')
    print(f'COMPLAINT: {entry["query_text"]}')
    print(f'TECHNICAL ISSUE: {q.get("technical_issue", "N/A")}')
    print(f'VALIDATED FIX: {q.get("validated_fix", "N/A")[:400]}')
    print(f'GUS STATE: {entry["current_state"]}')
    print(f'GUS SAID: {entry.get("mechanic_instructions", "")[:400]}')
    print(f'GUS REASONING: {entry.get("diagnostic_reasoning", "")[:300]}')
    print(f'GUS SUBSYSTEMS: {entry.get("intersecting_subsystems", [])}')
    paths = entry.get('answer_paths', [])
    if paths:
        print(f'GUS OPTIONS ({len(paths)}):')
        for i, p in enumerate(paths[:5]):
            print(f'  {i+1}. {p[:120]}')
    print()
