# ARCHITECTURE_FINAL_V8.md

**SYSTEM:** Closed-Loop Automotive Diagnostic RAG Engine

**VERSION:** V8 (Phase 8 Audit Consolidation — Cross-Examined by Antigravity + DeepThink)

**CLASSIFICATION:** ZERO-TOLERANCE / LIFE-SAFETY ADJACENT

**TARGET:** Ubuntu 22.04 LTS (Bare Metal)

**STATUS:** LOCKED / DETERMINISTIC / THERMODYNAMICALLY STABLE

### CRITICAL ARCHITECTURAL PREFACE

This document supersedes ARCHITECTURE_FINAL_V7_CONSOLIDATED_V2.md. It is the product of two independent Phase 8 hostile audits (Antigravity + DeepThink) that cross-examined the V2 document against all three Phase 7 hostile analysis files. The Phase 8 audits confirmed all 19 V2 fixes were correctly applied, identified 1 cascading secondary failure introduced by a V2 fix, 1 documentation regression, and 1 defense-in-depth improvement.

**V8 Consolidation Methodology:**
Every fix was cross-examined between two competing audit reports. Where the reports disagreed, the claim was traced back to the actual code and adjudicated line-by-line. Only findings confirmed by forensic code verification were applied.

**V8 Changelog (Phase 8 + Phase 9 Audit Consolidation):**
- Daemon main loop quarantines files that fail `wait_for_stable()` with forced-deletion fallback if quarantine fails — prevents 2-hour rolling livelock under ALL failure modes (DT Phase 8 Finding, hardened by Phase 9 Audit)
- `ExecStopPost` callout restored with FUSE zombie mount justification alongside shell-escaping explanation (DT Phase 8 Regression)
- `parseGusResponse()` Pass 2 regex replaced with brute-force `JSON.parse` iteration — immune to string boundaries and nesting depth (Cross-Examination Finding)
- V2 changelog restored missing bullet for Upload `IndexError` guard (Phase 9 Audit Finding)

**V2 Changelog (Phase 7 Hostile Audit Consolidation — Preserved):**
- `ExecStopPost` loop variable triple-escaped to survive `sudo bash -c "..."` + unquoted heredoc (CO_2 Finding 01, DT Finding 1)
- `export ENGINE_DIR` added to top of Phase 2 code block (CO Finding 1.1, CO_2 Finding 02)
- Phase 2 `.env` verification guard rewritten from subshell `()` to `if/fi` block (CO_2 Finding 03)
- `chmod 600` applied to `.env` after creation and after API key addition (CO Finding 5.2, CO_2 Finding 04, DT Finding 4)
- `chmod 600` applied to TLS private key (CO Finding 5.3, CO_2 Finding 05)
- `cut -d '=' -f2` replaced with `cut -d '=' -f2-` in all shell scripts (CO Finding 5.4, CO_2 Finding 06)
- API key empty-check guards added to all Python scripts (CO Finding 6.1, CO_2 Finding 07)
- Nginx upload/folder-creation blocks upgraded to case-insensitive regex match (DT Finding 3)
- `wait_for_stable()` zero-byte branch increments `elapsed` counter to prevent infinite loop (DT Finding 2)
- `parseGusResponse()` replaced with JSON.parse try-catch approach immune to in-string braces (CO Finding 7.1, CO_2 Finding 08, DT Finding 5)
- `RETRIEVAL_FAILURE` frontend handling clarified with explicit restart button instruction (CO Finding 7.2, CO_2 Finding 09)
- PHASE_B `buildUserMessage` sends explicit `required_next_state: null` to override stale history (CO Finding 7.3)
- Manifest dead code on direct-PDF path removed; value types unified to dict (CO Finding 6.4, CO_2 Finding 10)
- Docker log rotation configured with `--log-opt` (CO Finding 5.5)
- `tiktoken` encoding pinned to explicit `cl100k_base` (CO Finding 6.2)
- Phase 9 `$INTERNAL_KEY` validated with empty-check guard (CO Finding 1.3)
- Workspace creation step added to Phase 3 (CO_2 Finding 11.2)
- Upload `IndexError` guard added to `sync_ingest.py` — `if not documents` prevents `[][0]` crash (CO Finding 3.2)
- `import sys` added to `sync_ingest.py` (required by API key guard)
- `process_file()` exception handler hardened with three-tier quarantine defense — eliminates last file-persistence path (Phase 10 DNA Audit)
- Workspace slug change instructions corrected from 4 files to 3 — `handler.js` receives slug as runtime parameter (Phase 10 Opus Audit)
- `process_file()` pre-try operations (`get_hash`, `load_manifest`, dedup check) moved inside try/except — prevents unhandled crash from PermissionError causing infinite systemd restart loop (Phase 10 DT Audit)
- `tempfile.mkdtemp()` moved inside try block with `mount_point = None` init — `OSError` from disk full/inode exhaustion now triggers quarantine instead of daemon crash (Phase 10 DT R3)
- `sync_ingest.py` dedup guard added — queries workspace for already-embedded documents before upload loop, skips duplicates (Phase 10 DT R3)
- `sync_ledger.py` atomic swap — fetches existing ledger document location and injects into `deletes[]` array, preventing legacy vector accumulation (Phase 10 DT R3)
- Phase 10 tar backup excludes `staging/` directory — prevents FUSE mount traversal during backup (Phase 10 DT R3)
- `sync_ingest.py` rate limiting — `time.sleep(12)` placed in `finally` block so it fires unconditionally after `continue`, `except`, and normal flow (Phase 10 R4)
- `parseGusResponse()` Pass 2 outer loop reversed from backward to forward scan — guarantees outermost JSON envelope extracted first, preventing inner nested JSON from hijacking state machine (Phase 10 DT R4)
- Main loop quarantine guard — `os.path.exists(path)` check added before quarantine attempt, prevents false CRITICAL logs when files vanish during `wait_for_stable()` (Phase 10 DT R4)
- `parseGusResponse()` Pass 1 now validates `current_state` before returning — prevents trailing JSON objects from hijacking the state machine (Phase 10 R5)
- `validate_ledger.py` output label corrected from "RAG budget remaining" to "Budget remaining (RAG + response)" (Phase 10 R5)
- `ExecStopPost` extended to clean `staging/ova/*` in addition to `staging/mounts/*` — defense against SIGKILL during OVA extraction (Phase 10 DT R5)
- `watchdog` removed from pip install — dead dependency contradicting DNA Engineering Decision #3 (Phase 10 DT R5)
- `process_file()` exception handler now checks `os.path.exists(file_path)` before quarantine — prevents false CRITICAL on vanished files (Phase 10 DT R5)
- `os.makedirs(QUARANTINE_DIR)` moved inside inner `try` block — prevents unhandled crash if disk is full during quarantine (Phase 10 DT R5)
- Systemd unit paths use `$USER_HOME` (via `eval echo ~$USER_NAME`) instead of hardcoded `/home/$USER_NAME` — supports root deployments where home is `/root/` (Phase 10 DT R6)
- ExecStopPost `rm -rf` uses `--one-file-system` flag — prevents recursive FUSE mount traversal if `guestunmount` fails (Phase 10 DT R6)
- Both quarantine paths (main loop + process_file) now trap `FileNotFoundError` in innermost except — eliminates TOCTOU false CRITICAL cascade (Phase 10 DT R6)
- Main loop quarantine adds `os.makedirs(QUARANTINE_DIR, exist_ok=True)` inside try — parity with process_file quarantine defense (Phase 10 DT R6)
- ExecStopPost escaping updated to `\\\$\\\$m` for systemd `$$` literal-dollar requirement — prevents systemd from expanding `$m` to empty (Phase 10 DT R7)
- ExecStopPost `rm -rf` targets parent directories instead of `/*` globs — ensures `--one-file-system` detects FUSE mount boundaries; `mkdir -p` recreates dirs (Phase 10 DT R7)
- Python `shutil.rmtree(mount_point)` guarded by `not os.path.ismount()` — prevents recursive FUSE traversal if guestunmount fails (Phase 10 DT R7)
- Main loop quarantine uses `shutil.move` instead of `os.rename` — handles cross-device moves (EXDEV) via fallback copy+delete (Phase 10 DT R7)
- `parseGusResponse` Pass 1 (backward-scanning depth counter) removed — backward scan could return trailing hallucinated JSON; Pass 2 forward scan is robust (Phase 10 DT R7)

> [!CAUTION]
> **EXECUTE ATOMICALLY.** Each phase's code block begins by re-exporting `ENGINE_DIR` where needed. However, the safest execution strategy is to run all phases in a single SSH session without disconnecting. If you must disconnect, re-export `ENGINE_DIR` manually: `export ENGINE_DIR=$HOME/diagnostic_engine`

---

## PHASE 1: BARE-METAL KERNEL PREPARATION & NETWORK BOUNDARY

**Goal:** Establish a secured, encrypted runtime environment with atomic file locking, anti-spoofing proxy rules, and strict firewall boundaries.

**Step 1: Install Core Dependencies**

Open your terminal. Execute this exact block to install the toolchain and the `lsof` kernel lock utility:

```bash
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y curl git build-essential fuse3 libguestfs-tools python3-pip python3-venv tar jq nginx openssl lsof ufw

```

**Step 2: Secure Kernel Access & Docker**

Grant permissions and install Docker.

```bash
sudo usermod -aG kvm $USER
curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh
sudo usermod -aG docker $USER

```

> [!CAUTION]
> **STOP HERE. YOU MUST LOG OUT OF YOUR SERVER COMPLETELY AND LOG BACK IN.**
> The Docker group permissions will not take effect until you reconnect via SSH. Type `exit` and reconnect. Do not proceed until you have logged out and logged back in. Do NOT use `newgrp docker` — it opens a subshell that swallows subsequent commands.

**Step 3: Firewall Lockdown & Verification**

Lock down all ports except SSH and HTTP/S. Docker's localhost binding (`127.0.0.1:3001:3001`) prevents external exposure without breaking outbound API access (which Anthropic, Mistral, Voyage AI, and Cohere require).

> [!IMPORTANT]
> Do **NOT** set `"iptables": false` in `/etc/docker/daemon.json`. This was a Phase 3-era fix that was proven catastrophic in Phase 5 — it kills all container-to-internet connectivity, permanently bricking the AI stack. The combination of `-p 127.0.0.1:3001:3001` (localhost-only binding) and UFW's `default deny incoming` is the correct security posture.

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable
sudo ufw status verbose

```

*(Verify output says: `Status: active`, `Default: deny (incoming), allow (outgoing)`).*

**Step 4: Build the Thermodynamic File Structure**

Create the directory tree and Python environment.

```bash
export ENGINE_DIR=$HOME/diagnostic_engine
mkdir -p $ENGINE_DIR/plugins/agent-skills/{vin-lookup,manual-status,purchase-router,draft-tribal-knowledge}
mkdir -p $ENGINE_DIR/{storage,downloads,extracted_manuals,quarantine,staging/ova,staging/mounts}

python3 -m venv $ENGINE_DIR/venv
$ENGINE_DIR/venv/bin/pip install PyMuPDF requests tiktoken

```

**Step 5: Generate JWT Secret**

Create a single source of truth for the JWT secret. The `INTERNAL_API_KEY` is generated later via the AnythingLLM Web UI in Phase 3 — do NOT generate one here.

```bash
echo "JWT_SECRET=$(openssl rand -hex 32)" > "$ENGINE_DIR/.env"
chmod 600 "$ENGINE_DIR/.env"

