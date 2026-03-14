import requests, json

queries = [
    ("spongy brake pedal", "BRAKES"),
    ("thermostat stuck closed engine overheats", "THERMOSTAT"),
]

for q, label in queries:
    r = requests.post('http://5.78.132.233:8888/api/chat', json={
        'message': q,
        'vehicle_id': '1965_ford_mustang'
    }, timeout=60)
    d = r.json()
    resp = json.loads(d['response'])
    rag = d.get('rag_context', {})
    srcs = rag.get('sources', [])
    unique = list(set(s.get('source','') for s in srcs))
    cites = resp.get('source_citations', [])
    print(f"=== {label} ===")
    print(f"  Confidence: {resp.get('confidence', 'NOT SET')}")
    print(f"  RAG chunks: {rag.get('chunk_count', '?')}, tokens: {rag.get('total_tokens_used', '?')}")
    print(f"  RAG sources ({len(unique)}): {unique[:8]}")
    print(f"  Gus cites ({len(cites)}): {[c.get('source','') for c in cites[:5]]}")
    print(f"  Mechanic: {resp.get('mechanic_instructions','')[:200]}")
    print()
