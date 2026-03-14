import requests

r = requests.head('http://5.78.132.233:8888/pdfs/snapshots/mercruiser.snapshot', timeout=30)
print(f'Status: {r.status_code}')
print(f'Content-Length: {r.headers.get("content-length", "unknown")}')
print(f'Content-Type: {r.headers.get("content-type", "unknown")}')
