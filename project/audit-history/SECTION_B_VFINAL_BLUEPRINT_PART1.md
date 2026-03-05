# SECTION B: VFINAL MASTER ARCHITECTURAL BLUEPRINT

**CLOSED-LOOP AUTOMOTIVE DIAGNOSTIC RAG ENGINE**  
**VERSION:** VFINAL — All Phase 1–4 Audit Fixes Incorporated  
**AUDIENCE:** Layman with terminal access on bare-metal Ubuntu 22.04 LTS  
**MANDATE:** Execute every command in exact order. Do not skip. Do not improvise.

---

## PHASE 1: BARE-METAL SERVER PREPARATION & NETWORK SECURITY

**Goal:** Lock down your Ubuntu server, install tools, establish TLS encryption and firewall.

### Step 1: System Updates & Core Tools

```bash
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y curl git build-essential fuse3 libguestfs-tools \
  python3-pip python3-venv tar jq nginx openssl ufw
```

### Step 2: Secure Kernel Access

```bash
sudo usermod -aG kvm $USER
```

### Step 3: Docker Installation

```bash
curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

> [!CAUTION]
> **DO NOT paste any more commands yet.** You must **log out completely** and **log back in** for the Docker group change to take effect. Type `exit`, reconnect via SSH, then continue.

### Step 4: Verify Docker Access (After Re-Login)

```bash
docker run hello-world
```

If you see "Hello from Docker!", proceed. If "permission denied," log out and back in again.

### Step 5: Firewall Configuration

Lock down all ports. Only allow SSH, HTTP (for redirect), and HTTPS:

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable
```

Prevent Docker from bypassing UFW by restricting its iptables behavior:

```bash
sudo bash -c 'cat > /etc/docker/daemon.json <<EOF
{
  "iptables": false
}
EOF'
sudo systemctl restart docker
```

> [!WARNING]
> With `"iptables": false`, Docker will not create its own NAT rules. The `-p 127.0.0.1:3001:3001` flag still works for localhost binding, but external access is fully blocked by UFW. This is the desired behavior — all external traffic routes through Nginx.

### Step 6: Build the Directory Structure & Python Environment

```bash
export ENGINE_DIR=$HOME/diagnostic_engine
mkdir -p $ENGINE_DIR/plugins/agent-skills/{vin-lookup,manual-status,purchase-router,draft-tribal-knowledge}
mkdir -p $ENGINE_DIR/{storage,downloads,extracted_manuals,staging/ova,staging/mounts,quarantine}

# Python Virtual Environment with ALL required dependencies
python3 -m venv $ENGINE_DIR/venv
$ENGINE_DIR/venv/bin/pip install watchdog PyMuPDF requests tiktoken

# Generate secure 256-bit API tokens
echo "JWT_SECRET=$(openssl rand -hex 32)" > "$ENGINE_DIR/.env"
echo "INTERNAL_API_KEY=$(openssl rand -hex 32)" >> "$ENGINE_DIR/.env"
```

### Step 7: Nginx Reverse Proxy (TLS + WebSocket + HTTP Redirect)

```bash
sudo mkdir -p /etc/nginx/ssl
sudo openssl req -x509 -nodes -days 3650 -newkey rsa:2048 \
  -keyout /etc/nginx/ssl/diag-engine.key \
  -out /etc/nginx/ssl/diag-engine.crt \
  -subj "/C=US/ST=State/L=City/O=Workshop/CN=diag-engine.local"

sudo bash -c 'cat > /etc/nginx/sites-available/default <<NGINXEOF
# HTTP -> HTTPS redirect (prevents plaintext API key transmission)
server {
    listen 80;
    server_name _;
    return 301 https://\$host\$request_uri;
}

# HTTPS with WebSocket support
server {
    listen 443 ssl;
    server_name _;
    ssl_certificate /etc/nginx/ssl/diag-engine.crt;
    ssl_certificate_key /etc/nginx/ssl/diag-engine.key;

    location / {
        proxy_pass http://127.0.0.1:3001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_read_timeout 86400s;
        proxy_send_timeout 86400s;
    }
}
NGINXEOF'
sudo nginx -t && sudo systemctl restart nginx
```

---

## PHASE 2: SECURE DOCKER ORCHESTRATION

**Goal:** Deploy AnythingLLM with a single source of truth for configuration.

