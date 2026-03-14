"""Wait for deploy, then test the timing chain stretch query (#10) for differential behavior."""
import requests, json, time, sys

API = "http://5.78.132.233:8888"

# Wait for deploy
print("Waiting for deploy...", flush=True)
for i in range(60):
    try:
        r = requests.get(f"{API}/api/health", timeout=5)
        if r.status_code == 200:
            print(f"  Backend healthy after {i*5}s", flush=True)
            break
    except:
        pass
    time.sleep(5)

# Test the exact same query that failed — timing chain stretch
query = "My Mustang has been gradually losing power over the past few months. The engine idles rough and it's gotten harder to start, especially when cold. It just doesn't have the pep it used to."

print(f"\nSending timing chain test query...\n", flush=True)
r = requests.post(f"{API}/api/chat", json={
    "message": query,
    "vehicle_id": "1965_ford_mustang"
}, timeout=120)

d = r.json()
answer = d.get("answer", d.get("response", ""))

if answer.startswith("{"):
    try:
        ad = json.loads(answer)
        print(f"STATE: {ad.get('current_state')}")
        print(f"CONFIDENCE: {ad.get('confidence')}")
        print(f"SUBSYSTEMS: {ad.get('intersecting_subsystems', [])}")
        print(f"\nREASONING:\n{ad.get('diagnostic_reasoning', '')}")
        print(f"\nINSTRUCTIONS:\n{ad.get('mechanic_instructions', '')}")
        paths = ad.get("answer_path_prompts", [])
        print(f"\nOPTIONS ({len(paths)}):")
        for i, p in enumerate(paths):
            print(f"  {i+1}. {p}")
    except:
        print(answer[:1000])
else:
    print(answer[:1000])
