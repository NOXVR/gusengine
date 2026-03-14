"""Download MerCruiser Qdrant snapshot from Hetzner to local storage."""
import requests, os, hashlib

URL = "http://5.78.132.233:8888/pdfs/snapshots/mercruiser.snapshot"
LOCAL_DIR = r"j:\GusEngine\storage\snapshots"
LOCAL_FILE = os.path.join(LOCAL_DIR, "fsm_corpus_2000_mercury_mercruiser_marine.snapshot")

os.makedirs(LOCAL_DIR, exist_ok=True)

print(f"Downloading from {URL}")
print(f"Saving to {LOCAL_FILE}")

r = requests.get(URL, stream=True, timeout=300)
r.raise_for_status()

total = int(r.headers.get("content-length", 0))
downloaded = 0
sha = hashlib.sha256()

with open(LOCAL_FILE, "wb") as f:
    for chunk in r.iter_content(chunk_size=1024 * 1024):  # 1MB chunks
        f.write(chunk)
        sha.update(chunk)
        downloaded += len(chunk)
        mb = downloaded / (1024 * 1024)
        pct = (downloaded / total * 100) if total else 0
        print(f"\r  {mb:.1f} MB / {total / (1024*1024):.1f} MB ({pct:.0f}%)", end="", flush=True)

print(f"\n\nDownload complete!")
print(f"  File: {LOCAL_FILE}")
print(f"  Size: {os.path.getsize(LOCAL_FILE):,} bytes ({os.path.getsize(LOCAL_FILE) / (1024*1024):.1f} MB)")
print(f"  SHA256: {sha.hexdigest()}")
