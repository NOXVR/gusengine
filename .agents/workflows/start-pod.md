---
description: Start the GusEngine pod on RunPod and verify all services are healthy
---

# Start GusEngine Pod

// turbo-all

## Prerequisites
- The RunPod pod must be in "Stopped/Exited" state
- The pod's `/workspace/GusEngine/.env` file must contain a valid `LLM_API_KEY`

## Steps

1. Go to https://console.runpod.io/pods and click "Start Pod" on the GusEngine pod
2. Wait for the pod status to change to "Running"
3. Open the pod's web terminal (port 19123)
4. Run the startup script:
```bash
bash /workspace/GusEngine/start_all.sh
```
5. Verify all 3 services are reported as healthy in the script output
6. If any service shows "WAITING" or "LOADING", check status with:
```bash
supervisorctl -c /workspace/GusEngine/supervisord.conf status
```
7. Test the chat endpoint:
```bash
curl -s http://localhost:8888/api/stats
```
8. Verify the frontend loads at the pod's proxy URL (port 8888)

## Service Management
After startup, use supervisorctl to manage services:
```bash
# Check status of all services
supervisorctl -c /workspace/GusEngine/supervisord.conf status

# Restart a specific service (keeps ALL env vars intact)
supervisorctl -c /workspace/GusEngine/supervisord.conf restart backend

# View live logs
supervisorctl -c /workspace/GusEngine/supervisord.conf tail -f backend

# Stop everything
supervisorctl -c /workspace/GusEngine/supervisord.conf shutdown
```

## IMPORTANT
- **NEVER restart services manually with pkill + nohup.** Always use supervisorctl.
- supervisord auto-restarts crashed services — no manual intervention needed.
- All environment variables are in `supervisord.conf` — never need to set them by hand.
