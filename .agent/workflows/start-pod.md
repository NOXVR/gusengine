---
description: Start the GusEngine pod on RunPod and verify all services are healthy
---

# Start the GusEngine Pod

## CRITICAL RULES
- **DO NOT take screenshots** of the terminal. Previous agents crashed from 5MB+ image errors.
- **DO NOT attempt SCP, base64, or browser-terminal file transfers.** Code deploys via git.
- **DO NOT spend more than 5 minutes on any single step.** If something fails, report it and stop.
- Only read DOM text from the terminal — never capture images.

## Prerequisites
- The pod must be running on RunPod (user should start it from https://console.runpod.io/pods)
- Code changes must be committed and pushed: `git add . && git commit -m "msg" && git push` from `J:\GusEngine`

## Step 1: Ensure local changes are pushed
// turbo
```
git -C J:\GusEngine status --short
```
If there are uncommitted changes, commit and push them:
```
git -C J:\GusEngine add . && git -C J:\GusEngine commit -m "Deploy latest changes" && git -C J:\GusEngine push
```

## Step 2: Open the RunPod web terminal
Navigate to the pod's web terminal via browser. The pod ID may change — check https://console.runpod.io/pods for the current pod. The web terminal runs on port 19123:
`https://{POD_ID}-19123.proxy.runpod.net/`

## Step 3: Run start_all.sh on the pod
In the web terminal, execute:
```
bash /workspace/GusEngine/start_all.sh
```
This script automatically:
1. Pulls latest code from GitHub (`git pull`)
2. Loads secrets from `.env`
3. Starts Qdrant, BGE-M3 embedding server, and the FastAPI backend
4. Runs health checks on all 3 services

**Wait ~45 seconds** for services to initialize before checking output.

## Step 4: Verify services (via terminal commands, NOT screenshots)
Run these in the web terminal and read DOM output:
```
curl -s http://localhost:6333/healthz && echo " [QDRANT OK]"
curl -s http://localhost:8080/health && echo " [EMBEDDING OK]"
curl -s http://localhost:8888/api/health && echo " [BACKEND OK]"
```
All 3 must return OK.

## Step 5: Report the frontend URL
The frontend is served at:
`https://{POD_ID}-8888.proxy.runpod.net/`

## Troubleshooting
- **Git pull fails (auth):** The pod's git remote should have a PAT embedded. If not, re-add: `git remote set-url origin https://{PAT}@github.com/NOXVR/gusengine.git`
- **Backend won't start:** Check `tail -50 /workspace/backend.log` — most likely a missing Python dependency or import error.
- **Embedding server slow:** BGE-M3 takes ~30 seconds to load the model. Wait and re-check.
- **`.env` missing on pod:** Create it: `echo 'LLM_API_KEY=...' > /workspace/GusEngine/.env` (ask user for the key)