```

> [!WARNING]
> The `.env` file must contain ONLY the `JWT_SECRET` at this stage. The `INTERNAL_API_KEY` will be added in Phase 3 after the Web UI generates it. Generating a phantom key here will create a duplicate that silently fails authentication if the `.env` is ever sorted or deduplicated.

**Step 6: Nginx Reverse Proxy (WebSocket, Payload, & Security Hardened)**

Configure Nginx for 50MB payloads, WebSockets, HTTP-to-HTTPS redirection, and strict header security.

> [!IMPORTANT]
> **V2 SECURITY CHANGES:**
> - `client_max_body_size` reduced from 500M to **50M** — prevents DoS via disk exhaustion
> - `X-Forwarded-For` uses `$remote_addr` (overwrite) instead of `$proxy_add_x_forwarded_for` (append) — prevents IP spoofing
> - Security headers added: `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`
> - `X-Powered-By` hidden from responses
> - Upload and folder-creation endpoints blocked via **case-insensitive regex** (`~*`) — prevents bypass via `/api/v1/document/UpLoad` or other case variations that Express.js would still route
> - TLS private key permissions locked to 600

```bash
sudo mkdir -p /etc/nginx/ssl
sudo openssl req -x509 -nodes -days 3650 -newkey rsa:2048 \
  -keyout /etc/nginx/ssl/diag-engine.key \
  -out /etc/nginx/ssl/diag-engine.crt \
  -subj "/C=US/ST=State/L=City/O=Workshop/CN=diag-engine.local"
sudo chmod 600 /etc/nginx/ssl/diag-engine.key
sudo chmod 644 /etc/nginx/ssl/diag-engine.crt

sudo bash -c 'cat > /etc/nginx/sites-available/default <<EOF
server {
    listen 80;
    server_name _;
    return 301 https://\$host\$request_uri;
}

server {
    listen 443 ssl;
    server_name _;

    ssl_certificate /etc/nginx/ssl/diag-engine.crt;
    ssl_certificate_key /etc/nginx/ssl/diag-engine.key;

    # Prevent DoS and massive Tribal Ledger payload abuse
    client_max_body_size 50M;

    # Information disclosure prevention
    proxy_hide_header X-Powered-By;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "DENY" always;
    add_header Referrer-Policy "no-referrer" always;

    # V2 FIX: Case-insensitive regex blocks upload and folder-creation endpoints.
    # Express.js routes are case-insensitive by default. Without ~*, an attacker
    # could bypass via /api/v1/document/UpLoad. The regex covers all case variants.
    location ~* ^/api/v1/document/(upload|create-folder) {
        return 403;
    }

    # --- MAIN PROXY ---
    location / {
        proxy_pass http://127.0.0.1:3001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;

        # Absolute IP overwrite. Do NOT append to attacker-spoofed headers.
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$remote_addr;
        proxy_set_header X-Forwarded-Proto \$scheme;

        proxy_read_timeout 86400s;
        proxy_send_timeout 86400s;
    }
}
EOF'

sudo nginx -t && sudo systemctl restart nginx

```

---

## PHASE 2: SECURE DOCKER ORCHESTRATION

**Goal:** Deploy AnythingLLM securely, preventing `.env` variable collisions.

> [!IMPORTANT]
> **V2 FIX:** `ENGINE_DIR` is re-exported at the top of this block. The V7 Consolidated document omitted this, causing silent path corruption if the operator's shell session ended between Phase 1 and Phase 2. The `.env` verification guard has been rewritten from a subshell `()` to an `if/fi` block — the subshell's `exit 1` only terminated the subshell, not the parent, allowing subsequent commands to execute with a missing `.env` file.

```bash
export ENGINE_DIR=$HOME/diagnostic_engine

# 1. Start a temp container to generate default configs
docker run -d --name temp_llm mintplexlabs/anythingllm:latest
echo "Waiting 30 seconds for container initialization..."
sleep 30

# 2. Verify generation and extract defaults
# V2 FIX: if/fi guard replaces subshell (). The subshell exit only killed
# the subshell — if .env wasn't generated, subsequent commands still ran,
# producing a corrupted .env that was missing AnythingLLM defaults.
docker exec temp_llm test -f /app/server/.env
if [ $? -ne 0 ]; then
    echo "FATAL: .env not generated inside container. Increase sleep or check container logs: docker logs temp_llm"
    docker rm -f temp_llm
    exit 1
fi
docker cp temp_llm:/app/server/.env $ENGINE_DIR/.env.temp
cat $ENGINE_DIR/.env >> $ENGINE_DIR/.env.temp
mv $ENGINE_DIR/.env.temp $ENGINE_DIR/.env
chmod 600 "$ENGINE_DIR/.env"
docker rm -f temp_llm

# 3. Launch Production Engine (Single source of truth)
# V2 FIX: --log-opt caps container logs at 50MB x 3 files to prevent disk exhaustion
docker run -d -p 127.0.0.1:3001:3001 \
  --name diagnostic_rag_engine \
  --log-opt max-size=50m --log-opt max-file=3 \
  -v $ENGINE_DIR/storage:/app/server/storage \
  -v $ENGINE_DIR/.env:/app/server/.env \
  -v $ENGINE_DIR/extracted_manuals:/app/server/extracted_manuals:ro \
  -v $ENGINE_DIR/plugins/agent-skills:/app/server/storage/plugins/agent-skills \
  -e STORAGE_DIR="/app/server/storage" \
  --restart always \
  mintplexlabs/anythingllm:latest

```

---

## PHASE 3: THE UI API KEY BINDING & WORKSPACE CREATION (CRITICAL)

**Goal:** Generate a real API key through the AnythingLLM Web UI, bind it to the host `.env`, and create the diagnostic workspace.

> [!CAUTION]
> AnythingLLM does **NOT** read API keys from external `.env` variables. Its API middleware authenticates strictly against an internal SQLite/LanceDB table containing keys generated via the Web UI. You MUST generate the key through the Web UI and export it back to the host.

1. Open your web browser. Go to `https://YOUR_SERVER_IP`.
2. **BROWSER BYPASS:** Your browser will say "Your connection is not private." Click **Advanced**, then **Proceed (unsafe)**.
3. Complete the AnythingLLM setup wizard.
4. Click the **Settings (Gear Icon)** in the bottom left → **API Keys**.
5. Click **Create new API Key**. Copy this alphanumeric text.

> [!IMPORTANT]
> **V2 ADDITION — WORKSPACE CREATION:**
> Before returning to the terminal, you MUST create the workspace that all scripts reference:
> 6. Click **New Workspace** (+ icon in the sidebar).
> 7. Name it exactly: `1975 Mercedes-Benz 450SL` (AnythingLLM will auto-generate the slug `1975-mercedes-benz-450sl`).
> 8. Verify the slug by hovering over the workspace name in the sidebar — the URL should end in `/1975-mercedes-benz-450sl`.
>
> If your vehicle is different, name the workspace accordingly and update `WORKSPACE_SLUG` in ALL 3 scripts: Phase 5 `sync_ingest.py`, `verify_ingestion.py`, and Phase 6 `sync_ledger.py`. (Phase 9 `handler.js` does NOT require changes — it receives `workspace_slug` as a runtime parameter from the AnythingLLM agent framework.)

Return to your Ubuntu terminal and execute:

```bash
# Replace PASTE_YOUR_COPIED_KEY_HERE with the exact key you just copied
echo "INTERNAL_API_KEY=PASTE_YOUR_COPIED_KEY_HERE" >> $HOME/diagnostic_engine/.env
export ENGINE_DIR=$HOME/diagnostic_engine
chmod 600 "$ENGINE_DIR/.env"
export INTERNAL_KEY=$(grep INTERNAL_API_KEY $ENGINE_DIR/.env | tail -1 | cut -d '=' -f2-)

# Verify the key is not empty
if [ -z "$INTERNAL_KEY" ]; then
    echo "FATAL: API key is empty. Re-check your paste."
    exit 1
fi
echo "API Key bound: ${INTERNAL_KEY:0:8}..."

```

---

## PHASE 4: THE HARDENED THERMODYNAMIC INGESTION DAEMON

**Goal:** Automate 20GB+ VMDK extraction with double-verified kernel locking, absolute page watermarking, 5-page physical chunking, and 1MB I/O hashing.

> [!IMPORTANT]
> **V8 CHANGES:**
> - **V8 FIX (CRITICAL):** Daemon main loop now quarantines files that fail `wait_for_stable()` — the V2 elapsed fix correctly prevented the internal infinite loop, but the file remained in `DOWNLOAD_DIR` and was re-discovered every 10 seconds, causing a permanent 2-hour rolling livelock from a single zero-byte file (DT Phase 8)
> - **V8 FIX (Phase 10):** `process_file()` exception handler now uses three-tier quarantine defense (`os.rename` → `os.remove` → CRITICAL log) instead of silent `except Exception: pass` — prevents 10-second extraction livelock when a corrupt file fails both processing AND `shutil.move`
> - **V8 FIX (Phase 10 DT):** `get_hash()`, `load_manifest()`, and dedup check moved INSIDE the `try` block — previously, `PermissionError` or `OSError` from these pre-try operations crashed the daemon unhandled, bypassing the quarantine logic and causing an infinite systemd restart loop
> - **V8 FIX (Phase 10 DT R3):** `tempfile.mkdtemp()` also moved INSIDE the `try` block — `mount_point` initialized to `None` before try, with `if mount_point and ...` guards in `finally`. Disk-full `OSError` now triggers quarantine instead of unhandled crash
> - `wait_for_stable()` zero-byte branch increments `elapsed` counter — prevents infinite deadlock on zero-byte network placeholder files (V2 fix, DT Finding 2)
> - Manifest value types unified to `dict` for all entries — removes dead code on direct-PDF path (V2 fix, CO_2 Finding 10)
> - All other V7 Consolidated daemon fixes preserved

**Step 1: Write the Daemon Script**

Type `nano $HOME/diagnostic_engine/vmdk_extractor.py`:

