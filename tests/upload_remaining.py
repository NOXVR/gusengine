"""Upload remaining Mustang FSM parts (4-14) to GusEngine."""
import requests, os, time, sys

API = "http://5.78.132.233:8888"
SPLIT_DIR = r"J:\GusEngine\project\1965-ford-mustang-fsm-corpus\split"
VEHICLE_ID = "1965_ford_mustang"

# Parts 4-14 are the ones missing
parts = [f"mustang_fsm_part_{i:02d}_p{(i-1)*50+1}-{min(i*50, 691)}.pdf" for i in range(4, 15)]
# Fix part 14 filename
parts[-1] = "mustang_fsm_part_14_p651-691.pdf"

print(f"Uploading {len(parts)} FSM parts to {API}")
print()

for i, part in enumerate(parts, 1):
    path = os.path.join(SPLIT_DIR, part)
    if not os.path.exists(path):
        print(f"[{i}/{len(parts)}] SKIP - {part} not found")
        continue
    
    size_mb = os.path.getsize(path) / (1024*1024)
    print(f"[{i}/{len(parts)}] Uploading {part} ({size_mb:.1f} MB)...", end=" ", flush=True)
    
    try:
        with open(path, 'rb') as f:
            r = requests.post(
                f"{API}/api/upload",
                files={"file": (part, f, "application/pdf")},
                data={"vehicle_id": VEHICLE_ID},
                timeout=600  # 10 min timeout for large PDFs
            )
        d = r.json()
        status = d.get("status", "unknown")
        chunks = d.get("chunks", "?")
        print(f"{status} ({chunks} chunks)")
    except Exception as e:
        print(f"ERROR: {e}")
    
    time.sleep(2)  # Brief pause between uploads

# Check final stats
print()
r = requests.get(f"{API}/api/stats/{VEHICLE_ID}", timeout=10)
print(f"Final Mustang collection: {r.json()}")
