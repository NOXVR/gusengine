import requests, time

API = "http://5.78.132.233:8888"
VID = "1965_ford_mustang"

for i in range(10):
    try:
        r = requests.get(f"{API}/api/stats/{VID}", timeout=10)
        d = r.json()
        t = time.strftime("%H:%M:%S")
        print(f"{t} - Points: {d['points']}, Sources: {d['sources']}")
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(30)