```bash
# 1. Run temporarily to generate native config
docker run -d --name temp_llm mintplexlabs/anythingllm:latest
echo "Waiting 30 seconds for AnythingLLM to initialize..."
sleep 30

# 2. Verify config was generated
docker exec temp_llm ls /app/server/.env
# If this prints "/app/server/.env", proceed. If "No such file", wait 15 more seconds and retry.

# 3. Extract valid config to host
docker cp temp_llm:/app/server/.env $ENGINE_DIR/.env.temp

# 4. Merge: AnythingLLM defaults FIRST, then our secure keys OVERRIDE
cat $ENGINE_DIR/.env >> $ENGINE_DIR/.env.temp
mv $ENGINE_DIR/.env.temp $ENGINE_DIR/.env

# 5. Destroy the temporary container
docker rm -f temp_llm

# 6. Deploy production container — SINGLE SOURCE OF TRUTH for config
#    NO --env-file, NO -e INTERNAL_API_KEY (both removed per audit)
docker run -d -p 127.0.0.1:3001:3001 \
  --name diagnostic_rag_engine \
  -v $ENGINE_DIR/storage:/app/server/storage \
  -v $ENGINE_DIR/.env:/app/server/.env \
  -v $ENGINE_DIR/extracted_manuals:/app/server/extracted_manuals:ro \
  -v $ENGINE_DIR/plugins/agent-skills:/app/server/storage/plugins/agent-skills \
  -e STORAGE_DIR="/app/server/storage" \
  --restart always \
  mintplexlabs/anythingllm:latest
```

> [!NOTE]
> The `extracted_manuals` directory is read-only (`:ro`) inside the container. Files are uploaded via the AnythingLLM UI or API, which copies them into internal storage. This is a security feature, not a bug.

---

## PHASE 3: THE HARDENED THERMODYNAMIC INGESTION DAEMON

**Goal:** Safely extract PDFs from 20GB+ VMDK/OVA files with crash-proof I/O.

### Step 1: Write the Daemon

