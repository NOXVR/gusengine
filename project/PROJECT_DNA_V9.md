# PROJECT DNA: THE CLOSED-LOOP AUTOMOTIVE DIAGNOSTIC RAG ENGINE

**Generated from:** `ARCHITECTURE_FINAL_V9.md` — the product of 10 phases of hostile adversarial auditing across 49 verified findings, with 16 gap analysis recovery items applied in V9.

---

## PART 1: THE MISSION

### Who Is This For?

This system serves **two distinct roles**:

- **The knowledge source:** A **master automotive technician** — someone who works on vintage/classic vehicles (the reference implementation targets a **1975 Mercedes-Benz 450SL**) and has accumulated decades of empirical diagnostic knowledge that contradicts or supersedes what's printed in factory service manuals (FSMs). This person's tribal knowledge is captured in the `MASTER_LEDGER.md`.
- **The end user:** A **junior technician or dealership service department** operating under flat-rate pay pressure, facing 4,000+ page FSMs they can't effectively search, and prone to the **"parts cannon"** approach — guessing which part is broken and swapping it at the customer's expense.

The deployer (who may be neither of these) needs zero Linux experience. The entire system is designed to be deployed by following a linear, copy-paste-verbatim set of instructions on a bare-metal Ubuntu server they have physical access to.

### What Problem Does This Solve?

Automotive diagnostics suffer from a fundamental **Epistemological Gap**: the Factory Service Manual contains one truth, the master tech's tribal knowledge contains a different (often more accurate) truth, and standard LLMs — if asked directly — hallucinate a third. The result is three competing information sources with no arbitration system.

This gap has real economic consequences. Take the 1975 450SL hot start vapor lock. The FSM says "Replace Fuel Accumulator" — an $800 tank drop. A master tech who's seen this fault signature 200 times knows the real answer is a $4 ballast resistor on the fender. Without this system, the junior tech follows the FSM, wastes the customer's money, and the shop eats the comeback. When the master tech retires, the knowledge dies entirely.

This system closes that gap. It captures tribal diagnostic knowledge, fuses it with digitized factory service manuals, and creates an AI mechanic named **"Gus"** that walks the junior technician through a structured diagnostic process — using the master tech's overrides as the highest-priority source of truth. The FSM provides the reference. The ledger provides the override. Gus enforces the hierarchy.

### What Is Gus?

**Gus** is the AI persona. He is not a chatbot. He is a **deterministic state-machine DAG** (Directed Acyclic Graph) that outputs strict JSON. He does not converse freely. He does not hallucinate. He does not guess. Every claim he makes must be derived from an embedded document, and every citation must reference a specific document name and page number. (If the page cannot be determined from watermarks or arithmetic, the system prompt permits citing `"page": "unknown"` with the chunk filename as a fallback.)

Gus operates as a **Tier-1 Master Mechanic**: his personality is authoritative, direct, and grounded in physical verification. He never tells a technician to "check the computer" — he tells them to "Have a helper crank the engine while you watch whether the fuel pump rod moves. Report what you see: [A] Rod moves, engine still won't start. [B] Rod doesn't move."

### The Physical Scenario

A technician is standing next to a car in a shop. They have a phone or laptop with the Gus Web UI open. They type a symptom: *"Hot start vapor lock, cranks but won't catch."* Gus walks them through a structured diagnostic tree — asking physical questions, receiving physical answers, and narrowing down to the root cause using both the FSM documentation and the master technician's tribal knowledge overrides.

---

## PART 2: THE ARCHITECTURE

### Component Map

```
┌─────────────────────────────────────────────────────────────────┐
│                      EXTERNAL ACCESS                            │
│  Mechanic's Browser ──HTTPS──▶ Nginx (port 443, TLS)           │
│                                  │                              │
│                        ┌─────────▼─────────┐                   │
│                        │   REVERSE PROXY    │                   │
│                        │  - WebSocket proxy │                   │
│                        │  - Upload blocking │                   │
│                        │  - Security hdrs   │                   │
│                        └─────────┬─────────┘                   │
│                                  │ proxy_pass                   │
│                        ┌─────────▼─────────┐                   │
│                        │  AnythingLLM       │                   │
│                        │  Docker Container  │                   │
│                        │  127.0.0.1:3001    │                   │
│                        │  ┌───────────────┐ │                   │
│                        │  │ LanceDB       │ │    ┌────────────┐│
│                        │  │ (vectors)     │ │    │ External   ││
│                        │  ├───────────────┤ │◄──▶│ AI APIs    ││
│                        │  │ SQLite        │ │    │ - Anthropic││
│                        │  │ (config/keys) │ │    │ - Voyage AI││
│                        │  └───────────────┘ │    │ - Mistral  ││
│                        └───────────────────┘    │ - Cohere   ││
│                                                  └────────────┘│
│  ┌──────────────────────────────────────────┐                   │
│  │         HOST FILESYSTEM                   │                   │
│  │  ~/diagnostic_engine/                     │                   │
│  │  ├── .env (JWT_SECRET + API_KEY, 600)     │                   │
│  │  ├── venv/ (Python: fitz/PyMuPDF, requests, tiktoken) │                   │
│  │  ├── downloads/ ←── mechanic drops files  │                   │
│  │  ├── quarantine/ ←── failed extractions   │                   │
│  │  ├── extracted_manuals/ ←── chunked PDFs  │                   │
│  │  ├── staging/ova/ + staging/mounts/       │                   │
│  │  ├── storage/ (Docker volume)             │                   │
│  │  ├── vmdk_extractor.py (systemd daemon)   │                   │
│  │  ├── sync_ingest.py                       │                   │
│  │  ├── verify_ingestion.py                  │                   │
│  │  ├── validate_ledger.py                   │                   │
│  │  ├── sync_ledger.py                       │                   │
│  │  ├── update_ledger.sh                     │                   │
│  │  └── plugins/agent-skills/               │
│       ├── manual-status/                  │
│       ├── vin-lookup/                     │
│       ├── purchase-router/                │
│       └── draft-tribal-knowledge/         │                   │
│  └──────────────────────────────────────────┘                   │
└─────────────────────────────────────────────────────────────────┘
```

### Layer-by-Layer Breakdown

#### 1. Infrastructure Layer (Phase 1)

| Component | What | Why |
|:----------|:-----|:----|
| **Ubuntu 22.04 LTS** (bare metal) | Host operating system | LTS provides 5-year security patches. Bare metal (not a VM) avoids nested virtualization issues with `guestmount` FUSE operations |
| **`lsof`** | Kernel-level file lock checker | Used by `wait_for_stable()` to verify the OS has fully released file handles before processing. Prevents TOCTOU race conditions where a file is still being written by `scp` or `rsync` when the daemon tries to read it |
| **UFW Firewall** | `deny incoming` + allow 22, 80, 443 | Only SSH and HTTP/S reach the server. Docker binds to `127.0.0.1:3001` (localhost only), so the AnythingLLM API is never directly exposed to the network |
| **Python 3 venv** | Isolated Python environment | All Python dependencies (`PyMuPDF`, `requests`, `tiktoken`) run inside `~/diagnostic_engine/venv/`. Bare `python3` will crash with `ModuleNotFoundError`. Every invocation uses the absolute path `$HOME/diagnostic_engine/venv/bin/python3` |
| **`fuse3` + `libguestfs-tools`** | Virtual disk image mounting | Enables mounting VMDK/OVA disk images as read-only filesystems to extract embedded PDFs without disk copying |
| **KVM group** | `sudo usermod -aG kvm $USER` | Required by `libguestfs` for kernel-level access to mount virtual disk images |