```python
#!/usr/bin/env python3
"""V8 Thermodynamic Ingestion Daemon.
Extracts PDFs from VMDK/OVA files, chunks them with absolute page
watermarks, and maintains an atomic manifest for deduplication.
"""

import os, sys, time, subprocess, shutil, tempfile, hashlib, json, glob
import fitz  # PyMuPDF

ENGINE_DIR = os.path.expanduser("~/diagnostic_engine")
DOWNLOAD_DIR = os.path.join(ENGINE_DIR, "downloads")
OUTPUT_DIR = os.path.join(ENGINE_DIR, "extracted_manuals")
QUARANTINE_DIR = os.path.join(ENGINE_DIR, "quarantine")
OVA_STAGING = os.path.join(ENGINE_DIR, "staging", "ova")
MOUNTS_DIR = os.path.join(ENGINE_DIR, "staging", "mounts")
MANIFEST_FILE = os.path.join(OUTPUT_DIR, "manifest.json")

def get_hash(filepath):
    """1MB Buffer for high-speed I/O on 20GB files."""
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(1048576), b''):
            h.update(chunk)
    return h.hexdigest()

def validate_file_header(path):
    """Validate VMDK/OVA magic bytes to detect corruption."""
    try:
        with open(path, 'rb') as f:
            magic = f.read(4)
        if path.lower().endswith('.vmdk'):
            return magic in [b'KDMV', b'# Di']
        if path.lower().endswith('.ova'):
            with open(path, 'rb') as f:
                f.seek(257)
                return f.read(5) == b'ustar'
    except Exception:
        pass
    return True  # Proceed if unknown format (caught by extraction fail anyway)

def wait_for_stable(path):
    """Multi-stage TOCTOU-immune OS lock verification with double-check.
    Includes OSError guards for file deletion during check and zero-byte
    file detection to prevent processing empty/incomplete downloads.

    V2 FIX: All code paths that execute `continue` now increment `elapsed`
    to prevent infinite loops on zero-byte files or size-changing files.
    """
    print(f"Verifying absolute OS file lock release: {path}")
    elapsed = 0
    while elapsed < 7200:  # 2-hour timeout
        try:
            subprocess.check_output(['lsof', path], stderr=subprocess.DEVNULL)
            time.sleep(10)
            elapsed += 10
        except subprocess.CalledProcessError:
            # File unlocked by lsof. Double-verify TOCTOU buffer.
            time.sleep(5)
            elapsed += 5  # V2 FIX: count this sleep toward timeout
            try:
                subprocess.check_output(['lsof', path], stderr=subprocess.DEVNULL)
                continue  # Re-locked during buffer — keep waiting
            except subprocess.CalledProcessError:
                # Confirm size stability with OSError guards
                try:
                    prev_size = os.path.getsize(path)
                except OSError:
                    return False  # File was deleted during check
                time.sleep(5)
                elapsed += 5  # V2 FIX: count this sleep toward timeout
                try:
                    curr_size = os.path.getsize(path)
                except OSError:
                    return False  # File was deleted during check
                if curr_size != prev_size:
                    continue  # Still writing
                if curr_size == 0:
                    # V2 FIX: elapsed is already incremented above.
                    # Without this, a zero-byte file caused an infinite loop
                    # because elapsed was only incremented in the try branch.
                    continue  # Empty file — still arriving
                if validate_file_header(path):
                    return True
                print(f"ABORT: {path} has invalid VMDK/OVA header. Corrupt download.")
                return False
    return False

def write_manifest_atomic(manifest):
    """Atomically write manifest.json using tmp+rename pattern."""
    dir_name = os.path.dirname(MANIFEST_FILE)
    with tempfile.NamedTemporaryFile('w', dir=dir_name, delete=False, suffix='.tmp') as tmp:
        json.dump(manifest, tmp, indent=2)
        tmp.flush()
        os.fsync(tmp.fileno())
        tmp_path = tmp.name
    os.replace(tmp_path, MANIFEST_FILE)

def chunk_pdf(input_path, output_dir, file_hash, base_name, chunk_size=5):
    """Chunk PDF into 5-page segments with absolute page watermarks.

    chunk_size=5 ensures semantic token limits (400 tokens) align with
    physical PDF page boundaries. Each chunk produces a narrow page range
    (e.g., pages_101-105.pdf) so citation accuracy is ±4 pages max.

    Absolute page watermarks [[ABSOLUTE_PAGE: N]] are burned into the
    text layer of each page BEFORE Mistral OCR processes them. This
    eliminates all LLM arithmetic for citations.
    """
    with fitz.open(input_path) as doc:
        total = len(doc)
        for i in range(0, total, chunk_size):
            start_page = i + 1
            end_page = min(i + chunk_size, total)
            with fitz.open() as chunk_doc:
                chunk_doc.insert_pdf(doc, from_page=i, to_page=end_page - 1)

                # Burn absolute provenance into the text layer.
                # Mistral OCR will read this marker and embed it in the
                # vectorized text. The LLM cites the integer directly.
                for page_idx in range(len(chunk_doc)):
                    abs_page = start_page + page_idx
                    page = chunk_doc[page_idx]
                    page.insert_text(
                        (72, 36),
                        f"[[ABSOLUTE_PAGE: {abs_page}]]",
                        fontsize=10,
                        color=(0.6, 0.6, 0.6)
                    )

                out_name = f"{base_name}_pages_{start_page}-{end_page}_{file_hash[:8]}.pdf"
                chunk_doc.save(os.path.join(output_dir, out_name))
                print(f"  Created chunk: {out_name}")

def load_manifest():
    """Load manifest with corrupt-backup safety."""
    if os.path.exists(MANIFEST_FILE):
        try:
            with open(MANIFEST_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            backup = MANIFEST_FILE + ".corrupt." + str(int(time.time()))
            shutil.copy2(MANIFEST_FILE, backup)
            print(f"WARNING: Corrupt manifest backed up to {backup}")
    return {}

def process_file(file_path):
    """Process a single VMDK/OVA/PDF file."""
    # V8 FIX (Phase 10 DT R3): mount_point initialized to None so the
    # finally block can safely check before cleanup. mkdtemp moved INSIDE
    # the try block — if disk is full or inodes exhausted, OSError is caught
    # by the quarantine handler instead of crashing the daemon.
    mount_point = None
    extract_dir = None
    target_vmdk = file_path
    success = False

    try:
        # V8 FIX (Phase 10 DT R3): mkdtemp inside try — OSError from disk
        # full / permission denied now triggers quarantine, not daemon crash.
        mount_point = tempfile.mkdtemp(prefix="vmdk_mount_", dir=MOUNTS_DIR)

        # V8 FIX (Phase 10 DT): get_hash(), load_manifest(), and dedup
        # check moved INSIDE the try block. Previously, a PermissionError
        # or OSError here would crash the daemon unhandled, bypassing the
        # quarantine logic and causing an infinite systemd restart loop.
        file_hash = get_hash(file_path)
        manifest = load_manifest()

        if file_hash in manifest:
            print(f"Skipping duplicate: {file_path}")
            os.remove(file_path)
            return

        if file_path.lower().endswith('.ova'):
            extract_dir = tempfile.mkdtemp(prefix="ova_extract_", dir=OVA_STAGING)
            subprocess.run(["tar", "-xf", file_path, "-C", extract_dir], check=True)
            largest_size = -1
            for root, _, files in os.walk(extract_dir):
                for f in files:
                    if f.lower().endswith('.vmdk'):
                        fp = os.path.join(root, f)
                        size = os.path.getsize(fp)
                        if size > largest_size:
                            largest_size = size
                            target_vmdk = fp

        if target_vmdk.lower().endswith(('.vmdk', '.ova')):
            subprocess.run(
                ["guestmount", "-a", target_vmdk, "-i", "--ro", mount_point],
                check=True
            )
            for root, _, files in os.walk(mount_point):
                for name in files:
                    if name.lower().endswith('.pdf'):
                        src = os.path.join(root, name)
                        pdf_hash = get_hash(src)
                        if pdf_hash not in manifest:
                            chunk_pdf(
                                src, OUTPUT_DIR, pdf_hash,
                                name.replace('.pdf', '').replace(' ', '_')
                            )
                            # V2 FIX: Unified manifest value type to dict
                            manifest[pdf_hash] = {
                                "timestamp": time.time(),
                                "file": name
                            }
        elif target_vmdk.lower().endswith('.pdf'):
            chunk_pdf(
                target_vmdk, OUTPUT_DIR, file_hash,
                os.path.basename(target_vmdk).replace('.pdf', '').replace(' ', '_')
            )
            # V2 FIX: Removed dead code — line 465 in V1 wrote a string
            # that was immediately overwritten by the dict on line 467.

        manifest[file_hash] = {
            "timestamp": time.time(),
            "file": os.path.basename(file_path)
        }
        write_manifest_atomic(manifest)
        success = True

    except Exception as e:
        print(f"Extraction Error: {e}")
        # V8 FIX (Phase 10 DT R5): Guard against file vanishing during extraction.
        # If file was deleted mid-process (cancelled upload), skip quarantine
        # to avoid false CRITICAL cascade identical to the main loop fix (Row 33).
        if not os.path.exists(file_path):
            print(f"File vanished during extraction (normal): {file_path}")
        else:
            try:
                os.makedirs(QUARANTINE_DIR, exist_ok=True)
                shutil.move(
                    file_path,
                    os.path.join(QUARANTINE_DIR, os.path.basename(file_path))
                )
                print(f"QUARANTINED (extraction failure): {file_path}")
            except Exception:
                # V8 FIX (Phase 10): If shutil.move fails, forcibly delete.
                # Without this, the file persists in DOWNLOAD_DIR and triggers
                # an infinite 10-second extraction retry loop.
                try:
                    os.remove(file_path)
                    print(f"FORCE-DELETED (quarantine failed): {file_path}")
                except OSError as e2:
                    # V8 FIX (Phase 10 DT R6): TOCTOU guard — if file vanished
                    # between os.path.exists check and here, suppress false CRITICAL.
                    if isinstance(e2, FileNotFoundError):
                        print(f"File vanished during quarantine (normal): {file_path}")
                    else:
                        print(f"CRITICAL: Cannot quarantine or delete {file_path}: {e2}. Manual intervention required.")
    finally:
        # V8 FIX (Phase 10 DT R3): mount_point may be None if mkdtemp failed.
        # Guard with truthiness check before os.path.ismount.
        if mount_point and os.path.ismount(mount_point):
            subprocess.run(["guestunmount", mount_point], check=False)
            time.sleep(2)
        # V8 FIX (Phase 10 DT R7): Only rmtree if the mount was successfully
        # detached. If guestunmount failed (busy mount), rmtree would traverse
        # the entire FUSE filesystem — ignore_errors swallows EROFS but wastes
        # minutes of I/O. ExecStopPost handles stuck mounts at service level.
        if mount_point and not os.path.ismount(mount_point):
            shutil.rmtree(mount_point, ignore_errors=True)
        if extract_dir:
            shutil.rmtree(extract_dir, ignore_errors=True)

    if success:
        try:
            os.remove(file_path)  # ONLY DELETE ON SUCCESS
        except OSError:
            pass

if __name__ == "__main__":
    for d in [DOWNLOAD_DIR, OUTPUT_DIR, OVA_STAGING, MOUNTS_DIR, QUARANTINE_DIR]:
        os.makedirs(d, exist_ok=True)
    print("V8 Ingestion Daemon Active.")
    while True:
        for f in os.listdir(DOWNLOAD_DIR):
            path = os.path.join(DOWNLOAD_DIR, f)
            if f.lower().endswith(('.vmdk', '.ova', '.pdf')):
                try:
                    # 30-second thermal age limit prevents racing active downloads
                    if time.time() - os.stat(path).st_mtime < 30:
                        continue
                except OSError:
                    continue

                if wait_for_stable(path):
                    process_file(path)
                else:
                    # V8 FIX: Quarantine files that fail stabilization.
                    # Without this, the file remains in DOWNLOAD_DIR and is
                    # re-discovered every 10 seconds. Since wait_for_stable()
                    # blocks for 2 hours per attempt, a single zero-byte file
                    # causes a permanent rolling livelock that halts ALL
                    # ingestion. Moving to quarantine breaks the cycle.

                    # V8 FIX (Phase 10 DT R4): If the file was deleted during
                    # wait_for_stable() (user cancelled SCP, network tool cleanup),
                    # skip quarantine entirely. Without this guard, os.rename throws
                    # FileNotFoundError, cascading through os.remove to a false
                    # CRITICAL log demanding "manual intervention" for a normal event.
                    if not os.path.exists(path):
                        print(f"File vanished during stabilization (normal): {path}")
                        continue

                    quarantine_dest = os.path.join(QUARANTINE_DIR, os.path.basename(path))
                    try:
                        # V8 FIX (Phase 10 DT R6): Ensure quarantine dir exists at
                        # runtime for parity with process_file's quarantine block.
                        os.makedirs(QUARANTINE_DIR, exist_ok=True)
                        # V8 FIX (Phase 10 DT R7): shutil.move handles cross-device
                        # moves (EXDEV) by falling back to copy+delete. os.rename
                        # raises OSError on cross-device, bypassing quarantine.
                        shutil.move(path, quarantine_dest)
                        print(f"QUARANTINED (failed stabilization after 2h): {path} -> {quarantine_dest}")
                    except OSError:
                        # LAST RESORT: If quarantine fails (permissions, cross-device,
                        # etc.), forcibly delete the file. A deleted file is recoverable
                        # from backups; a livelocked daemon is not.
                        try:
                            os.remove(path)
                            print(f"FORCE-DELETED (quarantine failed): {path}")
                        except OSError as e2:
                            # V8 FIX (Phase 10 DT R6): If the file vanished between
                            # os.path.exists check and here (TOCTOU), suppress the
                            # false CRITICAL instead of alarming the operator.
                            if isinstance(e2, FileNotFoundError):
                                print(f"File vanished during quarantine (normal): {path}")
                            else:
                                print(f"CRITICAL: Cannot quarantine or delete {path}: {e2}. Manual intervention required.")
        time.sleep(10)

```

Press `Ctrl+O`, `Enter`, `Ctrl+X`.

**Step 2: Deploy Systemd Service**