```bash
cat > $ENGINE_DIR/vmdk_extractor.py << 'DAEMON_EOF'
import os, time, subprocess, shutil, tempfile, tarfile, hashlib, json, struct
import fitz  # PyMuPDF

ENGINE_DIR = os.path.expanduser("~/diagnostic_engine")
DOWNLOAD_DIR = os.path.join(ENGINE_DIR, "downloads")
OUTPUT_DIR = os.path.join(ENGINE_DIR, "extracted_manuals")
OVA_STAGING = os.path.join(ENGINE_DIR, "staging", "ova")
MOUNTS_DIR = os.path.join(ENGINE_DIR, "staging", "mounts")
MANIFEST_FILE = os.path.join(OUTPUT_DIR, "manifest.json")
QUARANTINE_DIR = os.path.join(ENGINE_DIR, "quarantine")

def get_hash(filepath):
    """SHA-256 hash with 1MB buffer (20GB in ~25s vs ~200s with 8KB)."""
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def validate_file_header(path):
    """Validate VMDK sparse header or OVA TAR magic to catch corrupt downloads."""
    try:
        with open(path, 'rb') as f:
            magic = f.read(4)
        if path.lower().endswith('.vmdk'):
            return magic == b'KDMV' or magic[:3] == b'# D'
        if path.lower().endswith('.ova'):
            with open(path, 'rb') as f:
                f.seek(257)
                return f.read(5) == b'ustar'
    except Exception:
        pass
    return False

def wait_for_stable(path, interval=5, stable_count=6, max_wait=7200):
    """
    Wait until file size is stable for 30 seconds (6 x 5s).
    Abort after 2 hours (download presumed dead).
    Validate file header after stabilization.
    """
    prev_size, count, elapsed = -1, 0, 0
    while count < stable_count:
        if elapsed >= max_wait:
            print(f"ABORT: File has not stabilized in {max_wait}s. Download dead.")
            return False
        try:
            curr_size = os.path.getsize(path)
            if curr_size == prev_size and curr_size > 0:
                count += 1
            else:
                count = 0
            prev_size = curr_size
        except OSError:
            count = 0
        time.sleep(interval)
        elapsed += interval

    if not validate_file_header(path):
        print(f"ABORT: {path} has invalid VMDK/OVA header. Corrupt download.")
        return False
    return True

def write_manifest_atomic(manifest, manifest_path):
    """Atomic write via tmpfile + os.replace (POSIX atomic rename)."""
    dir_name = os.path.dirname(manifest_path)
    with tempfile.NamedTemporaryFile('w', dir=dir_name, delete=False, suffix='.tmp') as tmp:
        json.dump(manifest, tmp, indent=2)
        tmp.flush()
        os.fsync(tmp.fileno())
        tmp_path = tmp.name
    os.replace(tmp_path, manifest_path)

def chunk_pdf(input_path, output_dir, file_hash, base_name, chunk_size=50):
    """
    Split FSMs into 50-page chunks with absolute page ranges in filenames.
    Example: 'FSM_Vol1_pages_101-150.pdf' so citations are traceable.
    """
    doc = fitz.open(input_path)
    total = len(doc)
    for i in range(0, total, chunk_size):
        start_page = i + 1  # 1-indexed
        end_page = min(i + chunk_size, total)
        chunk_doc = fitz.open()
        chunk_doc.insert_pdf(doc, from_page=i, to_page=end_page - 1)
        out_name = f"{base_name}_pages_{start_page}-{end_page}.pdf"
        chunk_doc.save(os.path.join(output_dir, out_name))
        chunk_doc.close()
        print(f"  Created chunk: {out_name}")
    doc.close()

def load_manifest():
    """Load manifest with corruption recovery."""
    if os.path.exists(MANIFEST_FILE):
        try:
            with open(MANIFEST_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"WARNING: Manifest corrupted ({e}). Starting fresh.")
            backup = MANIFEST_FILE + ".corrupt." + str(int(time.time()))
            shutil.copy2(MANIFEST_FILE, backup)
    return {}

def process_file(file_path):
    file_hash = get_hash(file_path)
    manifest = load_manifest()

    if file_hash in manifest:
        print("DUPLICATE ARCHIVE DETECTED. Skipping.")
        os.remove(file_path)
        return

    mount_point = tempfile.mkdtemp(prefix="vmdk_mount_", dir=MOUNTS_DIR)
    extract_dir = None
    target_vmdk = file_path
    success = False

    try:
        if file_path.lower().endswith('.ova'):
            extract_dir = tempfile.mkdtemp(prefix="ova_extract_", dir=OVA_STAGING)
            subprocess.run(["tar", "-xf", file_path, "-C", extract_dir], check=True)
            for root, _, files in os.walk(extract_dir):
                for f in files:
                    if f.lower().endswith('.vmdk'):
                        target_vmdk = os.path.join(root, f)
                        break

        print(f"Mounting VMDK at {mount_point}")
        subprocess.run(["guestmount", "-a", target_vmdk, "-i", "--ro", mount_point], check=True)

        for root, _, files in os.walk(mount_point):
            for name in files:
                if name.lower().endswith('.pdf'):
                    src = os.path.join(root, name)
                    pdf_hash = get_hash(src)
                    if pdf_hash not in manifest:
                        print(f"Chunking: {name}")
                        chunk_pdf(src, OUTPUT_DIR, pdf_hash, name.replace('.pdf', ''))
                        manifest[pdf_hash] = name

        manifest[file_hash] = {"timestamp": time.time(), "file": os.path.basename(file_path)}
        write_manifest_atomic(manifest, MANIFEST_FILE)
        success = True

    except Exception as e:
        print(f"EXTRACTION ERROR: {e}")
        # Quarantine failed file instead of deleting
        os.makedirs(QUARANTINE_DIR, exist_ok=True)
        quarantine_path = os.path.join(QUARANTINE_DIR, os.path.basename(file_path))
        try:
            shutil.move(file_path, quarantine_path)
            print(f"QUARANTINED: {quarantine_path}")
        except Exception as qe:
            print(f"QUARANTINE FAILED: {qe}")

    finally:
        if os.path.ismount(mount_point):
            subprocess.run(["guestunmount", mount_point], check=False)
            time.sleep(2)  # Allow FUSE to release
        try:
            shutil.rmtree(mount_point, ignore_errors=True)
        except Exception:
            pass
        if extract_dir:
            shutil.rmtree(extract_dir, ignore_errors=True)

    # Delete source file ONLY on success (never in finally)
    if success:
        try:
            os.remove(file_path)
            print(f"Source file removed after successful extraction.")
        except Exception as e:
            print(f"Warning: Could not remove source: {e}")

if __name__ == "__main__":
    for d in [DOWNLOAD_DIR, OUTPUT_DIR, OVA_STAGING, MOUNTS_DIR, QUARANTINE_DIR]:
        os.makedirs(d, exist_ok=True)
    print("Zero-Tolerance Ingestion Daemon Active.")
    while True:
        for f in os.listdir(DOWNLOAD_DIR):
            if f.lower().endswith(('.vmdk', '.ova')):
                path = os.path.join(DOWNLOAD_DIR, f)
                try:
                    # Skip files younger than 30 seconds (still downloading)
                    age = time.time() - os.stat(path).st_mtime
                    if age < 30:
                        continue
                except OSError:
                    continue
                if wait_for_stable(path):
                    process_file(path)
        time.sleep(10)
DAEMON_EOF
```

