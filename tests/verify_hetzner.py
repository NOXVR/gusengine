import requests, json

API = "http://5.78.132.233:8888"

queries = [
    ("Engine overheating - thermostat", "My engine is overheating. I think the thermostat might be stuck closed. What should I check?"),
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
        
        # Try to parse if answer is JSON string
        if answer.startswith("{"):
            try:
                ad = json.loads(answer)
                conf = ad.get("confidence", conf)
                state = ad.get("current_state", state)
                answer = ad.get("mechanic_instructions", answer)
            except:
                pass
        
        print(f"Confidence: {conf}")
        print(f"State: {state}")
        print(f"Answer (first 400 chars):")
        print(answer[:400])
    except Exception as e:
        print(f"ERROR: {e}")
