"""Download ALL snapshots from Hetzner to local storage."""
import requests, os, hashlib

API = "http://5.78.132.233:8888"
SNAPSHOT_DIR = r"j:\GusEngine\storage\snapshots"
os.makedirs(SNAPSHOT_DIR, exist_ok=True)

# Also check mercruiser snapshot that's already there
COLLECTIONS = [
    "fsm_corpus_1975_cessna_172_skyhawk_aviation",
    "fsm_corpus_1979_chevrolet_camaro",
    "fsm_corpus_1975_ford_2000_3000_4000_agriculture_tractor",
    "fsm_corpus_1965_ford_mustang",
    "fsm_corpus",  # Mercedes 450SL
]

print("=== Checking snapshot availability ===")
for coll in COLLECTIONS:
    url = f"{API}/pdfs/snapshots/{coll}.snapshot"
    try:
        r = requests.head(url, timeout=30)
        size_mb = int(r.headers.get("content-length", 0)) / (1024*1024)
        print(f"  {coll}: HTTP {r.status_code}, {size_mb:.1f} MB")
    except Exception as e:
        print(f"  {coll}: ERROR - {e}")

print("\n=== Downloading snapshots ===")
for coll in COLLECTIONS:
    local_path = os.path.join(SNAPSHOT_DIR, f"{coll}.snapshot")
    if os.path.exists(local_path):
        existing_mb = os.path.getsize(local_path) / (1024*1024)
        print(f"  SKIP {coll}: already exists ({existing_mb:.1f} MB)")
        continue

    url = f"{API}/pdfs/snapshots/{coll}.snapshot"
    print(f"  Downloading {coll}...", end="", flush=True)
    try:
        r = requests.get(url, stream=True, timeout=600)
        r.raise_for_status()
        total = int(r.headers.get("content-length", 0))
        downloaded = 0
        sha = hashlib.sha256()
        with open(local_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024*1024):
                f.write(chunk)
                sha.update(chunk)
                downloaded += len(chunk)
                mb = downloaded / (1024*1024)
                print(f"\r  Downloading {coll}... {mb:.1f}/{total/(1024*1024):.1f} MB", end="", flush=True)
        
        final_mb = os.path.getsize(local_path) / (1024*1024)
        print(f"\r  OK {coll}: {final_mb:.1f} MB (SHA256: {sha.hexdigest()[:16]}...)")
    except Exception as e:
        print(f"\r  FAIL {coll}: {e}")

print("\n=== Final inventory ===")
total_size = 0
for f in sorted(os.listdir(SNAPSHOT_DIR)):
    if f.endswith(".snapshot"):
        size = os.path.getsize(os.path.join(SNAPSHOT_DIR, f))
        total_size += size
        print(f"  {f}: {size/(1024*1024):.1f} MB")
print(f"\nTotal backup size: {total_size/(1024*1024):.1f} MB ({total_size/(1024*1024*1024):.2f} GB)")