> [!IMPORTANT]
> **Docker & KVM group propagation:** After adding the user to the `docker` and `kvm` groups, you MUST log out of the SSH session completely and log back in. Linux group membership changes do not take effect until the next login. Running `docker` or `guestmount` without re-login will fail with a permissions error.

#### 2. Container Layer (Phase 2)

**AnythingLLM** is deployed as a Docker container binding to `127.0.0.1:3001` — localhost only, invisible to the network.

| Setting | Value | Why |
|:--------|:------|:----|
| Port binding | `-p 127.0.0.1:3001:3001` | Localhost-only exposure. Network access is routed through Nginx (TLS) |
| Storage volume | `-v $ENGINE_DIR/storage:/app/server/storage` | Persistent vector database, config, and chat history |
| `.env` volume | `-v $ENGINE_DIR/.env:/app/server/.env` | Passes secrets (JWT_SECRET, INTERNAL_API_KEY) from host to container |
| Extracted manuals | `-v $ENGINE_DIR/extracted_manuals:/app/server/extracted_manuals:ro` | Read-only mount of chunked PDFs for ingestion scripts |
| Log rotation | `--log-opt max-size=50m --log-opt max-file=3` | Caps container logs at 150MB total. Without this, Docker JSON logs grow unbounded and exhaust disk |
| Restart policy | `--restart always` | Auto-recovery from crashes, OOM kills, or host reboots |

**Deployment method:** A temporary container (`temp_llm`) is started first to generate AnythingLLM's default `.env` configuration. These defaults are merged with the host's `.env` (which already contains the `JWT_SECRET`), then the temp container is destroyed and the production container launched. This avoids the need to manually construct the `.env` contents.

**Critical anti-pattern:** Docker's `iptables: false` daemon option was tested in Phase 3 and proven catastrophic in Phase 5 — it kills all container-to-internet connectivity, permanently preventing API calls to Anthropic, Mistral, Voyage AI, and Cohere. The correct security posture is localhost binding + UFW, NOT iptables manipulation.

#### 3. Reverse Proxy Layer (Phase 1, Step 6)

**Nginx** provides TLS termination, WebSocket proxying, payload limits, and endpoint security.

| Feature | Implementation | Why |
|:--------|:---------------|:----|
| TLS | Self-signed cert (10-year validity), key permissions `chmod 600` | Encrypts all traffic between mechanic's browser and server. Self-signed is acceptable for a single-user shop deployment |
| WebSocket | `Upgrade $http_upgrade` / `Connection "upgrade"` / 86400s timeouts | AnythingLLM's chat interface uses WebSockets for real-time streaming. Without this, the chat would fail to connect |
| Payload limit | `client_max_body_size 50M` | Prevents disk exhaustion via massive upload payloads. Reduced from V7's 500MB to 50MB after hostile audit |
| Upload blocking | `location ~* ^/api/v1/document/(upload\|create-folder)` → 403 | Blocks file uploads from external clients. `~*` makes it case-insensitive — without this, `UpLoad` bypasses Express.js routing |
| IP anti-spoofing | `X-Forwarded-For $remote_addr` (overwrite, not append) | Prevents attackers from injecting fake IP addresses via `X-Forwarded-For` headers |
| Security headers | `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy: no-referrer`, `X-Powered-By` hidden | Standard defense-in-depth headers |

#### 4. Ingestion Pipeline (Phase 4)

The **Thermodynamic Ingestion Daemon** (`vmdk_extractor.py`) is a Python script running as a systemd service. It performs continuous automated extraction of PDFs from virtual disk images.

**Pipeline flow:** `DOWNLOAD_DIR` → file detected → 30s age check → `wait_for_stable()` → `process_file()` → chunk + watermark → `extracted_manuals/` → delete original (or quarantine on failure)

**Key functions:**

| Function | Purpose |
|:---------|:--------|
| `get_hash(filepath)` | SHA-256 hash with 1MB I/O buffer for 20GB+ files. Used for deduplication via manifest lookup |
| `validate_file_header(path)` | Magic byte validation: VMDK must start with `KDMV` or `# Di`, OVA must have `ustar` at byte 257. Rejects corrupt downloads before expensive guestmount operations |
| `wait_for_stable(path)` | Multi-stage TOCTOU-immune file lock verification (see dedicated section below) |
| `chunk_pdf(input_path, output_dir, ...)` | Splits PDFs into 5-page segments. Burns `[[ABSOLUTE_PAGE: N]]` watermarks into the text layer at position (72, 36) in gray (0.6, 0.6, 0.6). Naming convention: `{basename}_pages_{start}-{end}_{hash8}.pdf` |
| `write_manifest_atomic(manifest)` | Writes `manifest.json` using tmp file + `os.fsync` + `os.replace` atomic rename pattern. Prevents corrupt manifest from power loss mid-write |
| `load_manifest()` | Loads manifest with corrupt-backup safety: on `JSONDecodeError`, backs up the corrupt file with timestamp suffix before returning empty manifest |
| `process_file(file_path)` | Orchestrates the full pipeline for a single file: hash → dedup check → OVA tar extraction → guestmount → PDF discovery → chunk + watermark → manifest update. All operations (including `tempfile.mkdtemp`, `get_hash`, `load_manifest`, dedup check) execute inside a single `try/except` block so that any exception triggers the three-tier quarantine defense: `shutil.move` → `os.remove` → CRITICAL log. `mount_point` is initialized to `None` before the `try` and the `finally` block uses `if mount_point and os.path.ismount(mount_point)` guards for safe FUSE cleanup |

**File type handling:**
- `.vmdk` — Mounted directly via `guestmount -a file -i --ro mountpoint`
- `.ova` — Extracted via `tar -xf` to `OVA_STAGING`, then the largest `.vmdk` inside is mounted
- `.pdf` — Chunked directly (no mount needed)

**Quarantine system (V8):** Both failure paths now use an identical three-tier defense with vanished-file guards and TOCTOU safety:
- **`wait_for_stable()` failure** (file unstable for 2 hours): `os.path.exists` check → `os.makedirs` + `shutil.move` to `QUARANTINE_DIR` → if move fails, `os.remove` → if delete fails, `FileNotFoundError` suppressed (TOCTOU), else CRITICAL log
- **`process_file()` failure** (extraction exception): `os.path.exists` check → `os.makedirs` + `shutil.move` to `QUARANTINE_DIR` (both inside `try`) → if move fails, `os.remove` → if delete fails, `FileNotFoundError` suppressed (TOCTOU), else CRITICAL log

