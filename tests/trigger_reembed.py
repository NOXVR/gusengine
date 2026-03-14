"""Wait for Hetzner deploy, then trigger re-embed and monitor progress."""
import requests
import time
import sys

API = "http://5.78.132.233:8888"

# Step 1: Wait for deploy to complete (health check)
print("Waiting for Hetzner deploy to complete...", flush=True)
for i in range(60):
    try:
        r = requests.get(f"{API}/api/health", timeout=5)
        if r.status_code == 200:
            print(f"  Backend healthy after {i*5}s", flush=True)
            break
    except:
        pass
    time.sleep(5)
else:
    print("ERROR: Backend not healthy after 5 minutes", flush=True)
    sys.exit(1)

# Step 2: Verify the new endpoint exists
try:
    r = requests.get(f"{API}/api/admin/reembed/status", timeout=10)
    print(f"  Reembed status endpoint: {r.status_code} - {r.json()}", flush=True)
except Exception as e:
    print(f"  Reembed status endpoint not found: {e}", flush=True)
    print("  Deploy may not have the new code yet. Waiting...", flush=True)
    for i in range(24):
        time.sleep(10)
        try:
            r = requests.get(f"{API}/api/admin/reembed/status", timeout=10)
            if r.status_code == 200:
                print(f"  Found after {(i+1)*10}s", flush=True)
                break
        except:
            pass
    else:
        print("ERROR: Reembed endpoint never became available", flush=True)
        sys.exit(1)

# Step 3: Trigger re-embed
print("\nTriggering re-embed for 1965_ford_mustang...", flush=True)
r = requests.post(f"{API}/api/admin/reembed/1965_ford_mustang", timeout=30)
print(f"  Response: {r.status_code} - {r.json()}", flush=True)

# Step 4: Monitor progress
print("\nMonitoring progress...", flush=True)
while True:
    time.sleep(10)
    try:
        r = requests.get(f"{API}/api/admin/reembed/status", timeout=10)
        s = r.json()
        t = time.strftime("%H:%M:%S")
        print(f"  {t} - {s['processed']}/{s['total']} ({s['errors']} errors) - {s['message']}", flush=True)
        if not s["running"] and s["processed"] > 0:
            print(f"\n  DONE: {s['message']}", flush=True)
            break
    except Exception as e:
        print(f"  Error polling status: {e}", flush=True)
