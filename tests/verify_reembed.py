import requests, json

API = "http://5.78.132.233:8888"

queries = [
    ("Thermostat stuck closed", "My engine is overheating. I think the thermostat might be stuck closed. What should I check?"),
    ("Transmission slipping", "My transmission is slipping between gears. What should I check?"),
    ("Brake specs (baseline)", "What are the brake drum specifications for my Mustang?"),
]

for name, msg in queries:
    print(f"\n{'='*60}")
    print(f"QUERY: {name}")
    print(f"{'='*60}")
    try:
        r = requests.post(f"{API}/api/chat", json={
            "message": msg,
            "vehicle_id": "1965_ford_mustang"
        }, timeout=60)
        d = r.json()
        conf = d.get("confidence", "N/A")
        state = d.get("state", d.get("current_state", "N/A"))
        answer = d.get("answer", d.get("response", ""))
        
        if answer.startswith("{"):
            try:
                ad = json.loads(answer)
                conf = ad.get("confidence", conf)
                state = ad.get("current_state", state)
                cites = ad.get("source_citations", [])
                answer = ad.get("mechanic_instructions", answer)
                print(f"Confidence: {conf}")
                print(f"State: {state}")
                print(f"Citations: {len(cites)}")
                if cites:
                    sources = set(c.get("source_document", "") for c in cites[:5])
                    print(f"Sources: {sources}")
                print(f"Answer (first 300 chars):")
                print(answer[:300])
            except:
                print(f"Confidence: {conf}")
                print(f"Answer: {answer[:300]}")
        else:
            print(f"Confidence: {conf}")
            print(f"State: {state}")
            print(f"Answer: {answer[:300]}")
    except Exception as e:
        print(f"ERROR: {e}")