Both paths use `shutil.move` (not `os.rename`) to handle cross-device moves gracefully. Files that vanish during processing are detected at two levels: the `os.path.exists` primary guard and the `isinstance(e2, FileNotFoundError)` TOCTOU fallback.

#### 5. Stabilization System — `wait_for_stable()`

This function answers the question: *"Is this file fully written and safe to read?"*

**Algorithm (5 stages):**

1. **`lsof` kernel lock check** — Calls `lsof path`. If a process has the file open, `lsof` returns exit code 0. The daemon waits 10 seconds and retries.
2. **TOCTOU double-check** — When `lsof` first reports no locks, the daemon waits 5 seconds and checks again. If the file was re-locked during the buffer (e.g., `rsync` temporarily releases and re-acquires), it goes back to waiting.
3. **Size stability verification** — Records `os.path.getsize()`, waits 5 seconds, checks again. If the size changed, the file is still being written. Both `getsize` calls are wrapped in `try/except OSError` to handle concurrent deletion.
4. **Zero-byte detection** — If `curr_size == 0`, the file is an empty placeholder (common with network copy tools that create the file before writing data). The daemon continues waiting.
5. **Magic byte validation** — If all previous checks pass, validates VMDK/OVA magic bytes via `validate_file_header()`. Corrupt files return `False`.

**Timeout:** 2 hours (`7200` seconds). All code paths (including `except` branches and zero-byte detection) increment the `elapsed` counter to guarantee eventual timeout.

#### 6. OCR & Embedding Layer (Phases 5 & 7)

| Component | Technology | Configuration |
|:----------|:-----------|:--------------|
| **OCR Processing** | Mistral OCR (via AnythingLLM) | Processes the watermarked PDF chunks into text for embedding |
| **Embedding Model** | Voyage AI `voyage-3-large` | Generates vector embeddings from OCR'd text |
| **Reranking** | Cohere `rerank-english-v3.0` | Re-scores retrieval results for relevance accuracy |
| **Text Splitter** | Markdown Header Text Splitter | Chunk Token Size: `400` tokens — matched to the 5-page physical PDF chunk size |
| **Vector Database** | LanceDB (inside AnythingLLM container) | Stores and queries document vectors |

**Ingestion script** (`sync_ingest.py`): Queries the workspace for already-embedded documents before starting, then uploads only NEW chunked PDFs to `http://127.0.0.1:3001/api/v1/document/upload` (bypassing Nginx) and embeds each via `/workspace/{slug}/update-embeddings`. A **12-second cooldown** in a `finally` block fires unconditionally after every upload attempt (including `continue` on upload failure, empty docs, and `except` on network errors) to prevent Mistral OCR 429 (rate limit) death spirals.

**Verification script** (`verify_ingestion.py`): Compares filesystem chunk files against embedded workspace documents. Reports any missing chunks.

#### 7. Tribal Knowledge Subsystem (Phase 6)

The **MASTER_LEDGER.md** is the system's highest-authority document. It contains empirical shop notes from master technicians that override contradicting FSM procedures.

**Example entry:**
```markdown
## FAULT SIGNATURE: Hot start vapor lock.
- **OEM FSM Diagnosis:** Replace Fuel Accumulator.
- **MASTER TECH OVERRIDE:** Do not drop the tank. 90% probability is a
  hairline crack in the 0.4 ohm ballast resistor on the fender.
- **VERIFICATION TEST:** Hot-wire terminal 15 on the ignition coil directly
  to the battery positive. If it starts instantly, the resistor is dead.
```

**Gating architecture:**
- `validate_ledger.py` — Enforces a **1,500-token hard cap** with a **15% safety margin** (effective cap: **1,275 tokens**). Uses `tiktoken` pinned to `cl100k_base` encoding. Also enforces a **`MIN_RAG_BUDGET = 2000`** floor check: if the remaining token budget (4000 − system prompt − ledger) falls below the floor, the ledger is rejected even if under the hard cap.
- `sync_ledger.py` — Uploads the validated ledger to AnythingLLM via the local API (bypasses Nginx). Before uploading, queries the workspace for any existing `MASTER_LEDGER` document and injects its location into the `deletes[]` array of the `update-embeddings` call, performing an atomic swap that prevents legacy vector accumulation.
- `update_ledger.sh` — The **only approved update method**. Runs validation FIRST, then uploads. If validation fails (token cap exceeded), nothing is uploaded.
- After upload, the operator must **pin** the document in the AnythingLLM Web UI (pushpin icon) to inject it into every query's context window.

**Why the gating exists:** The ledger is pinned (permanently injected into every prompt). If it grows too large, it consumes the token budget and either pushes RAG retrieval results out of the context window or causes the LLM to truncate its response. The 1,275-token safety cap guarantees the total input (system prompt + ledger + RAG chunks) never exceeds 4,000 tokens. When the ledger exceeds the token cap, old entries can be moved to a non-pinned `MASTER_LEDGER_ARCHIVE.md` that is still uploaded and embedded in the workspace — it participates in vector search (discoverable via RAG retrieval) but does NOT consume the fixed context token budget on every query, preserving historical tribal knowledge while freeing pinned context budget.

#### 8. The AI Brain — System Prompt (Phase 8)

The system prompt defines Gus as a **deterministic state-machine DAG** with 5 possible states:

```
PHASE_A_TRIAGE ──▶ PHASE_B_FUNNEL ──▶ PHASE_C_TESTING ──▶ PHASE_D_CONCLUSION
                        │     ▲
                        └─────┘ (loop for multi-variable isolation)

RETRIEVAL_FAILURE (dead end — no documents found)
```

**State transition rules:**

| Trigger | Output State | `requires_input` |
|:--------|:-------------|:------------------|
| User provides symptom | `PHASE_A_TRIAGE` | `true` (answer buttons shown) |
| User answers PHASE_A prompt | `PHASE_B_FUNNEL` | `true` |
| User answers PHASE_B prompt | `PHASE_B_FUNNEL` (loop) OR `PHASE_C_TESTING` (advance) | `true` |
| Physical test resolves fault | `PHASE_D_CONCLUSION` | `false` (no more buttons) |
| User sends new message after PHASE_D | `PHASE_A_TRIAGE` (reset) | `true` (new diagnostic session) |
| No document chunks retrieved | `RETRIEVAL_FAILURE` | `false` |

**Citation rules (dual-layer):**
1. **Watermark-first:** If the document text contains `[[ABSOLUTE_PAGE: N]]`, cite page N directly. No arithmetic.
2. **Fallback (no watermark):**
   - Arabic numerals: `absolute = range_start + in_chunk_page - 1`
   - Roman numerals (i, ii, iii): cite as-is with chunk filename
   - Section-prefixed (e.g., "54-12", "A-3"): cite as-is with chunk filename
   - Unknown: cite `"page": "unknown"` — NEVER fabricate

**Output schema:** Raw JSON only. No markdown code fences. First character must be `{`, last must be `}`.

