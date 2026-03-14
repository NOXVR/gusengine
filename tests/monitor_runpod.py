import requests, time

API = "https://09hzf2941cdsxb-8888.proxy.runpod.net"

for i in range(30):
    try:
        r = requests.get(f"{API}/api/stats/1965_ford_mustang", timeout=30)
        d = r.json()
        t = time.strftime("%H:%M:%S")
        print(f"{t} - Points: {d['points']}, Sources: {d['sources']}", flush=True)
    except Exception as e:
        print(f"Error: {e}", flush=True)
    time.sleep(60)