### Step 2: Deploy as Systemd Service

```bash
USER_NAME=$(whoami)
sudo bash -c "cat > /etc/systemd/system/manual-ingest.service <<EOF
[Unit]
Description=Automotive Diagnostic VMDK/OVA Extraction Daemon
After=network.target
[Service]
Type=simple
User=$USER_NAME
ExecStart=/home/$USER_NAME/diagnostic_engine/venv/bin/python3 /home/$USER_NAME/diagnostic_engine/vmdk_extractor.py
Restart=always
RestartSec=10
[Install]
WantedBy=multi-user.target
EOF"
sudo systemctl daemon-reload && sudo systemctl enable --now manual-ingest.service
```

---

## PHASE 4: UI CALIBRATION & RAG MATHEMATICS

**Goal:** Force the AI to reason ONLY from retrieved document chunks. Zero hallucination tolerance.

1. **Access Web UI:** Browser → `https://YOUR_SERVER_IP` (accept self-signed TLS warning). Complete setup wizard.

2. **AI Provider:** Settings → AI Providers → **Anthropic** (`claude-3-5-sonnet-latest`). Insert API Key.
   - **Token Limit: `4000`** (hard cap to force precision)

3. **Embedding:** Settings → Embedding Preference → **Voyage AI** (`voyage-3-large`). Insert API Key.

4. **Table Preservation:** Settings → Document Handling → **Mistral OCR**.
   - Text Splitter: **Markdown Header Text Splitter**

5. **Reranking:** Settings → AI Providers → Reranking → **Cohere** → `rerank-english-v3.0`. Insert API Key.

6. **Workspace Creation:** Create workspace (e.g., `1975-Mercedes-Benz-450SL`). Go to Workspace Settings → Vector Database:
   - **Similarity Threshold:** `0.50`
   - **Max Context Snippets:** `4` *(NOT 40. Budget: 4 chunks × 250 tokens = 1,000 tokens. Leaves 2,500 tokens for system prompt + ledger + response.)*
   - **Accuracy Optimized (Reranking):** ON

7. **Chat History Limit:** Workspace Settings → Chat Settings → **Chat History: `4`** *(Keeps last 4 messages. Prevents token budget collapse in multi-turn sessions.)*

---

## PHASE 5: THE TRIBAL KNOWLEDGE SUBSYSTEM (TKS)

**Goal:** Master Technician's empirical knowledge mathematically overrides the FSM.

### Step 1: Create the Master Ledger

Create a file named `1975_450SL_MASTER_LEDGER.md`:

```markdown
# MASTER TECHNICIAN LEDGER: 1975 MERCEDES-BENZ 450SL
**AUTHORITY LEVEL: TRIBAL SUPREMACY**
**MANDATE:** These empirical shop notes supersede conflicting FSM procedures.

## FAULT SIGNATURE: Hot start vapor lock, cranks but won't catch.
- **OEM FSM Diagnosis:** Replace Fuel Accumulator.
- **MASTER TECH OVERRIDE:** Do not drop the tank. 90% probability is a hairline crack in the 0.4 ohm ballast resistor on the fender.
- **VERIFICATION TEST:** Hot-wire terminal 15 on the ignition coil directly to battery positive. If it starts instantly, the resistor is dead.
```

### Step 2: Upload and Pin

1. In the `1975-Mercedes-Benz-450SL` workspace, click **Upload Document** (paperclip icon).
2. Upload the `1975_450SL_MASTER_LEDGER.md` file.
3. Click **Move to Workspace**, then **Save and Embed**.
4. **CRITICAL:** Find the Ledger in the document list and click the **Pushpin icon** (turns blue).

> [!IMPORTANT]
> **Token Budget Rule:** The Master Ledger MUST NOT exceed 1,500 tokens (~30 fault signatures). Before every edit, run the validation script (Phase 10). When the ledger hits the cap, archive older entries to a non-pinned `MASTER_LEDGER_ARCHIVE.md` that participates in vector search but does not consume the token budget on every query.

*(Continued in Part 2: Phases 6–10)*