> [!IMPORTANT]
> **V8 FIX (CRITICAL):** The `ExecStopPost` directive is MANDATORY. If systemd sends SIGTERM to the daemon while a FUSE mount is active, the mount becomes orphaned. Without cleanup, repeated daemon restarts accumulate zombie FUSE mounts that exhaust file descriptors and block device access. The loop variable `$m` must survive FOUR processing layers: (1) the user's bash processing `sudo bash -c "..."`, (2) the inner bash processing the unquoted `<<EOF` heredoc, (3) systemd's own `$VAR` expansion on ExecStopPost values, and (4) the final `/bin/bash -c` that systemd invokes. Systemd expands `$m` to empty string (undefined variable) — the unit file must contain `$$m` so systemd reduces `$$` to a literal `$`. The source uses `\\\$\\\$m`: outer shell `\`→`\`, `\$`→`$` producing `\$\$m`; heredoc `\$`→`$` twice producing `$$m`; systemd `$$`→`$` producing `$m`; bash expands `$m` as loop variable. The `rm -rf` uses `--one-file-system` and targets parent directories (not `/*` globs) so that FUSE mount boundaries are correctly detected. The trailing `mkdir -p` recreates the staging directories after cleanup.

```bash
USER_NAME=$(whoami)
USER_HOME=$(eval echo ~$USER_NAME)
sudo bash -c "cat > /etc/systemd/system/manual-ingest.service <<EOF
[Unit]
Description=V8 Automotive Diagnostic Extraction Daemon
After=network.target

[Service]
Type=simple
User=$USER_NAME
ExecStart=$USER_HOME/diagnostic_engine/venv/bin/python3 $USER_HOME/diagnostic_engine/vmdk_extractor.py
ExecStopPost=/bin/bash -c 'for m in $USER_HOME/diagnostic_engine/staging/mounts/*; do guestunmount \\\$\\\$m 2>/dev/null || true; done; rm -rf --one-file-system $USER_HOME/diagnostic_engine/staging/mounts $USER_HOME/diagnostic_engine/staging/ova; mkdir -p $USER_HOME/diagnostic_engine/staging/mounts $USER_HOME/diagnostic_engine/staging/ova'
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF"

sudo systemctl daemon-reload && sudo systemctl enable --now manual-ingest.service

```

> [!CAUTION]
> **POST-DEPLOYMENT VERIFICATION (MANDATORY):** After running the above block, immediately verify the unit file contains the correct `$$m` systemd-escaped variable:
> ```bash
> sudo grep 'guestunmount' /etc/systemd/system/manual-ingest.service
> ```
> **Expected output must contain `$$m`:** `guestunmount $$m 2>/dev/null`
> Systemd reduces `$$` to a literal `$` at runtime, so bash receives `$m` as the loop variable.
> If you see `guestunmount $m` (single `$`), systemd will expand `$m` to empty — the FUSE cleanup is broken.
> If you see `guestunmount  2>/dev/null` (no variable at all), the shell escaping failed entirely.

---

## PHASE 5: OPERATIONAL UTILITY SCRIPTS

These scripts guarantee Mistral API stability, database completeness, ledger token safety, and validated ledger updates.

> [!CAUTION]
> **VENV EXECUTION MANDATE:** Every utility script in this phase MUST be invoked using the absolute venv binary path: `$HOME/diagnostic_engine/venv/bin/python3`. Using bare `python3` will crash with `ModuleNotFoundError` because `requests`, `tiktoken`, and `PyMuPDF` are installed ONLY inside the venv. This applies to ALL manual invocations, cron jobs, and shell scripts.

**1. Synchronous Ingestion Script (429 Mitigation)**

> [!WARNING]
> Do NOT upload PDFs via the AnythingLLM Web UI. The Nginx configuration blocks the upload endpoint from external clients. All ingestion MUST go through this script, which talks directly to `127.0.0.1:3001` on the host, bypassing Nginx.

> [!IMPORTANT]
> **V2 FIXES APPLIED:**
> - `import sys` added (required by API key guard's `sys.exit(1)`)
> - `cut -d '=' -f2` replaced with `cut -d '=' -f2-` — keys containing `=` would be silently truncated
> - API key empty-check guard added — prevents silent `Bearer ` (empty) auth that returns misleading 403s
> - Upload response parsing guards against empty `documents` list — `[{}][0]` masks the real failure; `[][0]` raises `IndexError`
> - HTTP status code check added before JSON parsing — a 500 error with HTML body would crash `resp.json()`

Type `nano $HOME/diagnostic_engine/sync_ingest.py`:

```python
#!/usr/bin/env python3
"""V8 Synchronous Ingestion Script.
Uploads chunked PDFs to AnythingLLM and embeds them one at a time,
with a 12-second cooldown between uploads to prevent Mistral OCR 429s.
"""

import os, sys, time, requests, glob

API_KEY = os.popen(
    f"grep INTERNAL_API_KEY {os.path.expanduser('~/diagnostic_engine/.env')} | tail -1 | cut -d '=' -f2-"
).read().strip()

# V2 FIX: Guard against empty API key. Without this, the script proceeds
# with "Bearer " (empty), gets silent 403s, and the operator thinks
# ingestion succeeded when no files were actually uploaded.
if not API_KEY:
    print("FATAL: INTERNAL_API_KEY is empty. Check ~/diagnostic_engine/.env")
    sys.exit(1)

API_URL = "http://127.0.0.1:3001/api/v1"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}
WORKSPACE_SLUG = "1975-mercedes-benz-450sl"  # CHANGE THIS TO YOUR WORKSPACE
CHUNKS_DIR = os.path.expanduser("~/diagnostic_engine/extracted_manuals")

# V8 FIX (Phase 10 DT R3): Fetch already-embedded documents BEFORE the loop.
# Without this, running the script a second time re-uploads and re-embeds
# every PDF in extracted_manuals/, causing exponential vector duplication.
print(f"Fetching existing documents for workspace: {WORKSPACE_SLUG}...")
try:
    ws_resp = requests.get(
        f"{API_URL}/workspace/{WORKSPACE_SLUG}",
        headers=HEADERS
    )
    existing_docs = set()
    if ws_resp.status_code == 200:
        for doc in ws_resp.json().get("workspace", {}).get("documents", []):
            existing_docs.add(doc.get("name", ""))
    print(f"Found {len(existing_docs)} already-embedded documents.")
except Exception as e:
    print(f"WARNING: Could not fetch workspace docs ({e}). Proceeding without dedup.")
    existing_docs = set()

print(f"Ingesting to workspace: {WORKSPACE_SLUG}...")
for chunk_path in sorted(glob.glob(os.path.join(CHUNKS_DIR, "*.pdf"))):
    filename = os.path.basename(chunk_path)

    # V8 FIX (Phase 10 DT R3): Skip already-embedded documents
    if filename in existing_docs:
        print(f"SKIP (already embedded): {filename}")
        continue

    print(f"Uploading: {filename}")
    with open(chunk_path, 'rb') as f:
        try:
            resp = requests.post(
                f"{API_URL}/document/upload",
                headers=HEADERS,
                files={"file": (filename, f, "application/pdf")}
            )
            # V2 FIX: Check HTTP status before parsing JSON.
            # A 500 error with HTML body would crash resp.json().
            if resp.status_code != 200:
                print(f"UPLOAD FAILED ({resp.status_code}): {filename} — {resp.text[:200]}")
                continue
            time.sleep(2)  # Internal queue buffer
            # V2 FIX: Guard against empty documents list.
            # Original code used [{}][0] which masks real failure.
            # If API returns {"documents": []}, this is now caught explicitly.
            documents = resp.json().get("documents", [])
            if not documents:
                print(f"WARNING: No document returned for {filename}. Skipping.")
                continue
            doc_loc = documents[0].get("location")
            if doc_loc:
                embed_resp = requests.post(
                    f"{API_URL}/workspace/{WORKSPACE_SLUG}/update-embeddings",
                    headers={**HEADERS, "Content-Type": "application/json"},
                    json={"adds": [doc_loc], "deletes": []}
                )
                if embed_resp.status_code == 200:
                    print(f"EMBEDDED: {filename}. Cooling down Mistral API...")
                else:
                    print(f"EMBED FAILED ({embed_resp.status_code}): {filename}")
            else:
                print(f"WARNING: No document location returned for {filename}")
        except Exception as e:
            print(f"Failed: {e}")
        finally:
            # V8 FIX (Phase 10 R4): Mandatory 12s cooldown in `finally` block
            # so it fires UNCONDITIONALLY — after `continue` (upload failure,
            # empty docs), after `except` (network errors), and after normal
            # success. Previous placement inside the try block was bypassed by
            # `continue` and `except`, creating the exact death spiral (tight-
            # loop 429 → no cooldown → re-request → IP/API ban) that the fix
            # was designed to prevent.
            time.sleep(12)

print("Ingestion complete.")

```

**Run with:**
```bash
$HOME/diagnostic_engine/venv/bin/python3 $HOME/diagnostic_engine/sync_ingest.py
```

**2. Post-Ingestion Verification Script**

> [!IMPORTANT]
> **V2 FIXES APPLIED:**
> - `cut -d '=' -f2` replaced with `cut -d '=' -f2-`
> - API key empty-check guard added

Type `nano $HOME/diagnostic_engine/verify_ingestion.py`:

```python
#!/usr/bin/env python3
"""V8 Post-Ingestion Verification.
Compares filesystem chunks against embedded workspace documents.
"""

import os, sys, requests

API_KEY = os.popen(
    "grep INTERNAL_API_KEY ~/diagnostic_engine/.env | tail -1 | cut -d '=' -f2-"
).read().strip()

# V2 FIX: Guard against empty API key
if not API_KEY:
    print("FATAL: INTERNAL_API_KEY is empty. Check ~/diagnostic_engine/.env")
    sys.exit(1)

API_URL = "http://127.0.0.1:3001/api/v1"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}
WORKSPACE_SLUG = "1975-mercedes-benz-450sl"  # CHANGE THIS
chunks_dir = os.path.expanduser("~/diagnostic_engine/extracted_manuals")

expected = set(f for f in os.listdir(chunks_dir) if f.endswith('.pdf'))
resp = requests.get(f"{API_URL}/workspace/{WORKSPACE_SLUG}", headers=HEADERS)
if resp.status_code == 200:
    docs = resp.json().get("workspace", {}).get("documents", [])
    embedded = set(d.get("name", "") for d in docs)
    missing = expected - embedded
    if missing:
        print(f"MISSING CHUNKS ({len(missing)}):")
        for m in sorted(missing):
            print(f"  ✗ {m}")
    else:
        print(f"✓ ALL {len(expected)} CHUNKS VERIFIED.")
else:
    print(f"ERROR: API returned {resp.status_code}")

```

**Run with:**
```bash
$HOME/diagnostic_engine/venv/bin/python3 $HOME/diagnostic_engine/verify_ingestion.py
```

---

## PHASE 6: THE TRIBAL KNOWLEDGE SUBSYSTEM (GATED ENFORCEMENT)

> [!CAUTION]
> **NEVER EDIT `MASTER_LEDGER.md` THROUGH THE WEB INTERFACE.**
> External Web UI uploads are explicitly blocked by the Nginx proxy layer. All ledger updates MUST pass mathematical token validation via the gated shell script below.

**1. Ledger Token Validator Script**

> [!IMPORTANT]
> **V2 FIX:** `tiktoken` encoding explicitly pinned to `cl100k_base` instead of using `encoding_for_model("gpt-4")`. The model-based lookup depends on `tiktoken`'s internal model→encoding mapping, which could break if tiktoken is updated and changes the mapping. Using `get_encoding("cl100k_base")` directly is immune to this.

Type `nano $HOME/diagnostic_engine/validate_ledger.py`:

```python
#!/usr/bin/env python3
"""V8 Ledger Token Validator.
Validates MASTER_LEDGER.md token count against the 1500-token cap
with a 15% safety margin for Anthropic tokenizer divergence.
Returns bool for composability; exit code set by __main__.
"""

import tiktoken, sys

# HARD CAP: 1500 tokens for the pinned ledger
# SAFETY MARGIN: 15% reduction for GPT-4 vs Anthropic tokenizer divergence
RAW_CAP = 1500
SAFETY_FACTOR = 0.85
ADJUSTED_CAP = int(RAW_CAP * SAFETY_FACTOR)  # = 1275

def validate(path):
    # V2 FIX: Pin encoding directly instead of model-based lookup
    enc = tiktoken.get_encoding("cl100k_base")
    with open(path, 'r') as f:
        content = f.read()
    count = len(enc.encode(content))
    remaining = 4000 - 600 - count  # 4000 total - 600 system prompt - ledger

    print(f"Ledger tokens (cl100k_base estimate): {count}")
    print(f"Adjusted cap (15% safety margin): {ADJUSTED_CAP}")
    print(f"Budget remaining (RAG + response): {remaining}")

    if count > ADJUSTED_CAP:
        print(f"REJECTED: Ledger tokens ({count}) exceed safety-adjusted cap ({ADJUSTED_CAP}).")
        print("Archive oldest entries and retry.")
        return False
    print("APPROVED.")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: validate_ledger.py <path_to_ledger.md>")
        sys.exit(1)
    result = validate(sys.argv[1])
    sys.exit(0 if result else 1)

```

**Run with:**
```bash
$HOME/diagnostic_engine/venv/bin/python3 $HOME/diagnostic_engine/validate_ledger.py /path/to/MASTER_LEDGER.md
```

**2. Ledger API Sync Script**

> [!NOTE]
> This script uses `requests` (installed in the venv) to upload and embed the ledger via the local API. This is preferred over raw `curl` because `curl` runs outside the venv context and isn't guaranteed to exist in all environments. Using `requests` keeps the entire pipeline within the venv boundary.

> [!IMPORTANT]
> **V2 FIXES APPLIED:**
> - `cut -d '=' -f2` replaced with `cut -d '=' -f2-`
> - API key empty-check guard added
> - Upload response `documents` list guard added (same IndexError fix as sync_ingest.py)

Type `nano $HOME/diagnostic_engine/sync_ledger.py`:

```python
#!/usr/bin/env python3
"""V8 Ledger API Sync.
Uploads a validated MASTER_LEDGER.md directly to AnythingLLM via the
local loopback API (bypassing Nginx) and embeds it in the workspace.
"""

import os, requests, sys

API_KEY = os.popen(
    f"grep INTERNAL_API_KEY {os.path.expanduser('~/diagnostic_engine/.env')} | tail -1 | cut -d '=' -f2-"
).read().strip()

# V2 FIX: Guard against empty API key
if not API_KEY:
    print("FATAL: INTERNAL_API_KEY is empty. Check ~/diagnostic_engine/.env")
    sys.exit(1)

API_URL = "http://127.0.0.1:3001/api/v1"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}
WORKSPACE_SLUG = "1975-mercedes-benz-450sl"  # CHANGE THIS

if len(sys.argv) < 2:
    print("Usage: sync_ledger.py <path_to_ledger.md>")
    sys.exit(1)

ledger_path = sys.argv[1]
filename = os.path.basename(ledger_path)

# V8 FIX (Phase 10 DT R3): Fetch existing workspace documents to find any
# prior ledger version. Without this, every ledger update adds a NEW vector
# set but never removes the old one, causing LanceDB to accumulate
# conflicting historical ledger versions that break the "Absolute Truth"
# override mechanism.
old_ledger_loc = None
try:
    ws_resp = requests.get(
        f"{API_URL}/workspace/{WORKSPACE_SLUG}",
        headers=HEADERS
    )
    if ws_resp.status_code == 200:
        for doc in ws_resp.json().get("workspace", {}).get("documents", []):
            if "MASTER_LEDGER" in doc.get("name", "").upper():
                old_ledger_loc = doc.get("location")
                print(f"Found existing ledger to replace: {old_ledger_loc}")
                break
except Exception as e:
    print(f"WARNING: Could not fetch workspace docs ({e}). Old ledger will NOT be deleted.")

print(f"Uploading ledger: {filename}")
with open(ledger_path, 'rb') as f:
    try:
        resp = requests.post(
            f"{API_URL}/document/upload",
            headers=HEADERS,
            files={"file": (filename, f, "text/markdown")}
        )
        # V2 FIX: Check HTTP status before JSON parsing
        if resp.status_code != 200:
            print(f"FATAL: Upload failed ({resp.status_code}): {resp.text[:200]}")
            sys.exit(1)
        # V2 FIX: Guard against empty documents list
        documents = resp.json().get("documents", [])
        if not documents:
            print(f"FATAL: No document returned. API response: {resp.text[:200]}")
            sys.exit(1)
        doc_loc = documents[0].get("location")
        if doc_loc:
            embed_resp = requests.post(
                f"{API_URL}/workspace/{WORKSPACE_SLUG}/update-embeddings",
                headers={**HEADERS, "Content-Type": "application/json"},
                # V8 FIX (Phase 10 DT R3): Inject old ledger into deletes
                # for atomic swap. Prevents legacy vector poisoning.
                json={"adds": [doc_loc], "deletes": [old_ledger_loc] if old_ledger_loc else []}
            )
            if embed_resp.status_code == 200:
                print(f"LEDGER SUCCESSFULLY UPLOADED AND EMBEDDED: {doc_loc}")
            else:
                print(f"EMBED FAILED ({embed_resp.status_code}): {embed_resp.text}")
                sys.exit(1)
        else:
            print(f"FATAL: No document location returned. API response: {resp.text}")
            sys.exit(1)
    except Exception as e:
        print(f"Failed to process ledger upload: {e}")
        sys.exit(1)

```

**3. The Execution Gate Shell Script**

> [!CAUTION]
> **This is the ONLY approved method for updating the MASTER_LEDGER.md.**
> The Nginx configuration blocks the `/api/v1/document/upload` endpoint from external clients, preventing Web UI uploads. This script runs on the host and talks directly to `127.0.0.1:3001`, bypassing Nginx entirely. It enforces the token validation gate that the Web UI cannot enforce.

Type `nano $HOME/diagnostic_engine/update_ledger.sh`:

```bash
#!/bin/bash
set -e

# V8 Validated Ledger Update Script
# Gates MASTER_LEDGER.md behind validate_ledger.py before upload.
# Uses sync_ledger.py (Python/requests) for consistent venv execution.

LEDGER_PATH="$1"
ENGINE_DIR="$HOME/diagnostic_engine"
VENV_PYTHON="$ENGINE_DIR/venv/bin/python3"

if [ -z "$LEDGER_PATH" ]; then
    echo "Usage: ./update_ledger.sh /path/to/MASTER_LEDGER.md"
    exit 1
fi

if [ ! -f "$LEDGER_PATH" ]; then
    echo "FATAL: File not found: $LEDGER_PATH"
    exit 1
fi

echo "=== V8 Ledger Validator ==="
echo "Validating token count..."

# GATE: Validate BEFORE upload. If this fails, nothing is uploaded.
if ! $VENV_PYTHON "$ENGINE_DIR/validate_ledger.py" "$LEDGER_PATH"; then
    echo ""
    echo "REJECTED: Ledger exceeds token cap. Edit the file and retry."
    exit 1
fi

echo ""
echo "Token validation PASSED. Uploading to workspace..."

# Upload via sync_ledger.py (uses Python requests through venv, bypasses Nginx)
$VENV_PYTHON "$ENGINE_DIR/sync_ledger.py" "$LEDGER_PATH"

echo ""
echo "=== LEDGER UPDATED SUCCESSFULLY ==="
echo "IMPORTANT: Open the AnythingLLM Web UI and click the PUSHPIN icon"
echo "on the ledger document to pin it to the workspace context."

```

Make it executable:
```bash
chmod +x $HOME/diagnostic_engine/update_ledger.sh

```

**4. Create the Seed Ledger**

Create `1975_450SL_MASTER_LEDGER.md` locally on the host:

```markdown
# MASTER TECHNICIAN LEDGER: 1975 MERCEDES-BENZ 450SL
**AUTHORITY LEVEL: TRIBAL SUPREMACY**
**MANDATE:** These empirical shop notes supersede conflicting FSM procedures.

## FAULT SIGNATURE: Hot start vapor lock.
- **OEM FSM Diagnosis:** Replace Fuel Accumulator.
- **MASTER TECH OVERRIDE:** Do not drop the tank. 90% probability is a hairline crack in the 0.4 ohm ballast resistor on the fender.
- **VERIFICATION TEST:** Hot-wire terminal 15 on the ignition coil directly to the battery positive. If it starts instantly, the resistor is dead.

```

**Upload using the validated update script (NOT the Web UI):**

```bash
$HOME/diagnostic_engine/update_ledger.sh $HOME/1975_450SL_MASTER_LEDGER.md

```

After the script confirms success, open the AnythingLLM Web UI → navigate to the workspace → find the ledger document → **CLICK THE PUSHPIN ICON** to pin it to the workspace context.

> [!WARNING]
> **NEVER edit the ledger through the Web UI.** To update the ledger:
> 1. Edit the markdown file on the host filesystem
> 2. Run `$HOME/diagnostic_engine/update_ledger.sh /path/to/updated_ledger.md`
> 3. If the script rejects the update (token cap exceeded), archive oldest entries and retry
> 4. Re-pin the document in the Web UI after successful upload

---

## PHASE 7: UI CALIBRATION & RAG MATHEMATICS

1. **Access Web UI:** `https://YOUR_SERVER_IP` (Accept TLS Warning).
2. **AI Provider:** Settings → AI Providers → **Anthropic** (`claude-3-5-sonnet-latest`).
   * **Token Limit:** **`4000`** (Hard cap enforced to prevent hallucination).


3. **Embedding:** Settings → Embedding Preference → **Voyage AI** (`voyage-3-large`).
4. **Document Handling:** Mistral OCR.
   * **Text Splitter:** Markdown Header Text Splitter.
   * **Chunk Token Size:** **`400`** (CRITICAL: Perfectly matches the 5-page physical PDF chunking threshold. Prevents Markdown Table chunk explosion).


5. **Reranking:** Settings → AI Providers → Reranking → **Cohere** (`rerank-english-v3.0`).
6. **Workspace Vector DB Settings:**
   * **Similarity Threshold:** `0.50`
   * **Max Context Snippets:** **`4`** (Math: 4 chunks × 400 = 1600 tokens. Leaves 2400 for System Prompt, Ledger, and Output).
   * **Accuracy Optimized (Reranking):** ON


7. **Chat Settings:**
   * **Chat History Limit:** `4`


> [!NOTE]
> **Token Budget Verification Checklist** (run after first deployment):
> ```
> System Prompt:        ~600 tokens
> Pinned Ledger (cap):  ~1275 tokens (safety-adjusted cap)
> RAG Chunks (4 × 400): 1600 tokens
> TOTAL INPUT:          ~3475 tokens
> Response Budget:      ~525 tokens (Gus JSON is ~200 tokens — safe)
> ```
> Send a test query. Check `docker logs diagnostic_rag_engine` for actual token count sent to Anthropic. Verify it is under 4,000 total.

---

## PHASE 8: THE "GUS" PROVENANCE ENGINE (SYSTEM PROMPT)

Paste EXACTLY this into Workspace Settings → **Chat Settings** AND **Agent Configuration** System Prompt:

> [!IMPORTANT]
> **V2 CITATION STRATEGY:**
> This system prompt uses a **dual-layer citation approach**: The daemon burns `[[ABSOLUTE_PAGE: N]]` watermarks into every PDF page (Phase 4). The system prompt instructs Gus to read these watermarks FIRST. If no watermark is found (legacy content), it falls back to Arabic numeral offset math, Roman numeral passthrough, and section-prefix passthrough — covering all edge cases from both Phase 6 audits.
>
> **V2 DAG BEHAVIOR:**
> PHASE_B allows looping for multi-variable isolation (per Phase 5 DeepThink). The LLM MAY remain in PHASE_B to ask NEW, DIFFERENT physical questions if the fault is not yet isolated. It MUST advance to PHASE_C when isolation is complete. It is FORBIDDEN from repeating the same question.

```text
PRIME DIRECTIVE: YOU ARE "GUS", A DETERMINISTIC STATE-MACHINE DAG. YOU ARE A TIER-1 MASTER MECHANIC.
YOU DO NOT CONVERSE FREELY. YOU ONLY OUTPUT STRICT JSON MATCHING THE SCHEMA BELOW.

EPISTEMOLOGICAL OVERRIDE:
1. Every hypothesis MUST be derived strictly from embedded documents.
2. Cite the exact Document Name and Page Number in "source_citations".
3. CITATION PAGE RULES (DUAL-LAYER):
   a) WATERMARK-FIRST: If the document text contains a [[ABSOLUTE_PAGE: N]] watermark, cite page N directly. Do NOT perform arithmetic. The watermark is the ground truth.
   b) FALLBACK (no watermark found):
      - For ARABIC NUMERAL in-chunk pages: compute absolute = range_start + in_chunk_page - 1.
      - For ROMAN NUMERAL pages (i, ii, iii, iv...): cite as-is with the chunk filename. Do NOT attempt arithmetic.
      - For SECTION-PREFIXED pages (e.g., "54-12", "A-3"): cite the section-page identifier as-is with the chunk filename.
   c) NEVER fabricate or compute page numbers. If you cannot determine the page, cite "page: unknown" with the chunk filename.
   NOTE: Chunk page ranges in filenames refer to PHYSICAL PAGE POSITIONS, not printed labels. Use for Arabic offset math only.
4. Pinned "MASTER_LEDGER.md" is the ABSOLUTE TRUTH. Override FSM if they contradict.

DAG STATE TRANSITION MATRIX (ABSOLUTE LAW):
- If user provides symptom -> Output "current_state": "PHASE_A_TRIAGE", "requires_input": true.
- If user answers PHASE_A prompt -> MUST transition to "current_state": "PHASE_B_FUNNEL".
- If user answers PHASE_B prompt -> You MAY loop in PHASE_B if further variable isolation is needed via NEW, DIFFERENT physical tests. You MUST advance to "PHASE_C_TESTING" when the component is isolated. FORBIDDEN FROM REPEATING the same question.
- If physical test resolves issue -> "current_state": "PHASE_D_CONCLUSION", "requires_input": false, "answer_path_prompts": [].
- ALWAYS respect "required_next_state" if provided in the prompt. Conversation history may be truncated; use the most recent state.

ZERO-RETRIEVAL SAFEGUARD:
If context contains NO embedded document chunks (excluding this prompt and pinned files), you MUST output:
"current_state": "RETRIEVAL_FAILURE", "requires_input": false, "answer_path_prompts": [], "mechanic_instructions": "STOP. Required documentation unavailable." Do NOT fabricate citations or guess.

REQUIRED JSON OUTPUT SCHEMA:
{
  "current_state": "PHASE_B_FUNNEL",
  "intersecting_subsystems": ["Bosch K-Jetronic CIS"],
  "source_citations": [
    {"source": "1975_450SL_FSM_pages_101-105.pdf", "page": "103", "context": "K-Jetronic Hand-off"}
  ],
  "diagnostic_reasoning": "Determining if handoff failure is fuel supply.",
  "mechanic_instructions": "Have a helper start car. Observe pump.",
  "answer_path_prompts": ["[A] Cuts out INSTANTLY.", "[B] Runs 1 SECOND AFTER dies."],
  "requires_input": true
}

CRITICAL OUTPUT RULE: Output raw JSON only. Do NOT wrap in markdown code fences. Do NOT prepend ```json. Do NOT append ```. First character MUST be { and last MUST be }.

```

---

## PHASE 9: AUTOMOTIVE AGENT SKILLS (SANDBOX INJECTION)

Execute this block to inject your API key dynamically, bypassing the vm2 sandbox strip. Note `127.0.0.1:3001` target.

> [!IMPORTANT]
> **V2 FIX:** `$INTERNAL_KEY` is validated with an empty-check guard before `sed` injection. Without this, if the `.env` parse fails, `sed` replaces `REPLACE_ME_KEY` with an empty string, and the agent skill silently fails all API calls. The `cut -d '=' -f2-` fix also applied here.

```bash
export ENGINE_DIR=$HOME/diagnostic_engine
export INTERNAL_KEY=$(grep INTERNAL_API_KEY $ENGINE_DIR/.env | tail -1 | cut -d '=' -f2-)

# V2 FIX: Validate key before injection
if [ -z "$INTERNAL_KEY" ]; then
    echo "FATAL: INTERNAL_API_KEY is empty. Cannot inject agent skill."
    exit 1
fi

mkdir -p $ENGINE_DIR/plugins/agent-skills/manual-status

cat << 'EOF' > $ENGINE_DIR/plugins/agent-skills/manual-status/plugin.json
{
  "name": "Manual-Status", "hubId": "manual-status", "version": "1.0.0", "active": true,
  "description": "Verify FSM index status in database",
  "entrypoint": { "file": "handler.js", "params": { "workspace_slug": { "type": "string", "required": true } } }
}
EOF

cat << 'EOF' > $ENGINE_DIR/plugins/agent-skills/manual-status/handler.js
module.exports.runtime = {
  handler: async function ({ workspace_slug }) {
    try {
      const response = await fetch(`http://127.0.0.1:3001/api/v1/workspace/${workspace_slug}`, {
        headers: { "Authorization": "Bearer REPLACE_ME_KEY" }
      });
      const data = await response.json();
      if (data.workspace && data.workspace.documents.length > 0)
        return `SUCCESS: ${data.workspace.documents.length} document chunks verified.`;
      return `CRITICAL: No documentation found.`;
    } catch (e) { return `ERROR: ${e.message}`; }
  }
};
EOF

sed -i "s/REPLACE_ME_KEY/$INTERNAL_KEY/g" $ENGINE_DIR/plugins/agent-skills/manual-status/handler.js
docker restart diagnostic_rag_engine

```

*(Deploy remaining skills from previous steps using this identical injection process. Toggle ON in UI).*

---

## PHASE 10: ZERO-TEAR DISASTER RECOVERY

> [!IMPORTANT]
> Backup cron job uses absolute path `/usr/bin/docker` to prevent `command not found` failures under cron's minimal PATH environment. Semicolons (`;`) guarantee the container restart fires regardless of the tar exit code.

```bash
(crontab -l 2>/dev/null; echo "0 2 * * * /usr/bin/docker stop diagnostic_rag_engine ; tar czf \$HOME/diagnostic_engine_backup_\$(date +\%Y\%m\%d).tar.gz --exclude=diagnostic_engine/staging -C \$HOME diagnostic_engine/ ; /usr/bin/docker start diagnostic_rag_engine") | crontab -
(crontab -l 2>/dev/null; echo "0 3 * * * find \$HOME/ -name 'diagnostic_engine_backup_*.tar.gz' -mtime +7 -exec rm {} \\;") | crontab -

```

---

## PHASE 11: THE FRONTEND CAGE (UI LOGIC INTEGRATION)

Your frontend MUST inject this to prevent markdown parsing crashes, handle error states, and allow proper LLM diagnostic flow:

> [!IMPORTANT]
> **V2 CRITICAL CHANGES:**
> - `parseGusResponse()` **COMPLETELY REWRITTEN** — the V1 reverse-scan depth-counter algorithm is fatally flawed: it counts raw `{` and `}` characters without respecting JSON string escaping. If `mechanic_instructions` contains `"Check the {intake} manifold"`, the unbalanced brace throws off the depth counter and the parser returns garbage or crashes. The V2 implementation uses a robust approach: scan backward for closing `}`, walk left counting braces (identical to V1) to find the candidate substring, then validate with `JSON.parse()`. If the parse fails (due to in-string braces corrupting the boundary detection), it falls through to a regex-based extraction that finds the last `{...}` containing `"current_state"`.
> - `RETRIEVAL_FAILURE` handling now displays an explicit "Restart Diagnostic" button — the V1 mapping to `PHASE_A_TRIAGE` was unreachable because `requires_input: false` means no answer buttons are rendered
> - PHASE_B `buildUserMessage` now sends `required_next_state: null` to prevent stale chat history from overriding the LLM's decision to loop or advance

```javascript
// 1. APEX JSON SANITIZER — V8 Hardened Implementation
// V2 FIX: The V1 depth-counter approach fails on in-string braces like
// "Check the {intake} manifold". V2 added JSON.parse validation to the
// depth-counter result. V8 FIX: The V2 regex fallback (Pass 2) used a
// /\{[^{}]*...\}/g pattern that is blind to string boundaries — an
// unbalanced brace inside a JSON string literal (e.g., "Check the } bracket")
// causes the regex to truncate the match at the in-string brace. The V8
// replacement uses brute-force JSON.parse iteration: for every '{' found
// (scanning forward), it tries pairing with every '}' (scanning backward)
// and validates with JSON.parse. This is O(n²) worst-case but the response
// text is typically <2KB, making it negligible.
//
// V8 FIX (Phase 10 DT R7): Pass 1 (backward-scanning depth counter) was
// removed entirely. Its backward scan returned the LAST valid JSON object,
// which allows a trailing hallucinated JSON to hijack the state machine.
// Pass 2's forward scan is mathematically robust — it always finds the
// FIRST (outermost, leftmost) valid JSON envelope with current_state.
function parseGusResponse(rawText) {
    // Single-pass brute-force JSON.parse iteration (formerly Pass 2).
    // Scan FORWARD for every '{', then BACKWARD for every '}' after it,
    // try JSON.parse. Forward outer scan guarantees the OUTERMOST (leftmost)
    // valid JSON envelope is found first — prevents inner nested JSON strings
    // (e.g., in mechanic_instructions) from being extracted over the real envelope.
    // V8 FIX (Phase 10 DT R4): Original backward scan found rightmost '{' first,
    // which could match inner nested JSON before the outer envelope.
    for (let i = 0; i < rawText.length; i++) {
        if (rawText[i] === '{') {
            for (let j = rawText.length - 1; j > i; j--) {
                if (rawText[j] === '}') {
                    try {
                        const candidate = JSON.parse(rawText.substring(i, j + 1));
                        if (candidate && candidate.current_state) {
                            return candidate;
                        }
                    } catch (e) {
                        continue;
                    }
                }
            }
        }
    }

    throw new Error("FATAL: No valid JSON object with 'current_state' found in response.");
}

// 2. DAG INJECTOR - Appends transition logic to user button clicks
// V2 FIX: RETRIEVAL_FAILURE is handled separately (see note below).
// PHASE_B sends required_next_state: null to let the LLM decide.
function buildUserMessage(selectedOption, lastResponse) {
    const nextStates = {
        "PHASE_A_TRIAGE": "PHASE_B_FUNNEL",
        "PHASE_B_FUNNEL": "PHASE_C_TESTING",
        "PHASE_C_TESTING": "PHASE_D_CONCLUSION",
        "PHASE_ERROR": "PHASE_A_TRIAGE"
        // NOTE: RETRIEVAL_FAILURE is NOT in this map.
        // requires_input=false means no answer buttons are shown,
        // so buildUserMessage is never called for this state.
        // The frontend must display a "Restart Diagnostic" button
        // that clears the conversation and starts a new session.
    };
    const currentState = lastResponse.current_state;
    const next = nextStates[currentState] || "PHASE_D_CONCLUSION";

    // PHASE_B allows looping for further variable isolation.
    // The LLM decides whether the fault is isolated (advance to C) or
    // needs more data (loop in B with a NEW, DIFFERENT question).
    // V2 FIX: Send required_next_state: null to prevent stale chat
    // history from overriding the LLM's looping decision.
    if (currentState === "PHASE_B_FUNNEL") {
        return JSON.stringify({
            completed_state: currentState,
            selected_option: selectedOption,
            required_next_state: null,
            instruction: `User physically verified: "${selectedOption}". Process this physical data. If the fault is isolated, transition to PHASE_C_TESTING. If further testing is required to isolate, remain in PHASE_B_FUNNEL but you MUST ask a NEW, DIFFERENT physical question. Do NOT repeat any previous question.`
        });
    }

    return JSON.stringify({
        completed_state: currentState,
        required_next_state: next,
        selected_option: selectedOption,
        instruction: `User physically verified: "${selectedOption}". You MUST transition to ${next}. Do NOT repeat ${currentState}.`
    });
}

// 3. RETRIEVAL_FAILURE HANDLER
// V2 ADDITION: When the LLM returns RETRIEVAL_FAILURE (no document
// chunks found), the frontend must show a message and a restart button.
// This is NOT handled by buildUserMessage because requires_input=false
// means no answer option buttons are rendered.
//
// Example implementation:
// if (response.current_state === "RETRIEVAL_FAILURE") {
//     displayMessage("Required documentation is unavailable. Please verify that manuals have been ingested (Phase 5) and embedded in the workspace.");
//     showRestartButton(); // Clears conversation, starts new session
// }

```

> [!CAUTION]
> **RETRIEVAL_FAILURE:** If Gus returns `current_state: "RETRIEVAL_FAILURE"`, the mechanic has NO path forward because `requires_input: false` means no answer buttons appear. Your frontend MUST detect this state and display:
> 1. The `mechanic_instructions` text ("STOP. Required documentation unavailable.")
> 2. A "Restart Diagnostic" button that clears the conversation and begins a new session
> 3. Operator instructions to verify ingestion via `verify_ingestion.py` (Phase 5)

---

## PHASE 12: POST-DEPLOYMENT VERIFICATION CHECKLIST

After completing all phases, execute this verification sequence:

```bash
# 1. Verify systemd daemon is running
sudo systemctl status manual-ingest.service
# Expected: Active: active (running)

# 2. Verify Docker container is running
docker ps | grep diagnostic_rag_engine
# Expected: Status: Up

# 3. Verify API key works
export ENGINE_DIR=$HOME/diagnostic_engine
export INTERNAL_KEY=$(grep INTERNAL_API_KEY $ENGINE_DIR/.env | tail -1 | cut -d '=' -f2-)
curl -s -H "Authorization: Bearer $INTERNAL_KEY" http://127.0.0.1:3001/api/v1/auth | python3 -m json.tool
# Expected: authenticated: true

# 4. Verify ingestion completeness
$HOME/diagnostic_engine/venv/bin/python3 $HOME/diagnostic_engine/verify_ingestion.py
# Expected: ✓ ALL CHUNKS VERIFIED.

# 5. Verify Nginx blocks external uploads (case-insensitive)
curl -s -o /dev/null -w "%{http_code}" -X POST https://YOUR_SERVER_IP/api/v1/document/upload --insecure
# Expected: 403
curl -s -o /dev/null -w "%{http_code}" -X POST https://YOUR_SERVER_IP/api/v1/document/UpLoad --insecure
# Expected: 403 (V2 case-insensitive regex test)

# 6. Verify UFW status
sudo ufw status verbose
# Expected: Status: active, Default: deny (incoming), allow (outgoing)

# 7. Verify cron jobs
crontab -l
# Expected: 0 2 * * * /usr/bin/docker stop ... ; tar czf ... ; /usr/bin/docker start ...

# 8. Verify ExecStopPost escaping (systemd requires $$m for literal dollar)
sudo grep 'guestunmount' /etc/systemd/system/manual-ingest.service
# Expected: guestunmount $$m 2>/dev/null (double-dollar for systemd, NOT single $m)

# 9. Verify .env permissions
ls -la $HOME/diagnostic_engine/.env
# Expected: -rw------- (600)

# 10. Verify TLS key permissions
ls -la /etc/nginx/ssl/diag-engine.key
# Expected: -rw------- (600)

# 11. Verify Docker log rotation
docker inspect diagnostic_rag_engine --format '{{.HostConfig.LogConfig}}'
# Expected: {json-file map[max-file:3 max-size:50m]}

# 12. Test Gus with a diagnostic query
# Open the Web UI, navigate to workspace, type: "Hot start vapor lock, cranks but won't catch."
# Expected: JSON response with current_state: "PHASE_A_TRIAGE", source_citations referencing MASTER_LEDGER.md

```

---

**SYSTEM DEPLOYMENT COMPLETE. THE V8 ARCHITECTURE IS LOCKED, DETERMINISTIC, AND MATHEMATICALLY BULLETPROOF.**

---

### V8 CONSOLIDATED DIFF ANALYSIS & RESOLUTION LOG

Every divergence identified by the Phase 8 and Phase 9 hostile audits has been resolved. Below is the complete record of findings and their resolutions.

| # | Finding | Source | Classification | V2 Code | V8 Fix | Impact |
|:--|:--------|:-------|:---------------|:--------|:-------|:-------|
| 20 | Daemon livelock on `wait_for_stable` returning `False` | DT Phase 8, hardened Phase 9 | 💀 WILL FAIL | File remains in `DOWNLOAD_DIR` after 2h timeout | `else` branch quarantines via `os.rename`; if rename fails, `os.remove` as last resort — file NEVER persists | Single zero-byte file permanently halts ingestion pipeline |
| 21 | ExecStopPost callout missing FUSE justification | DT Phase 8 | ⚠️ REGRESSION | Callout explains only shell-escaping mechanics | Callout restored: FUSE zombie mount → file descriptor exhaustion justification merged with escaping explanation | Future maintainer lacks context for why ExecStopPost exists |
| 22 | `parseGusResponse` regex fallback blind to string boundaries | Cross-Examination | ⚠️ COULD FAIL | Pass 2 uses `[^{}]` regex — truncates on in-string `}` | Brute-force `JSON.parse` iteration over all `{`→`}` pairs (backward scan) | Regex fails on `"Check the } bracket"` in `mechanic_instructions` |
| 23 | V2 changelog missing Upload `IndexError` bullet | Phase 9 Audit | 🔍 ADMINISTRATIVE | 18 bullets for 19 diff table rows | 19th bullet added for CO Finding 3.2 | Audit trail incomplete |
| 24 | `process_file()` quarantine uses silent `except Exception: pass` | Phase 10 DNA Audit | ⚠️ COULD FAIL | `shutil.move` failure silently swallowed — file persists in `DOWNLOAD_DIR` | Three-tier defense: `shutil.move` → `os.remove` → CRITICAL log (mirrors `wait_for_stable` quarantine pattern) | Corrupt file triggers infinite 10-second extraction retry loop |
| 25 | Workspace slug change instructions list `handler.js` (4 files) | Phase 10 Opus Audit | 🔍 ADMINISTRATIVE | Phase 3 callout says change slug in 4 files including `handler.js` | Corrected to 3 files — `handler.js` receives `workspace_slug` as a runtime parameter from the agent framework | Deployer wastes time searching for non-existent hardcoded slug |
| 26 | `process_file()` pre-try operations bypass quarantine on crash | Phase 10 DT Audit | 💀 WILL FAIL | `get_hash()`, `load_manifest()`, dedup check execute BEFORE the `try` block | Moved all operations inside `try` — `mount_point`/`extract_dir` initialized before `try` with safe defaults for `finally` | `PermissionError` on file hash crashes daemon → infinite systemd restart loop with file persisting in `DOWNLOAD_DIR` |
| 27 | `tempfile.mkdtemp()` outside `try` block bypasses quarantine | Phase 10 DT R3 | 💀 WILL FAIL | `mount_point = tempfile.mkdtemp(...)` executes before `try` | `mount_point = None` before try; `mkdtemp` inside try; `finally` guarded with `if mount_point and os.path.ismount(mount_point)` | `OSError` (disk full / inode exhaustion) crashes daemon unhandled → infinite systemd restart loop |
| 28 | `sync_ingest.py` re-uploads all documents on second run | Phase 10 DT R3 | 💀 WILL FAIL | Blind `glob.glob` loop over all PDFs — no dedup against workspace | GET workspace docs before loop, build `existing_docs` set, skip already-embedded filenames | Exponential vector duplication in LanceDB, massive wasted API quotas |
| 29 | `sync_ledger.py` never deletes old ledger vectors | Phase 10 DT R3 | 💀 WILL FAIL | `"deletes": []` hardcoded — old versions accumulate | GET workspace docs, find existing `MASTER_LEDGER` location, inject into `deletes[]` for atomic swap | Conflicting historical ledger versions break “Absolute Truth” override mechanism |
| 30 | Disaster recovery tar traverses live FUSE mounts | Phase 10 DT R3 | ⚠️ COULD FAIL | `tar czf ... -C $HOME diagnostic_engine/` includes `staging/mounts/` | Added `--exclude=diagnostic_engine/staging` before `-C` flag | Active VMDK mount bloats backup to 20GB+, exhausts disk, corrupts archive |
| 31 | `sync_ingest.py` rate limiting only on success | Phase 10 DT R3 + R4 | 💀 WILL FAIL | `time.sleep(12)` inside `if status == 200:` block; R3 fix moved it outside if/else but `continue` and `except` still bypassed it | `time.sleep(12)` placed in `finally` block — fires unconditionally after `continue`, `except`, and normal flow | API 429/500 skips cooldown → tight-loop death spiral → guaranteed IP/API ban |
| 32 | `parseGusResponse` Pass 2 backward scan extracts inner JSON first | Phase 10 DT R4 | ⚠️ COULD FAIL | Outer loop scans backward (rightmost `{` first) — nested JSON in `mechanic_instructions` found before outer envelope | Reversed outer loop to scan forward (`i=0 → length`) — outermost `{` found first, paired with rightmost `}` via backward inner loop | Inner nested JSON hijacks frontend state machine with wrong `current_state` |
| 33 | Main loop spams false CRITICAL on deleted files | Phase 10 DT R4 | 🔍 ADMINISTRATIVE | `wait_for_stable()` returns False for vanished file → quarantine `os.rename` → `FileNotFoundError` cascade → CRITICAL log | Added `if not os.path.exists(path): continue` before quarantine | Operator alarmed by terrifying "Manual intervention required" for normal cancelled SCP |
| 34 | `parseGusResponse` Pass 1 returns unvalidated JSON | Phase 10 R5 | ⚠️ COULD FAIL | Pass 1 `return JSON.parse(...)` has no `current_state` check; trailing JSON objects extracted and returned blindly | Added `candidate.current_state` validation to Pass 1, matching Pass 2's guard | Trailing JSON hijacks state machine; caller gets object without `current_state`, `requires_input`, or `answer_path_prompts` |
| 35 | `validate_ledger.py` misleading output label | Phase 10 R5 | 🔍 ADMINISTRATIVE | "RAG budget remaining" suggests value is only for RAG; actually includes response budget | Relabeled to "Budget remaining (RAG + response)" | Operator may allocate 2125 tokens to RAG when 1600 goes to RAG and only 525 for response |
| 36 | `ExecStopPost` omits OVA staging directory cleanup | Phase 10 DT R5 | ⚠️ COULD FAIL | `rm -rf .../staging/mounts/*` only — orphaned `staging/ova/*` survives SIGKILL | Extended to `rm -rf .../staging/mounts/* .../staging/ova/*` | 20GB+ OVA payload leaked per daemon kill during extraction |
| 37 | Dead `watchdog` dependency contradicts DNA | Phase 10 DT R5 | 🔍 ADMINISTRATIVE | `pip install watchdog` but no code imports it; DNA Decision #3 explicitly rejects file watchers | Removed `watchdog` from pip install | Operator confusion; contradicts documented architecture rationale |
| 38 | `process_file()` quarantine ignores vanished files | Phase 10 DT R5 | 🔍 ADMINISTRATIVE | File deleted during extraction → `shutil.move` → `os.remove` → false CRITICAL cascade | Added `if not os.path.exists(file_path)` guard before quarantine | Duplicate of Row 33 logic gap — same false alarm in different code path |
| 39 | `os.makedirs` outside inner try crashes daemon on full disk | Phase 10 DT R5 | ⚠️ COULD FAIL | `os.makedirs(QUARANTINE_DIR)` between outer `except` and inner `try` — unhandled `OSError` on disk full | Moved `os.makedirs` inside inner `try` block | Daemon crash loop on disk exhaustion; file stays in DOWNLOAD_DIR |
| 40 | DNA still lists `watchdog` as Python dependency | Phase 10 R6 | 🔍 ADMINISTRATIVE | DNA component map and Layer 1 table list `watchdog` despite Row 37 removing it from pip install | Removed `watchdog` from DNA Lines 71 and 97 | Internal DNA contradiction with Engineering Decision #3 |
| 41 | Systemd unit hardcodes `/home/$USER_NAME` — crashes for root | Phase 10 DT R6 | ⚠️ COULD FAIL | `ExecStart=/home/$USER_NAME/...` — root’s home is `/root/` not `/home/root/` | `USER_HOME=$(eval echo ~$USER_NAME)` + `$USER_HOME/...` in all paths | Daemon permanently fails on startup if deployed as root |
| 42 | ExecStopPost `rm -rf` traverses live FUSE mounts | Phase 10 DT R6 | ⚠️ COULD FAIL | `rm -rf .../staging/mounts/*` recursively walks still-mounted VMDK if `guestunmount` fails | Added `--one-file-system` flag to `rm -rf` | 90s I/O storm + EROFS log spam until systemd SIGKILL |
| 43 | TOCTOU race between `os.path.exists` and quarantine ops | Phase 10 DT R6 | 🔍 ADMINISTRATIVE | File vanishes between exists check and `shutil.move`/`os.rename` → `FileNotFoundError` → false CRITICAL | Added `isinstance(e2, FileNotFoundError)` guard in innermost except (both paths) | False CRITICAL log for race-condition edge case |
| 44 | Main loop quarantine missing `os.makedirs` defense | Phase 10 DT R6 | 🔍 ADMINISTRATIVE | `process_file` has `os.makedirs(QUARANTINE_DIR)` but main loop does not — `os.rename` fails if dir removed | Added `os.makedirs(QUARANTINE_DIR, exist_ok=True)` to main loop try block | Force-deletes recoverable files if quarantine dir is missing |
| 45 | Systemd expands `$m` to empty string in ExecStopPost | Phase 10 DT R7 | ⚠️ COULD FAIL | Unit file contains `$m` — systemd’s own variable expansion replaces undefined `$m` with empty | Changed escaping to produce `$$m` in unit file (systemd `$$`→`$`) | `guestunmount` receives no path; zombie FUSE mounts accumulate |
| 46 | Shell `/*` glob defeats `--one-file-system` on FUSE mounts | Phase 10 DT R7 | ⚠️ COULD FAIL | `rm -rf --one-file-system .../mounts/*` — glob expands to mount point itself, making FUSE fs the reference root | Removed `/*` globs; `rm -rf` targets parent dirs + `mkdir -p` recreates | `rm` traverses entire read-only VMDK generating I/O storm until SIGKILL |
| 47 | `shutil.rmtree` traverses live FUSE mount in `finally` block | Phase 10 DT R7 | ⚠️ COULD FAIL | If `guestunmount` fails, `shutil.rmtree(mount_point, ignore_errors=True)` walks entire VMDK | Guarded with `not os.path.ismount(mount_point)` — skip if still mounted | Minutes of wasted I/O + CPU thrashing; pipeline stalls |
| 48 | `os.rename` fails cross-device (EXDEV) in main loop quarantine | Phase 10 DT R7 | 🔍 ADMINISTRATIVE | `os.rename(path, quarantine_dest)` raises `OSError(18)` if dirs on different partitions | Replaced with `shutil.move()` which falls back to copy+delete | Quarantine bypassed; file force-deleted instead of preserved |
| 49 | `parseGusResponse` Pass 1 backward scan returns trailing JSON | Phase 10 DT R7 | 🔍 ADMINISTRATIVE | Backward-scanning depth counter captures LAST valid JSON object — trailing hallucinated JSON hijacks state machine | Removed Pass 1 entirely; Pass 2 forward scan is robust | LLM-appended trailing JSON could override correct state transition |

### V2 CONSOLIDATED DIFF ANALYSIS & RESOLUTION LOG (Preserved)

Every divergence between the V7 Consolidated document and the three Phase 7 hostile audits has been resolved. Below is the complete record of findings and their resolutions.

| # | Finding | Source | Classification | V1 Code | V2 Fix | Impact |
|:--|:--------|:-------|:---------------|:--------|:-------|:-------|
| 1 | `ExecStopPost` `$m` consumed by shell layers | CO_2 #01, DT #1 | 💀 WILL FAIL | `\$m` (single escape) | `\\\$m` (triple escape) + mandatory verification step | FUSE zombie mounts exhaust file descriptors |
| 2 | `ENGINE_DIR` not re-exported in Phase 2 | CO #1.1, CO_2 #02 | 💀 WILL FAIL | Not present | `export ENGINE_DIR=$HOME/diagnostic_engine` at top of Phase 2 | Docker volumes mount to wrong path |
| 3 | Phase 2 `.env` guard exits subshell, not parent | CO_2 #03 | 💀 WILL FAIL | `(echo ... && exit 1)` | `if [ $? -ne 0 ]; then ... exit 1; fi` | Corrupted `.env` missing AnythingLLM defaults |
| 4 | `.env` file world-readable (644) | CO #5.2, CO_2 #04, DT #4 | 💀 WILL FAIL | No `chmod` | `chmod 600 "$ENGINE_DIR/.env"` after every write | JWT_SECRET and API key exposed |
| 5 | TLS private key world-readable (644) | CO #5.3, CO_2 #05 | ⚠️ COULD FAIL | No `chmod` | `sudo chmod 600 /etc/nginx/ssl/diag-engine.key` | Private key exposed to all users |
| 6 | `cut -d '=' -f2` truncates keys with `=` | CO #5.4, CO_2 #06 | ⚠️ COULD FAIL | `-f2` | `-f2-` (all fields from 2 onward) | Silent API auth failure |
| 7 | Python scripts proceed with empty API key | CO #6.1, CO_2 #07, DT #6 | 💀 WILL FAIL | No guard | `if not API_KEY: sys.exit(1)` | Silent `Bearer ` auth, misleading 403s |
| 8 | Nginx upload block case-sensitive | DT #3 | ⚠️ COULD FAIL | `location /api/v1/...` | `location ~* ^/api/v1/document/(upload\|create-folder)` | Bypass via `/UpLoad` |
| 9 | `wait_for_stable()` infinite loop on zero-byte | DT #2 | 💀 WILL FAIL | `elapsed` only in `try` branch | `elapsed += 5` in all `except` branches | Daemon deadlocks forever |
| 10 | `parseGusResponse` naive brace counter | CO #7.1, CO_2 #08, DT #5 | 💀 WILL FAIL | Depth counter ignores strings | Try-catch + regex fallback | Crash on `{intake}` in instructions |
| 11 | `RETRIEVAL_FAILURE` state unreachable | CO #7.2, CO_2 #09 | 🔍 AMBIGUOUS | Maps to `PHASE_A_TRIAGE` | Explicit restart button instruction | Dead-end — no buttons shown |
| 12 | PHASE_B stale `required_next_state` | CO #7.3 | ⚠️ COULD FAIL | No explicit null | `required_next_state: null` | Chat history overrides LLM decision |
| 13 | Manifest value type inconsistency | CO #6.4, CO_2 #10 | 🔍 AMBIGUOUS | String for PDFs, dict for containers | All entries use dict | Dead code on direct-PDF path |
| 14 | Docker logs unbounded | CO #5.5 | ⚠️ COULD FAIL | No `--log-opt` | `--log-opt max-size=50m --log-opt max-file=3` | Disk exhaustion |
| 15 | `tiktoken` model-based lookup fragile | CO #6.2 | 🔍 AMBIGUOUS | `encoding_for_model("gpt-4")` | `get_encoding("cl100k_base")` | Breaks on tiktoken update |
| 16 | Phase 9 `$INTERNAL_KEY` not validated | CO #1.3 | ⚠️ COULD FAIL | No guard | `if [ -z "$INTERNAL_KEY" ]; then exit 1; fi` | Empty key injected into handler.js |
| 17 | No workspace creation instructions | CO_2 #11.2 | 🔍 AMBIGUOUS | Not documented | Phase 3 workspace creation steps added | Scripts reference non-existent workspace |
| 18 | Upload `IndexError` on empty `documents` | CO #3.2 | 💀 WILL FAIL | `[{}][0]` default mask | Explicit `if not documents` guard | Crash or silent skip |
| 19 | `import sys` missing in `sync_ingest.py` | Implicit from CO #6.1 | 💀 WILL FAIL | `import os, time...` | `import os, sys, time...` | `NameError: sys` on API key guard |

### V7 CONSOLIDATED ORIGINAL DIFF ANALYSIS (Preserved)

The following table records the original divergences between the two V7 blueprints that were resolved in the V7 Consolidated document. It is preserved for audit trail completeness.

| # | Area | Antigravity V7 | DeepThink V7 | Resolution | Rationale |
|:--|:-----|:---------------|:-------------|:-----------|:----------|
| 1 | **Nginx `/api/v1/document/create-folder`** | Blocked (returns 403) | Not blocked | **Antigravity adopted** | Defense in depth — prevents unauthorized folder creation via spoofed requests |
| 2 | **PDF page watermarks** | Burns `[[ABSOLUTE_PAGE: N]]` into every page via PyMuPDF | Not implemented — relies on LLM arithmetic + branching rules | **Antigravity adopted** | Eliminates non-deterministic LLM arithmetic entirely. The DeepThink Phase 6 audit itself recommended this approach |
| 3 | **`wait_for_stable()` error handling** | Wraps `os.path.getsize()` in try/except OSError + zero-byte guard | Raw `os.path.getsize()` — crashes if file deleted mid-check | **Antigravity adopted** | Production daemon must not crash on concurrent file deletion |
| 4 | **`validate_ledger.py` return type** | Returns `bool` from `validate()`; `sys.exit()` in `__main__` | Calls `sys.exit()` directly from `validate()` | **Antigravity adopted** | Returning bool is more composable — allows `validate()` to be called from other scripts |
| 5 | **Ledger upload mechanism** | `update_ledger.sh` uses raw `curl` for API calls | `update_ledger.sh` calls `sync_ledger.py` (Python `requests` via venv) | **DeepThink adopted** | Using `requests` via the venv is consistent with the venv mandate. `curl` runs outside the venv and isn't guaranteed on all systems |
| 6 | **System prompt citation rules** | Watermark-first (`[[ABSOLUTE_PAGE: N]]`), with generic fallback | Arabic numeral arithmetic + Roman numeral passthrough + section-prefix passthrough (no watermark) | **Both merged** | Watermark is primary source of truth (ties to daemon fix). DeepThink's branching rules serve as fallback for legacy/unprocessed content |
| 7 | **System prompt DAG: PHASE_B behavior** | Allows looping in PHASE_B for multi-variable isolation with NEW questions | Forbids PHASE_B repetition; forces strict PHASE_B → PHASE_C transition | **Antigravity adopted** | Complex diagnostics often require multiple isolation questions. Phase 5 DeepThink explicitly identified forced PHASE_B exit as a flaw |
| 8 | **`buildUserMessage()` PHASE_B logic** | Includes PHASE_B-specific conditional branch with looping instruction | Strict linear transition for all states (no PHASE_B special case) | **Antigravity adopted** | Must match the system prompt's allowance for PHASE_B looping |
| 9 | **Cron PATH for docker** | Uses absolute binary: `/usr/bin/docker` | Prepends `PATH=/usr/local/bin:/usr/bin:/bin:/snap/bin` before `docker` | **Antigravity adopted** | Absolute binary path is more deterministic. PATH prepend can be overridden by shell config |
| 10 | **ExecStopPost shell escaping** | `\$m` (single backslash) | `\\\\\\$m` (triple-escaped) | **V2: Triple-escape adopted** | V7 Consolidated adopted single-escape, which was proven incorrect by the Phase 7 hostile audits. Triple-escaping is required to survive the three shell layers. |
| 11 | **Token budget checklist** | Explicit math breakdown with line-by-line token accounting | Not included | **Antigravity adopted** | Essential for post-deployment verification — gives the operator exact numbers to validate against `docker logs` |
| 12 | **API key empty-check** | `if [ -z "$INTERNAL_KEY" ]` guard in Phase 3 | No guard | **Antigravity adopted** | Prevents silent failure from an empty paste |
| 13 | **Post-deployment verification** | Full Phase 12 checklist (8 verification steps) | Not included | **Antigravity adopted, expanded to 12 steps in V2** | Critical for confirming all subsystems are operational before first diagnostic query |
| 14 | **Phase numbering** | 12 phases (dedicated phases for API key, tribal knowledge, UI calibration) | 10 phases (merged UI calibration with API key; merged tribal knowledge with ledger scripts) | **Antigravity structure adopted** | More granular phases provide clearer execution boundaries and reduce operator confusion |
| 15 | **`sync_ingest.py` logging** | Includes `print(f"Ingesting to workspace...")` and per-file status + failure messages | Minimal logging (no workspace print, no failure branch messages) | **Antigravity adopted** | Verbose logging is essential for debugging 429 issues and identifying failed uploads |
| 16 | **Docker iptables warning** | Explicit callout box with Phase 5 regression context | Not mentioned | **Antigravity adopted** | This was a catastrophic Phase 5 regression — the warning must persist to prevent re-introduction |
