# RunPod Deployment Guide — GusEngine V10 Prototype

> **Cost:** ~$0.79/hr when running, ~$7/mo storage when stopped

---

## 1. Create RunPod Account

1. Go to [runpod.io](https://www.runpod.io/) and sign up
2. Add a payment method (credit card or crypto)
3. Add $10-25 in credits to start

---

## 2. Create GPU Pod

1. Navigate to **GPU Cloud** → **Deploy**
2. Select **A100 80GB SXM** (~$0.79/hr)
3. Configure:
   - **Template:** RunPod PyTorch 2.1 (Ubuntu 22.04, CUDA 12.1)
   - **Container Disk:** 20 GB (for Docker images)
   - **Volume Disk:** 100 GB (for models, PDFs, Qdrant data)
   - **Volume Mount Path:** `/workspace`
   - **Exposed HTTP Ports:** `80, 8888`
   - **Exposed TCP Ports:** `22`
4. Click **Deploy**

> [!NOTE]
> The pod takes 1-3 minutes to provision. You'll see a green "Running" status when ready.

---

## 3. First-Time Setup (SSH into Pod)

```bash
# Connect via SSH (connection string shown in RunPod dashboard)
ssh root@<pod-ip> -p <port> -i ~/.ssh/id_rsa

# Navigate to workspace (persists across restarts)
cd /workspace

# Clone your repository
git clone <your-repo-url> GusEngine
cd GusEngine

# Verify GPU
nvidia-smi
# Expected: A100-SXM4-80GB, 81920 MiB

# Install huggingface_hub for model downloads
pip install huggingface_hub

# Download models (~25 GB total, takes 10-20 min)
mkdir -p ./storage/models

# Qwen2.5-32B-Instruct-AWQ (~18 GB)
huggingface-cli download Qwen/Qwen2.5-32B-Instruct-AWQ \
  --local-dir ./storage/models/Qwen2.5-32B-Instruct-AWQ

# BGE-M3 embedding model (~2 GB)
huggingface-cli download BAAI/bge-m3 \
  --local-dir ./storage/models/bge-m3

# Docling layout models (~500 MB)
huggingface-cli download ds4sd/docling-models \
  --local-dir ./storage/models/docling-models

# EasyOCR models (~100 MB)
python3 -c "
import easyocr
import shutil, os
reader = easyocr.Reader(['en'], gpu=False)
src = os.path.expanduser('~/.EasyOCR/model')
dst = './storage/easyocr_models'
os.makedirs(dst, exist_ok=True)
for f in os.listdir(src):
    shutil.copy2(os.path.join(src, f), dst)
print(f'EasyOCR models cached to {dst}: {os.listdir(dst)}')
"
```

---

## 4. Upload FSM PDFs

From your **Windows machine** (PowerShell):

```powershell
# Option A: Using SCP
scp -r -P <port> J:\GusEngine\storage\pdfs\* root@<pod-ip>:/workspace/GusEngine/storage/pdfs/

# Option B: Using rsync (if available)
rsync -avz -e "ssh -p <port>" J:\GusEngine\storage\pdfs\ root@<pod-ip>:/workspace/GusEngine/storage/pdfs/
```

---

## 5. Start GusEngine

```bash
cd /workspace/GusEngine

# Build and start all services
docker compose up -d --build

# Watch the startup (vLLM takes ~2 min to load 32B model)
docker compose logs -f

# Check health
curl http://localhost:8888/api/health
# Expected: {"status": "ok"}
```

### Service Startup Order

| Service | Start Time | Health Indicator |
|:--------|:-----------|:-----------------|
| Qdrant | ~15 sec | Port 6333 responds |
| TEI | ~30 sec | `/health` returns 200 |
| vLLM | ~2 min | `/v1/models` returns model list |
| Backend | ~1 min (after deps) | `/api/health` returns ok |
| Frontend | ~10 sec (after deps) | Port 80 serves HTML |

---

## 6. Test the Pipeline

```bash
# Test ingestion (with a PDF already in ./storage/pdfs/)
curl -X POST http://localhost:8888/api/ingest \
  -H "Content-Type: application/json" \
  -d '{"pdf_path": "47.0-00 Fuel System.pdf"}'

# Test chat
curl -X POST http://localhost:8888/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What does the fuel system section cover?"}'
```

---

## 7. Cost Management

| State | Cost | What Persists |
|:------|:-----|:--------------|
| **Running** | ~$0.79/hr | Everything |
| **Stopped** | ~$0.07/GB/mo (~$7/mo for 100 GB) | Network volume (models, PDFs, Qdrant data) |
| **Terminated** | $0 | Nothing — all data lost |

### To save money:
```bash
# Stop all containers first
docker compose down

# Then stop the pod via RunPod dashboard → "Stop"
# Models, PDFs, and Qdrant data persist on the network volume
```

### To resume:
1. Click **Start** in RunPod dashboard
2. SSH in
3. `cd /workspace/GusEngine && docker compose up -d`

---

## 8. Access the Frontend

RunPod exposes HTTP ports via proxy URLs:
- **Frontend:** `https://<pod-id>-80.proxy.runpod.net`
- **API:** `https://<pod-id>-8888.proxy.runpod.net/api/health`

These URLs are shown in the RunPod dashboard under **Connect** → **HTTP Service**.