```json
{
  "current_state": "PHASE_B_FUNNEL",
  "intersecting_subsystems": ["Bosch K-Jetronic CIS"],
  "source_citations": [
    {"source": "1975_450SL_FSM_pages_101-105.pdf", "page": "103", "context": "K-Jetronic Hand-off"}
  ],
  "diagnostic_reasoning": "Determining if handoff failure is fuel supply.",
  "mechanic_instructions": "Have a helper start car. Observe pump.",
  "answer_path_prompts": ["[A] Cuts out INSTANTLY.", "[B] Runs 1 SECOND AFTER dies."],  // 2-5 mutually exclusive options required
  "requires_input": true
}
```

#### 9. Frontend Intelligence Layer (Phase 11)

Two JavaScript functions manage the client-side diagnostic flow:

**`parseGusResponse(rawText)`** — Extracts valid JSON from the LLM’s raw text response.

- **Single-pass brute-force `JSON.parse` iteration (V8).** Scans **forward** for every `{`, pairs with every `}` (backward inner scan), attempts `JSON.parse(substring)`. Forward outer scan guarantees the **outermost** (leftmost) JSON envelope is found first — prevents inner nested JSON strings (e.g., in `mechanic_instructions`) or trailing hallucinated JSON from being extracted over the real envelope. O(n²) worst case on ~2KB text — negligible latency.
- **Fatal:** Throws `Error("FATAL: No valid JSON object with 'current_state' found in response.")` if parsing fails.

**`buildUserMessage(selectedOption, lastResponse)`** — Constructs the structured message sent back to Gus when a mechanic clicks an answer button.

- **PHASE_A → PHASE_B:** Forces `required_next_state: "PHASE_B_FUNNEL"`
- **PHASE_B:** Sends `required_next_state: null` — lets the LLM decide whether to loop (more isolation needed) or advance to PHASE_C
- **PHASE_C → PHASE_D:** Forces `required_next_state: "PHASE_D_CONCLUSION"`
- **RETRIEVAL_FAILURE:** Not in the map. `requires_input: false` means no buttons render. Frontend must detect this state and display a "Restart Diagnostic" button.
- **PHASE_ERROR → PHASE_A:** Defensive frontend-only state (not in the system prompt DAG). Explicitly mapped in the `nextStates` table — `buildUserMessage` sends `required_next_state: "PHASE_A_TRIAGE"`, restarting the diagnostic flow.
- **Truly unrecognized states:** Any `current_state` not in the `nextStates` map hits the fallback `nextStates[currentState] || "PHASE_D_CONCLUSION"`, which concludes the diagnostic gracefully rather than crashing.

#### 9½. Agent Skills Sandbox (Phase 9)

V9 Phase 9 injects **four AnythingLLM Agent Skills** into the container's plugin directory — one diagnostic verification tool and three operational utilities:

| Skill | Purpose | API Key Required? |
|:------|:--------|:------------------|
| **@Manual-Status** | Queries workspace document count for ingestion verification | Yes (`$INTERNAL_KEY` via `sed`) |
| **@VIN-Lookup** | Decodes VINs via public NHTSA API for vehicle identification | No |
| **@Purchase-Router** | Generates vendor search links for missing FSMs | No |
| **@Draft-Tribal-Knowledge** | Formats undocumented fixes into FAULT SIGNATURE structure for `MASTER_LEDGER.md` | No |

| Component | File | Purpose |
|:----------|:-----|:--------|
| Skill manifest | `plugins/agent-skills/manual-status/plugin.json` | Registers the skill with AnythingLLM. Declares a required parameter `workspace_slug` (type: string) passed at runtime by the agent framework |
| Skill handler | `plugins/agent-skills/manual-status/handler.js` | Queries `GET /api/v1/workspace/{workspace_slug}` on `127.0.0.1:3001`. Returns document chunk count or CRITICAL alert. API key injected via `sed` replacement at deployment time |

> [!NOTE]
> `handler.js` does **not** hardcode the workspace slug. It receives `workspace_slug` as a runtime parameter from the agent framework's `plugin.json` declaration. Only the 3 Python scripts (`sync_ingest.py`, `verify_ingestion.py`, `sync_ledger.py`) require manual slug updates when changing vehicles. The 3 additional skills (@VIN-Lookup, @Purchase-Router, @Draft-Tribal-Knowledge) are defined in **Appendix A: Agent Skill Definitions** and use quoted heredocs (`cat << 'EOF'`) for simple file creation — none require `$INTERNAL_KEY`.

#### 10. Security Posture

| Control | Implementation | Threat Mitigated |
|:--------|:---------------|:-----------------|
| `.env` permissions | `chmod 600` after every write (creation, merge, key append) | JWT_SECRET and API key readable by other users |
| TLS key permissions | `chmod 600` on `/etc/nginx/ssl/diag-engine.key` | Private key accessible to non-root users |
| API key guards | `if not API_KEY: sys.exit(1)` in all 3 Python scripts | Silent `Bearer ` (empty) auth → misleading 403 errors |
| `cut -d '=' -f2-` | All shell scripts use `-f2-` instead of `-f2` | Base64 keys containing `=` are silently truncated |
| Nginx upload blocking | Case-insensitive regex (`~*`) blocks `/api/v1/document/upload` | Bypass via `UpLoad`, `UPLOAD`, etc. |
| IP anti-spoofing | `X-Forwarded-For $remote_addr` (overwrite) | Forged IP headers in `X-Forwarded-For` |
| `X-Powered-By` hidden | `proxy_hide_header X-Powered-By` | Technology fingerprinting |
| Docker localhost binding | `127.0.0.1:3001:3001` | Direct API access from network |
| ExecStopPost FUSE cleanup | `guestunmount $m` on daemon stop | Zombie FUSE mounts exhausting file descriptors |
| Triple shell escaping | `\\\\\\$m` in heredoc | `$m` consumed by 3 shell layers → empty variable |

#### 11. Systemd Service Layer (Phase 4, Step 2)

