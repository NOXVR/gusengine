import urllib.request
import os

filepath = r'j:\GusEngine\storage\pdf_transfer.py'
filesize = os.path.getsize(filepath)
print(f"Uploading {filepath} ({filesize // 1024}KB)...")

with open(filepath, 'rb') as f:
    data = f.read()

# Try 0x0.st (simple file hosting)
boundary = '----FormBoundary7MA4YWxkTrZu0gW'
body = (
    f'--{boundary}\r\n'
    f'Content-Disposition: form-data; name="file"; filename="pdf_transfer.py"\r\n'
    f'Content-Type: application/octet-stream\r\n\r\n'
).encode() + data + f'\r\n--{boundary}--\r\n'.encode()

req = urllib.request.Request(
    'https://0x0.st',
    data=body,
    headers={'Content-Type': f'multipart/form-data; boundary={boundary}'}
)

try:
    resp = urllib.request.urlopen(req, timeout=120)
    url = resp.read().decode().strip()
    print(f"SUCCESS! URL: {url}")
    print(f"\nRun this on the pod:")
    print(f"  curl -o /workspace/GusEngine/pdf_transfer.py '{url}' && python3 /workspace/GusEngine/pdf_transfer.py")
except Exception as e:
    print(f"0x0.st failed: {e}")
    print("Trying dpaste.com...")
    # If 0x0.st fails too, we'll do a different approach
