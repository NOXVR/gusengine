"""Upload remaining Mustang FSM parts (4-14) to RunPod for GPU ingestion."""
import os, requests, time

API = "https://09hzf2941cdsxb-8888.proxy.runpod.net"
SRC = r"J:\GusEngine\project\1965-ford-mustang-fsm-corpus\split"
VID = "1965_ford_mustang"

# Only upload parts 4-14 (parts 1-3 are already ingested)
files = sorted(f for f in os.listdir(SRC) if f.endswith('.pdf') and f >= 'mustang_fsm_part_04')
print(f"Uploading {len(files)} PDFs to RunPod ({API})")

for i, f in enumerate(files, 1):
    path = os.path.join(SRC, f)
    size_mb = os.path.getsize(path) / (1024*1024)
    print(f"[{i}/{len(files)}] {f} ({size_mb:.1f}MB)...", end=" ", flush=True)
    with open(path, "rb") as pdf:
        r = requests.post(
            f"{API}/api/upload",
            files={"file": (f, pdf, "application/pdf")},
            data={"vehicle_id": VID},
            timeout=120
        )
    print(f"{r.status_code} - {r.json().get('message','')[:60]}")
    time.sleep(1)

print("\nAll uploads complete. Files are on RunPod disk.")
print("NOTE: Do NOT rely on background ingestion. Use the manual worker script.")