The daemon runs as `manual-ingest.service`:
- **User:** Runs as the deploying user. The systemd unit resolves the user's home directory via `$(eval echo ~$USER_NAME)`, supporting both standard (`/home/user/`) and root (`/root/`) deployments.
- **ExecStart:** `$USER_HOME/diagnostic_engine/venv/bin/python3 $USER_HOME/diagnostic_engine/vmdk_extractor.py`
- **ExecStopPost:** Cleans up orphaned FUSE mounts and OVA extractions on stop/crash. Iterates `staging/mounts/*` and calls `guestunmount $$m` on each (double-dollar is systemd's literal-dollar escape, so bash receives `$m` as the loop variable). Then `rm -rf --one-file-system` targets the parent directories `staging/mounts` and `staging/ova` (NOT `/*` globs — targeting parent dirs ensures `--one-file-system` correctly detects FUSE mount boundaries). Finally, `mkdir -p` recreates the staging directories. The `--one-file-system` flag prevents recursive FUSE traversal if `guestunmount` fails (busy mount). The OVA cleanup is critical: if `SIGKILL` terminates the daemon during a 20GB OVA extraction, Python's `finally` block is bypassed, leaking the uncompressed payload.
- **Restart:** `always` with `RestartSec=10`

#### 11½. Disaster Recovery (Phase 10)

Automated daily backup and cleanup via cron:

- **Schedule:** Daily at 2:00 AM
- **Mechanism:** Docker container stop → `tar czf` with `--exclude=diagnostic_engine/staging` → Docker container start. The container is stopped before backup to **prevent torn copies of LanceDB/SQLite databases** — an interrupted read during an active write produces a corrupt vector DB or config store. Downtime is ~2-5 minutes at 2 AM. The staging exclusion is critical: if the extraction daemon has an active FUSE mount during backup, `tar` would traverse the mounted filesystem, bloating the archive by 20GB+ and potentially exhausting disk space.
- **Retention:** 7 days — cleanup cron runs daily at 3:00 AM and removes archives older than 7 days
- **Path handling:** Uses absolute `/usr/bin/docker` path to prevent `command not found` under cron's minimal `PATH` environment. Semicolons (`;`) guarantee the container restart fires regardless of the tar exit code.

#### 12. Verification Framework (Phase 12)

A 12-step post-deployment checklist:

| # | Check | Expected Result |
|:--|:------|:----------------|
| 1 | Systemd daemon status | `Active: active (running)` |
| 2 | Docker container running | `Status: Up` |
| 3 | API key authentication | `authenticated: true` |
| 4 | Ingestion completeness | `✓ ALL CHUNKS VERIFIED` |
| 5 | Nginx upload blocking (lowercase + mixed case) | HTTP 403 for both |
| 6 | UFW firewall active | `deny (incoming), allow (outgoing)` |
| 7 | Cron jobs present | Backup + cleanup crons |
| 8 | ExecStopPost escaping | Literal `$m` (not empty) |
| 9 | `.env` permissions | `-rw-------` (600) |
| 10 | TLS key permissions | `-rw-------` (600) |
| 11 | Docker log rotation | `max-size:50m max-file:3` |
| 12 | Live diagnostic test | Gus returns `PHASE_A_TRIAGE` with `source_citations` |

---

## PART 3: THE DATA FLOW

### Flow A: "A Mechanic Drops a VMDK File Onto the Server"

```
                    ┌──────────────────────────────┐
                    │  mechanic SCP/rsync uploads   │
                    │  service_manual.vmdk to       │
                    │  ~/diagnostic_engine/downloads│
                    └──────────────┬───────────────┘
                                   │
                    ┌──────────────▼───────────────┐
                    │  DAEMON MAIN LOOP (10s cycle) │
                    │  os.listdir(DOWNLOAD_DIR)     │
                    │  File detected: .vmdk match   │
                    └──────────────┬───────────────┘
                                   │
                    ┌──────────────▼───────────────┐
                    │  30-SECOND AGE CHECK          │
                    │  time.time() - st_mtime < 30? │
                    │  YES → skip (still uploading) │
                    │  NO  → proceed                │
                    └──────────────┬───────────────┘
                                   │
                    ┌──────────────▼───────────────┐
                    │  wait_for_stable(path)        │
                    │  1. lsof lock check           │
                    │  2. TOCTOU 5s double-check    │
                    │  3. Size stability (5s gap)   │
                    │  4. Zero-byte detection        │
                    │  5. VMDK magic byte validation│
                    │  Timeout: 2 hours             │
                    │                               │
                    │  FALSE → quarantine/delete    │
                    │  TRUE  → proceed              │
                    └──────────────┬───────────────┘
                                   │
                    ┌──────────────▼───────────────┐
                    │  process_file(path)           │
                    │  1. SHA-256 hash (1MB buffer) │
                    │  2. Manifest dedup check      │
                    │     (duplicate? → delete+skip)│
                    └──────────────┬───────────────┘
                                   │
                    ┌──────────────▼───────────────┐
                    │  GUESTMOUNT                   │
                    │  guestmount -a file -i --ro   │
                    │  → staging/mounts/vmdk_mount_ │
                    │  Walk mounted filesystem      │
                    │  Find all .pdf files           │
                    └──────────────┬───────────────┘
                                   │
                    ┌──────────────▼───────────────┐
                    │  FOR EACH PDF:                │
                    │  1. SHA-256 hash              │
                    │  2. Dedup check vs manifest   │
                    │  3. chunk_pdf():              │
                    │     - Split into 5-page segs  │
                    │     - Burn [[ABSOLUTE_PAGE: N]]│
                    │       watermark on each page   │
                    │     - Save as:                 │
                    │       {name}_pages_{S}-{E}     │
                    │       _{hash8}.pdf             │
                    │     → extracted_manuals/       │
                    │  4. Update manifest (dict)     │
                    └──────────────┬───────────────┘
                                   │
                    ┌──────────────▼───────────────┐
                    │  write_manifest_atomic()      │
                    │  tmpfile → fsync → os.replace │
                    └──────────────┬───────────────┘
                                   │
                    ┌──────────────▼───────────────┐
                    │  guestunmount + cleanup tmps  │
                    │  os.remove(original VMDK)     │
                    └──────────────┬───────────────┘
                                   │
      ┌────────────────────────────▼────────────────────────────┐
      │  MANUAL STEP: Operator runs sync_ingest.py             │
      │  0. GET /workspace/{slug}/documents → existing_docs     │
      │  For each PDF in extracted_manuals/:                    │
      │    • Skip if filename in existing_docs (dedup)          │
      │    1. POST /api/v1/document/upload → 127.0.0.1:3001    │
      │    2. Mistral OCR processes PDF → text (watermarks     │
      │       [[ABSOLUTE_PAGE: N]] become part of text)        │
      │    3. POST /workspace/{slug}/update-embeddings         │
      │       → Voyage AI generates vectors → LanceDB stores  │
      │    4. 12s cooldown in `finally` (unconditional)        │
      └──────────────────────────────────────────────────────────┘
```

### Flow B: "A Mechanic Types a Diagnostic Query"

```
MECHANIC types: "Hot start vapor lock, cranks but won't catch"
         │
         ▼
┌─────────────────────────────┐
│  Browser → HTTPS → Nginx   │
│  WebSocket upgrade          │
│  proxy_pass 127.0.0.1:3001 │
└────────────┬────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────┐
│  AnythingLLM receives query                             │
│                                                         │
│  1. RETRIEVAL: Query → Voyage AI embedding              │
│     → LanceDB vector similarity search (threshold 0.50) │
│     → Top 4 chunks retrieved (max 1600 tokens)          │
│     → Cohere reranking for precision                    │
│                                                         │
│  2. CONTEXT ASSEMBLY:                                   │
│     System Prompt (~600 tokens)                         │
│     + Pinned MASTER_LEDGER.md (~1275 tokens max)        │
│     + 4 RAG chunks (4 × 400 = 1600 tokens max)         │
│     + User message                                      │
│     = ~3475 tokens total input                          │
│                                                         │
│  3. LLM CALL: Anthropic claude-3-5-sonnet-latest        │
│     Token limit: 4000 (hard cap)                        │
│     → Gus processes via DAG state machine               │
│     → Finds MASTER_LEDGER override for vapor lock       │
│     → Identifies ballast resistor fault signature       │
│     → Returns raw JSON (no markdown fences)             │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────────────────┐
│  RAW LLM OUTPUT (arrives via WebSocket):             │
│  {"current_state":"PHASE_A_TRIAGE",                  │
│   "intersecting_subsystems":["Bosch K-Jetronic CIS"],│
│   "source_citations":[                               │
│     {"source":"MASTER_LEDGER.md","page":"1",         │
│      "context":"Hot start vapor lock signature"}     │
│   ],                                                 │
│   "diagnostic_reasoning":"Hot start failure with     │
│    crank-no-catch pattern. Master Ledger overrides    │
│    FSM fuel accumulator diagnosis.",                  │
│   "mechanic_instructions":"Before any parts: Locate  │
│    the 0.4 ohm ballast resistor on the passenger     │
│    side fender. Inspect for hairline cracks.",        │
│   "answer_path_prompts":[                            │
│     "[A] Resistor shows visible crack or burn mark",  │
│     "[B] Resistor appears intact"                    │
│   ],                                                 │
│   "requires_input":true}                             │
└────────────────┬─────────────────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────────────────┐
│  FRONTEND: parseGusResponse(rawText)                 │
│  Pass 1: depth-counter → JSON.parse → valid ✓       │
│  Returns parsed JSON object                          │
│                                                      │
│  UI renders:                                         │
│  ┌────────────────────────────────────────────────┐  │
│  │ GUS: "Locate the 0.4 ohm ballast resistor     │  │
│  │  on the passenger side fender. Inspect for     │  │
│  │  hairline cracks."                             │  │
│  │                                                │  │
│  │  Source: MASTER_LEDGER.md, page 1              │  │
│  │                                                │  │
│  │  [A] Resistor shows visible crack or burn mark │  │
│  │  [B] Resistor appears intact                   │  │
│  └────────────────────────────────────────────────┘  │
└────────────────┬─────────────────────────────────────┘
                 │
    Mechanic clicks [A]
                 │
                 ▼
┌──────────────────────────────────────────────────────┐
│  FRONTEND: buildUserMessage("[A] Resistor shows      │
│    visible crack or burn mark", lastResponse)        │
│                                                      │
│  currentState = "PHASE_A_TRIAGE"                     │
│  nextStates["PHASE_A_TRIAGE"] = "PHASE_B_FUNNEL"    │
│                                                      │
│  Sends JSON message to AnythingLLM:                  │
│  {"completed_state":"PHASE_A_TRIAGE",                │
│   "required_next_state":"PHASE_B_FUNNEL",            │
│   "selected_option":"[A] Resistor shows visible      │
│     crack or burn mark",                             │
│   "instruction":"User physically verified: \"[A]     │
│     Resistor shows visible crack or burn mark\".     │
│     You MUST transition to PHASE_B_FUNNEL.           │
│     Do NOT repeat PHASE_A_TRIAGE."}                  │
└──────────────────────────────────────────────────────┘
                 │
                 ▼
         ... Gus returns PHASE_B_FUNNEL response ...
         ... Mechanic answers PHASE_B questions ...
         ... Gus may LOOP in PHASE_B or advance ...
         ... Eventually reaches PHASE_D_CONCLUSION ...
```

---

## PART 4: THE ENGINEERING DECISIONS

### 1. Why Absolute Page Watermarks Instead of LLM Arithmetic?

The V3-V5 architecture relied on the LLM to compute page numbers: `absolute_page = range_start + in_chunk_page - 1`. This arithmetic is trivial for humans but LLMs get it wrong with alarming frequency — especially when chunk filenames use complex naming conventions. Burning `[[ABSOLUTE_PAGE: 103]]` directly into the PDF text layer before OCR means the watermark becomes part of the vectorized text. The LLM simply reads the number. No arithmetic. No error. The Phase 6 DeepThink audit explicitly recommended this approach after identifying the arithmetic as a reliability risk.

### 2. Why 5-Page Physical Chunks Instead of Semantic Chunking?

Semantic chunking (splitting at topic boundaries) sounds elegant but is non-deterministic — the boundary detection varies by algorithm and content. Physical 5-page chunks produce predictable, narrow page ranges (`pages_101-105.pdf`). The 400-token chunk size in AnythingLLM's text splitter is calibrated to match these 5-page segments. This alignment prevents "Markdown Table chunk explosion" — a failure mode where a single dense table generates dozens of sub-chunks that consume the entire RAG budget. The physical chunk alignment addresses explosion at the PDF page level; the `preprocess_markdown_tables()` function in `sync_ingest.py` provides the text-level defense — splitting oversized tables at `max_rows=20` with header re-injection before upload, ensuring no single table generates more chunks than the RAG budget can absorb.

### 3. Why a Systemd Daemon Instead of a Cron Job or File Watcher?

- **Cron job** — Runs at intervals (e.g., every 5 minutes). A 20GB VMDK extraction takes 15+ minutes. Cron would launch overlapping instances, causing duplicate processing and FUSE mount conflicts.
- **`inotify` / `watchdog`** — Fires on file creation events. But `scp` and `rsync` create the file immediately (triggering the event) and then write data over seconds or minutes. Processing would start before the file is complete.
- **Systemd daemon** — Runs continuously in a single-threaded loop. The 30-second age check and `wait_for_stable()` function guarantee the file is fully written before processing. Systemd provides auto-restart, logging (`journalctl`), and `ExecStopPost` cleanup.

### 4. Why `lsof` Kernel Lock Verification Instead of `inotify`?

`inotify` tells you when a file was *modified*. `lsof` tells you whether any process *still has the file open*. These are different questions. `rsync` may finish its final write (last `inotify` event) but still hold the file descriptor open while verifying checksums. `lsof` catches this — `inotify` doesn't.

### 5. Why the DAG State Machine Allows PHASE_B Looping?

Complex diagnostics often require multiple isolation questions. A 1975 450SL hot start failure could involve the ballast resistor, the fuel accumulator, the warm control pressure regulator, or the cold start valve. Forcing a linear `A → B → C → D` progression means only one isolation question per diagnostic session. PHASE_B looping allows Gus to ask: "Check the resistor" → mechanic reports intact → Gus asks "Now check the fuel accumulator pressure" → mechanic reports low pressure → Gus advances to PHASE_C with the accumulated physical evidence. The DeepThink Phase 5 audit explicitly identified forced PHASE_B exit as a design flaw.

### 6. Why `os.rename` + `os.remove` Fallback Instead of Just Deleting?

Quarantine preserves evidence. If a file fails `wait_for_stable()`, it could be a corrupt download, a file from an unsupported format, or a partially transferred file that needs to be re-sent. Moving it to `quarantine/` lets the operator inspect it later. But if the rename itself fails (permissions, cross-device move), the file must still be removed from `DOWNLOAD_DIR` — otherwise, the daemon re-discovers it every 10 seconds and spends 2 hours on each `wait_for_stable()` attempt, permanently livelocking the entire ingestion pipeline. A deleted file is recoverable from backups; a livelocked daemon is not.

### 7. Why Brute-Force `JSON.parse` Instead of Regex for JSON Extraction?

The V2 regex fallback (`/\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}/g`) handles one level of nesting but is blind to string boundaries. If a JSON value contains `"Check the } bracket"`, the regex treats the in-string `}` as a structural brace and truncates the match. No regex can reliably parse JSON (it's a context-free grammar, not a regular language). The brute-force approach is mathematically correct: try every possible `{...}` substring until `JSON.parse` succeeds. O(n²) is acceptable because response text is typically <2KB.

### 8. Why `cl100k_base` Pinning Instead of `encoding_for_model("gpt-4")`?

`tiktoken.encoding_for_model("gpt-4")` depends on an internal model→encoding mapping table maintained by the tiktoken library. If OpenAI updates tiktoken and changes which encoding maps to "gpt-4", the validation script silently uses a different tokenizer, and the token count changes. `tiktoken.get_encoding("cl100k_base")` bypasses the lookup table and requests the encoding directly. The count is deterministic regardless of tiktoken version.

### 9. Why Localhost-Only Docker Binding + Nginx Instead of Direct Port Exposure?

Direct port exposure (`-p 3001:3001`) puts the AnythingLLM API on the public internet with zero authentication (the API key is checked by the application, not the network layer). Localhost binding (`127.0.0.1:3001:3001`) makes the API invisible to the network. Nginx provides TLS encryption, WebSocket support, security headers, upload blocking, and payload limits — all at the network boundary.

### 10. Why Triple-Escaping `$m` in ExecStopPost?

The ExecStopPost command passes through **three shell layers**:

1. **`sudo bash -c "..."`** — The user's shell interprets the outer double quotes
2. **Unquoted `<<EOF` heredoc** — The heredoc is NOT quoted (`<<EOF`, not `<<'EOF'`), so bash performs variable expansion on its contents
3. **systemd's `/bin/bash -c`** — When the service stops, systemd invokes `/bin/bash -c 'for m in ...; do guestunmount $m ...'`

Starting with `\\\\\\$m` in the source code:
- Layer 1 (`sudo bash`): `\\\\` → `\\`, `\\$` → `$` → produces `\\$m` in the heredoc content
- Layer 2 (heredoc expansion): `\\$m` → `$m` is preserved as literal (backslash escapes the `$`)
- Layer 3 (unit file): Contains literal `$m` → systemd's bash expands it as the loop variable

Single escape (`\$m`) gets consumed by layers 1+2, producing an empty variable in the unit file.

---

## PART 5: THE AUDIT HISTORY

### Evolutionary Lineage

```
V3 (initial architecture)
 └─ Phase 3 Hostile Audit → found first-order failures
     └─ V5 (fixes applied)
         └─ Phase 5 Hostile Audit (Red Team + DeepThink)
             → found kernel-level race conditions, token math errors, state machine paradoxes
             └─ Phase 6 Consolidated Architecture
                 └─ V7 Antigravity + V7 DeepThink (two independent blueprints)
                     └─ V7 Consolidated (merged — 16 divergences resolved)
                         └─ Three Phase 7 Hostile Audits:
                             │ V7_HOSTILE_ANALYSIS_CO.md (19 findings, 8 attack vectors)
                             │ V7_HOSTILE_ANALYSIS_CO_2.md (11 findings)
                             │ V7_HOSTILE_ANALYSIS_DT.md (6 findings)
                             └─ V2 (all 19 unique fixes applied)
                                 └─ Two Phase 8 Hostile Audits:
                                     │ Antigravity audit (verified 19 fixes, 4 new low-severity issues)
                                     │ DeepThink audit (3 critical claims, 2 invalid claims)
                                     └─ Cross-Examination (adjudicated disputes)
                                         └─ V8 (3 Phase 8 fixes + 1 Phase 9 fix)
                                             └─ Phase 9 Hostile Audit → 45/48 checks passed
                                                 → V8 hardened (forced-deletion fallback, changelog fix)
                                                     └─ Phase 10 Hostile Audits:
                                                         │ DNA Audit (1 fix: three-tier quarantine)
                                                         │ Opus Audit (1 fix: workspace slug correction)
                                                         │ DT Audit (1 fix: pre-try scope)
                                                         │ DT R3 Audit (5 fixes: mkdtemp, dedup, atomic swap, staging exclusion, rate limiting)
                                                         │ Opus R4 Audit (1 fix: rate limiting finally block)
                                                         │ DT R4 Audit (2 fixes: parseGusResponse forward scan, quarantine exists guard)
                                                         │ Opus R5 Audit (2 fixes: parseGusResponse Pass 1 current_state guard, validate_ledger label)
                                                         │ DT R5 Audit (4 fixes: ExecStopPost OVA cleanup, watchdog removal, process_file exists guard, os.makedirs inside try)
                                                         │ Opus R6 Audit (1 fix: stale watchdog refs in DNA)
                                                         │ DT R6 Audit (4 fixes: HOME path, --one-file-system, TOCTOU guards, main loop makedirs)
                                                         │ R7 Opus Audit (0 fixes: 🟢 GREENLIT 42/42)
                                                         │ DT R7 Audit (5 fixes: systemd $$m, glob removal, rmtree guard, shutil.move, Pass 1 removal)
                                                         └─ V8 Final (49 total fixes)
```

### Finding Classification System

| Symbol | Meaning |
|:-------|:--------|
| 💀 WILL FAIL | Guaranteed production failure. Copy-paste results in crash, data loss, or security breach |
| ⚠️ COULD FAIL | Fails under specific conditions (edge cases, timing, unusual input) |
| 🔍 AMBIGUOUS | Design choice that may or may not cause issues depending on deployment context |

### Cumulative Fix Count

| Change | Rows | 💀 | ⚠️ | 🔍 |
|:-------|:-----|:---|:---|:---|
| V7 Consolidated (blueprint merge) | 1–16 | — | — | — |
| V2 (Phase 7 hostile audit fixes) | 1–19 | 9 | 6 | 4 |
| V8 (Phase 8, 9, 10 fixes) | 20–49 | 6 | 13 | 11 |
| **Total verified fixes** | **49** | **15** | **19** | **15** |

---

## PART 6: THE TOKEN MATHEMATICS

### Context Window Budget (4,000 Token Hard Cap)

```
┌─────────────────────────────────────────────────┐
│           4,000 TOKEN CONTEXT WINDOW             │
│                                                  │
│  ┌──────────────────────────────┐  ~750 tokens  │
│  │  System Prompt (Gus DAG)     │               │
│  └──────────────────────────────┘               │
│  ┌──────────────────────────────┐  ≤1,275 tokens│
│  │  Pinned MASTER_LEDGER.md     │  (1500 × 0.85)│
│  │  (safety-adjusted cap)       │               │
│  └──────────────────────────────┘               │
│  ┌──────────────────────────────┐  ≤1,600 tokens│
│  │  RAG Retrieval Chunks        │               │
│  │  4 chunks × 400 tokens each  │               │
│  └──────────────────────────────┘               │
│  ┌──────────────────────────────┐  variable     │
│  │  User Message + Chat History  │               │
│  │  (Chat History Limit: 4)      │               │
│  └──────────────────────────────┘               │
│                                                  │
│  TOTAL INPUT:  ~3,625 tokens                     │
│  RESPONSE:     ~375 tokens remaining             │
│  Gus JSON:     ~200 tokens typical               │
│  MARGIN:       ~175 tokens safety buffer         │
└─────────────────────────────────────────────────┘
```

### Safety Margin Calculations

**Ledger cap derivation:**
- Raw cap: **1,500 tokens** (pinned document)
- Safety factor: **0.85** (15% reduction)
- Effective cap: **1,500 × 0.85 = 1,275 tokens**
- Reason: Anthropic's tokenizer (used by Claude) and OpenAI's `cl100k_base` tokenizer (used by `tiktoken` for validation) produce different token counts for the same text. The 15% margin guarantees the ledger fits regardless of which tokenizer is more aggressive.

**RAG budget derivation:**
- 4 context snippets × 400 tokens per chunk = **1,600 tokens maximum**
- Similarity threshold: **0.50** — chunks below this score are excluded, reducing actual RAG consumption
- Reranking: Cohere `rerank-english-v3.0` re-orders results by relevance, ensuring the 4 selected chunks are the most pertinent

**Overflow proof:**
```
750 (system prompt) + 1,275 (ledger cap) + 1,600 (RAG max) = 3,625
4,000 - 3,625 = 375 tokens remaining for response
Gus JSON output ≈ 200 tokens → 175 token safety buffer ✓
```

**Operational warning — ledger growth vs. context snippets:** As the `MASTER_LEDGER.md` grows toward its 1,275-token safety cap, the margin between total input and the 4,000-token hard cap tightens. The `validate_ledger.py` script enforces an automated **`MIN_RAG_BUDGET = 2000`** floor check that rejects ledger updates when the remaining budget is dangerously low. Additionally, if the operator accumulates enough tribal knowledge entries to consistently approach the cap, `Max Context Snippets` should be reduced from **4 to 3** (dropping RAG consumption from 1,600 to 1,200 tokens) to preserve the response buffer. Old entries can be archived to `MASTER_LEDGER_ARCHIVE.md` (non-pinned, vector-searchable) to free pinned context budget while preserving historical knowledge.

---

## PART 7: KNOWN BOUNDARIES & DEPLOYMENT GAPS

### What the System Does NOT Do

| Gap | Status | Impact |
|:----|:-------|:-------|
| **No custom frontend** | The architecture provides `parseGusResponse()` and `buildUserMessage()` as JavaScript functions but does NOT include a deployable HTML/CSS/JS application | A frontend developer must build the UI that calls these functions, renders Gus's responses, and displays answer buttons |
| **No multi-vehicle support** | Workspace slug is hardcoded to `1975-mercedes-benz-450sl` in all scripts | To support multiple vehicles, the operator must create additional workspaces and duplicate scripts with different slugs |
| **No user authentication** | AnythingLLM's Web UI has its own auth, but there's no multi-user access control | Anyone who can reach the server's HTTPS port can interact with Gus |
| **No automated ledger updates** | The tribal knowledge update flow requires manual: edit file → run `update_ledger.sh` → re-pin in Web UI | No API-driven or CI/CD-triggered ledger management |
| **No monitoring or alerting** | Daemon failures are logged to `journalctl` but there are no Slack/email/PagerDuty alerts | Operator must manually check `systemctl status` and `docker logs` |
| **No PDF upload via browser** | Nginx blocks `/api/v1/document/upload` from external clients | All document ingestion must run on the host via `sync_ingest.py` over localhost |

### External Service Dependencies

| Service | Used For | What Happens If Down |
|:--------|:---------|:---------------------|
| **Anthropic** (Claude 3.5 Sonnet) | LLM inference — generates Gus's diagnostic responses | Gus cannot respond. Queries fail with an API error |
| **Voyage AI** (`voyage-3-large`) | Vector embedding for RAG retrieval | New document embedding fails. Existing vectors still queryable from LanceDB |
| **Mistral OCR** | PDF text extraction during ingestion | `sync_ingest.py` fails with 429 or 500 errors. Documents cannot be ingested |
| **Cohere** (`rerank-english-v3.0`) | Result reranking for retrieval precision | RAG results returned without reranking — lower precision but not a hard failure |

### Hardcoded vs Configurable

| Setting | Value | Location | Changeable? |
|:--------|:------|:---------|:------------|
| Workspace slug | `1975-mercedes-benz-450sl` | `sync_ingest.py`, `verify_ingestion.py`, `sync_ledger.py` | Yes — must change in ALL 3 files (`handler.js` receives the slug as a runtime parameter, no change needed) |
| Token limit | `4000` | AnythingLLM Web UI (Phase 7) | Yes — via UI, but budget math must be recalculated |
| Chunk size | `5` pages | `vmdk_extractor.py` `chunk_pdf()` | Yes — but must re-calibrate `Chunk Token Size` in AnythingLLM to match |
| Ledger token cap | `1500` (raw), `1275` (adjusted) | `validate_ledger.py` | Yes — but must re-verify token budget proof |
| Mistral cooldown | `12` seconds | `sync_ingest.py` | Yes — lower values risk 429 errors |
| Max context snippets | `4` | AnythingLLM Web UI (Phase 7) | Yes — but RAG budget changes (N × 400 tokens) |
| Similarity threshold | `0.50` | AnythingLLM Web UI (Phase 7) | Yes — lower = more results (but noisier), higher = fewer (but more precise) |
| Chat history limit | `4` | AnythingLLM Web UI (Phase 7) | Yes — higher = more context but consumes token budget |
| Accuracy optimized (reranking) | `ON` | AnythingLLM Web UI (Phase 7) | Yes — enables Cohere reranking for retrieval precision |
| Backup retention | `7` days | Cron job (Phase 10) | Yes — change `-mtime +7` to desired days |
| TLS cert validity | `3650` days (10 years) | Phase 1 `openssl req` | Fixed at generation time |

### Who Is Required to Deploy and Operate This System

This is not an "install and forget" consumer application. It is an industrial-grade engineering specification for critical diagnostic infrastructure that requires:

- **A systems administrator** (or technically competent operator) to deploy the Ubuntu server, execute the 12-phase blueprint, manage systemd services, and perform ongoing maintenance (backup verification, daemon health checks, API key rotation)
- **A frontend developer** to build the HTML/CSS/JS application that consumes `parseGusResponse()` and `buildUserMessage()`, renders Gus's diagnostic output, and handles the `RETRIEVAL_FAILURE` dead-end state
- **A domain expert** (the master technician) to author and maintain the `MASTER_LEDGER.md` tribal knowledge entries — the system's highest-authority data source

Once deployed, the system operates autonomously: the daemon watches for new files, the ingestion pipeline processes them, and Gus responds to queries. But the three roles above are required to stand it up and keep it honest.

---

*This document was produced by forensic extraction from `ARCHITECTURE_FINAL_V9.md`, which extends V8 with 16 gap analysis recovery items (6 RESTORE, 5 RE-IMPLEMENT, 5 DOCUMENT). Cross-referenced against NotebookLM synthesis of the full 18-source audit corpus. The V9 document is the product of 10 phases of independent hostile adversarial auditing with 49 verified findings resolved across 4 document versions, plus a V3/VFINAL→V8 exhaustive gap analysis that identified and recovered silently dropped features.*
