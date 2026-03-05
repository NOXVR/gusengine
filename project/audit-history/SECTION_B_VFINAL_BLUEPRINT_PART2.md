# SECTION B: VFINAL MASTER ARCHITECTURAL BLUEPRINT (Part 2)

*(Continued from Part 1: Phases 1–5)*

---

## PHASE 6: THE "GUS" PROVENANCE ENGINE (SYSTEM PROMPT)

**Goal:** Force the AI into a strict JSON state-machine with exact citations and answer-path caging. This prompt incorporates ALL fixes from Phases 1–4 audits.

Go to **Workspace Settings → Chat Settings** AND **Workspace Settings → Agent Configuration**. Paste this EXACT text into **BOTH** System Prompt boxes:

```text
PRIME DIRECTIVE: YOU ARE "GUS", A DETERMINISTIC STATE-MACHINE DAG. YOU ARE A TIER-1 MASTER MECHANIC.
YOU DO NOT CONVERSE FREELY. YOU DO NOT TRUST THE USER'S ASSUMPTIONS. YOU ONLY OUTPUT STRICT JSON MATCHING THE SCHEMA BELOW.

EPISTEMOLOGICAL OVERRIDE (HIERARCHY OF TRUTH):
1. Every hypothesis and test MUST be derived strictly from the embedded documents in your context.
2. You MUST cite the exact Document Name and Page Number in the "source_citations" array for every technical claim.
3. If the document name contains a page range (e.g., "FSM_Vol1_pages_101-150.pdf"), compute the ABSOLUTE page number by adding the chunk's start page to the in-chunk page. Example: if the chunk is "pages_101-150.pdf" and the relevant content is on chunk page 12, cite page 112.
4. If Pinned "MASTER_LEDGER.md" (Tribal Knowledge) contradicts the FSM, the Tribal Knowledge is the ABSOLUTE TRUTH. Prioritize it and cite it.

THE DIAGNOSTIC FUNNEL (ANSWER-PATH PROMPTING):
You must never jump to a conclusion. Lead the user from vague symptom to specific test via multiple-choice triage. You do not ask open-ended questions. YOU MUST PROVIDE THE ANSWERS.

DAG STATE TRANSITION MATRIX (ABSOLUTE LAW — NEVER REGRESS):
- If the user provides a raw symptom → Output "current_state": "PHASE_A_TRIAGE".
- If the user answers a PHASE_A prompt → You MUST advance to "current_state": "PHASE_B_FUNNEL".
- If the user answers a PHASE_B prompt → YOU ARE FORBIDDEN FROM REPEATING PHASE_B. You MUST transition to "current_state": "PHASE_C_TESTING".
- If the physical test resolves the issue → You MUST transition to "current_state": "PHASE_D_CONCLUSION".

STATE TRANSITION RULES:
- In PHASE_A, PHASE_B, and PHASE_C: "requires_input" MUST be true. "answer_path_prompts" MUST contain 2-5 mutually exclusive options.
- In PHASE_D: "requires_input" MUST be false. "answer_path_prompts" MUST be an empty array []. The diagnostic is complete.
- After PHASE_D, if the user sends any new message, RESET to PHASE_A for the new symptom.

STATE TRANSITION ENFORCEMENT:
When you receive a message containing "completed_state" and "required_next_state", you MUST:
1. Set "current_state" to the value of "required_next_state".
2. NEVER repeat the "completed_state" phase.
3. If you cannot advance due to insufficient data, set "current_state" to "PHASE_ERROR" with an explanation.

ZERO-RETRIEVAL SAFEGUARD:
If your context contains NO embedded document chunks (only this system prompt and any pinned files), you MUST output:
{
  "current_state": "RETRIEVAL_FAILURE",
  "intersecting_subsystems": [],
  "source_citations": [],
  "diagnostic_reasoning": "No relevant Factory Service Manual data was retrieved for this query. Diagnostic reasoning is unsafe.",
  "mechanic_instructions": "STOP. Do not proceed. The required documentation is not available. Contact the shop manager to verify that the correct FSM has been uploaded for this vehicle.",
  "answer_path_prompts": [],
  "requires_input": false
}
Do NOT fabricate citations. Do NOT guess procedures. Do NOT use training data.

REQUIRED JSON OUTPUT SCHEMA:
{
  "current_state": "PHASE_B_FUNNEL",
  "intersecting_subsystems": ["Bosch K-Jetronic CIS", "Ignition Ballast Circuit"],
  "source_citations": [
    {"source": "1975_450SL_FSM_Vol1_pages_101-150.pdf", "page": "142", "context": "K-Jetronic Hand-off Protocol"},
    {"source": "MASTER_LEDGER.md", "page": "1", "context": "Hot Start Resistor Override"}
  ],
  "diagnostic_reasoning": "Determining if handoff failure is fuel supply or electrical Run-circuit.",
  "mechanic_instructions": "Listen for the fuel pump. Have a helper start the car. Stand at the rear. When the engine dies, observe the pump sound.",
  "answer_path_prompts": [
    "[A] The fuel pump cuts out INSTANTLY with the engine.",
    "[B] The fuel pump runs for 1 SECOND AFTER the engine dies.",
    "[C] I cannot hear the fuel pump run at all."
  ],
  "requires_input": true
}

CRITICAL OUTPUT RULE: Output raw JSON only. Do NOT wrap in markdown code fences. Do NOT prepend ```json. Do NOT append ```. The first character of your response MUST be { and the last character MUST be }.
```

---

## PHASE 7: AUTOMOTIVE AGENT SKILLS (JAVASCRIPT)

**Goal:** Provide the AI with safe tools. The `@Manual-Status` skill uses a hardcoded API key because AnythingLLM's sandbox strips `process.env`.

### Skill 1: @VIN-Lookup

```bash
cat << 'EOF' > ~/diagnostic_engine/plugins/agent-skills/vin-lookup/plugin.json
{
  "name": "VIN-Lookup",
  "hubId": "vin-lookup",
  "version": "1.0.0",
  "active": true,
  "description": "Decodes VINs or Chassis Codes",
  "entrypoint": { "file": "handler.js", "params": { "vin": { "description": "17-digit VIN or legacy chassis code", "type": "string", "required": true } } }
}
EOF
cat << 'EOF' > ~/diagnostic_engine/plugins/agent-skills/vin-lookup/handler.js
module.exports.runtime = {
  handler: async function ({ vin }) {
    if (!vin || vin.length < 5) return "Error: Invalid VIN.";
    if (vin.length < 17) return `CLASSIC CHASSIS IDENTIFIED: ${vin}. Bypassing NHTSA API. Lock workspace manually.`;
    try {
      const response = await fetch(`https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/${vin}?format=json`);
      const data = await response.json();
      const res = data.Results[0];
      if (res.ErrorCode !== "0" && res.ErrorCode !== "") return `API Error: ${res.ErrorText}`;
      return `VEHICLE: ${res.ModelYear} ${res.Make} ${res.Model}. ENGINE: ${res.DisplacementL}L. METADATA LOCK ENFORCED.`;
    } catch (e) { return `ERROR: ${e.message}`; }
  }
};
EOF
```

### Skill 2: @Manual-Status (Hardcoded API Key)

> [!WARNING]
> This uses an **unquoted** `EOF` so bash expands `$INTERNAL_KEY` at write-time. The API key is baked into the file because `process.env` is unavailable in AnythingLLM's agent skill sandbox.

```bash
export INTERNAL_KEY=$(grep INTERNAL_API_KEY $ENGINE_DIR/.env | tail -1 | cut -d '=' -f2)

cat << 'PLUGINJSON' > ~/diagnostic_engine/plugins/agent-skills/manual-status/plugin.json
{
  "name": "Manual-Status",
  "hubId": "manual-status",
  "version": "1.0.0",
  "active": true,
  "description": "Verify FSM index status in database",
  "entrypoint": { "file": "handler.js", "params": { "workspace_slug": { "description": "Workspace identifier", "type": "string", "required": true } } }
}
PLUGINJSON

cat << EOF > ~/diagnostic_engine/plugins/agent-skills/manual-status/handler.js
module.exports.runtime = {
  handler: async function ({ workspace_slug }) {
    try {
      const response = await fetch(\`http://localhost:3001/api/v1/workspace/\${workspace_slug}\`, {
        headers: { "Authorization": "Bearer $INTERNAL_KEY" }
      });
      const data = await response.json();
      if (data.workspace && data.workspace.documents.length > 0)
        return \`SUCCESS: \${data.workspace.documents.length} document chunks verified.\`;
      return \`CRITICAL: No documentation found for \${workspace_slug}. ABORT DIAGNOSTICS.\`;
    } catch (e) { return \`ERROR: \${e.message}\`; }
  }
};
EOF
```

### Skill 3: @Purchase-Router

```bash
cat << 'EOF' > ~/diagnostic_engine/plugins/agent-skills/purchase-router/plugin.json
{
  "name": "Purchase-Router",
  "hubId": "purchase-router",
  "version": "1.0.0",
  "active": true,
  "description": "Acquire missing FSMs",
  "entrypoint": { "file": "handler.js", "params": { "vehicle_data": { "description": "Year make model", "type": "string", "required": true } } }
}
EOF
cat << 'EOF' > ~/diagnostic_engine/plugins/agent-skills/purchase-router/handler.js
module.exports.runtime = {
  handler: async function ({ vehicle_data }) {
    const query = encodeURIComponent(`${vehicle_data} factory service manual OEM PDF`);
    return `DOCUMENTATION MISSING. Secure OEM files here:\n- Factory-Manuals: https://factory-manuals.com/search?q=${query}\n- eManualOnline: https://www.emanualonline.com/search.html?q=${query}`;
  }
};
EOF
```

### Skill 4: @Draft-Tribal-Knowledge

```bash
cat << 'EOF' > ~/diagnostic_engine/plugins/agent-skills/draft-tribal-knowledge/plugin.json
{
  "name": "Draft-Tribal-Knowledge",
  "hubId": "draft-tribal-knowledge",
  "version": "1.0.0",
  "active": true,
  "description": "Drafts undocumented fix for Manager approval",
  "entrypoint": { "file": "handler.js", "params": { "symptom": { "description": "Exact vehicle symptom.", "type": "string", "required": true }, "fix": { "description": "The undocumented fix.", "type": "string", "required": true } } }
}
EOF
cat << 'EOF' > ~/diagnostic_engine/plugins/agent-skills/draft-tribal-knowledge/handler.js
module.exports.runtime = {
  handler: async function ({ symptom, fix }) {
    return `### TRIBAL KNOWLEDGE DRAFT ###\n\n**SHOP MANAGER ACTION REQUIRED:**\nReview the following fix. Copy into pinned MASTER_LEDGER.md:\n\n## FAULT SIGNATURE: ${symptom}\n- **MASTER TECH OVERRIDE:** ${fix}\n\n*STATUS: Pending QA Review.*`;
  }
};
EOF
```

### Final Activation

```bash
docker restart diagnostic_rag_engine
```

Go to AnythingLLM **Settings → Agent Skills** and toggle all four skills to **ON**.

---

## PHASE 8: DISASTER RECOVERY (CRON)

**Goal:** Nightly backups without corrupting live databases.

> [!IMPORTANT]
> The container is stopped before backup to prevent torn copies of LanceDB/SQLite. Downtime is ~2-5 minutes at 2 AM.

```bash
(crontab -l 2>/dev/null; echo "0 2 * * * docker stop diagnostic_rag_engine && tar czf \$HOME/diagnostic_engine_backup_\$(date +\%Y\%m\%d).tar.gz -C \$HOME diagnostic_engine/ && docker start diagnostic_rag_engine") | crontab -
(crontab -l 2>/dev/null; echo "0 3 * * * find \$HOME/ -name 'diagnostic_engine_backup_*.tar.gz' -mtime +7 -exec rm {} \;") | crontab -
```

---

## PHASE 9: THE FRONTEND CAGE (REFERENCE IMPLEMENTATION)

**Goal:** Your web developer receives a concrete, working reference — not vague bullets.

The following JavaScript module parses Gus's JSON output, sanitizes markdown fencing, renders answer-path buttons, disables free text, and injects state transitions:

```javascript
// gus-frontend.js — Reference Implementation for Custom Shop Dashboard

/**
 * Parse LLM output with Claude markdown-fence sanitization.
 * Handles: ```json fences, conversational preamble, raw JSON.
 */
function parseGusResponse(raw) {
  let cleaned = raw.trim();
  // Strip markdown code fences
  cleaned = cleaned.replace(/^```(?:json)?\s*\n?/i, '');
  cleaned = cleaned.replace(/\n?\s*```\s*$/i, '');
  cleaned = cleaned.trim();

  try {
    return JSON.parse(cleaned);
  } catch (e) {
    // Extract JSON object from surrounding conversational text
    const match = cleaned.match(/\{[\s\S]*\}/);
    if (match) {
      try {
        return JSON.parse(match[0]);
      } catch (e2) { /* fall through */ }
    }
    throw new Error(`FATAL: LLM output is not valid JSON. Raw: ${raw.substring(0, 200)}`);
  }
}

/**
 * Build the user message that enforces state transitions.
 * This is sent TO the LLM when the mechanic clicks a button.
 */
function buildUserMessage(selectedOption, lastGusResponse) {
  const transitions = {
    "PHASE_A_TRIAGE": "PHASE_B_FUNNEL",
    "PHASE_B_FUNNEL": "PHASE_C_TESTING",
    "PHASE_C_TESTING": "PHASE_D_CONCLUSION"
  };
  const nextState = transitions[lastGusResponse.current_state] || "PHASE_D_CONCLUSION";

  return JSON.stringify({
    type: "ANSWER_PATH_SELECTION",
    completed_state: lastGusResponse.current_state,
    required_next_state: nextState,
    selected_option: selectedOption,
    instruction: `The mechanic completed ${lastGusResponse.current_state} by selecting: "${selectedOption}". You MUST now transition to ${nextState}. Do NOT repeat ${lastGusResponse.current_state}.`
  });
}

/**
 * Render the Gus response into the shop dashboard UI.
 * - Displays mechanic_instructions as readable text
 * - Renders source_citations as clickable verification bubbles
 * - Generates answer_path_prompts as large tap buttons
 * - Disables text input when requires_input is true (button mode)
 * - Re-enables text input when requires_input is false (PHASE_D complete)
 */
function renderGusResponse(gus, containerEl, textInputEl) {
  containerEl.innerHTML = '';

  // Handle error/retrieval failure states
  if (gus.current_state === "RETRIEVAL_FAILURE" || gus.current_state === "PHASE_ERROR") {
    containerEl.innerHTML = `<div class="gus-error"><h2>⚠️ ${gus.current_state}</h2><p>${gus.mechanic_instructions}</p></div>`;
    textInputEl.disabled = false;
    return;
  }

  // State badge
  const stateBadge = document.createElement('div');
  stateBadge.className = 'gus-state-badge';
  stateBadge.textContent = gus.current_state;
  containerEl.appendChild(stateBadge);

  // Mechanic instructions
  const instructions = document.createElement('div');
  instructions.className = 'gus-instructions';
  instructions.innerHTML = `<h3>Instructions:</h3><p>${gus.mechanic_instructions}</p>`;
  containerEl.appendChild(instructions);

  // Source citations (NotebookLM-style bubbles)
  if (gus.source_citations && gus.source_citations.length > 0) {
    const citationsDiv = document.createElement('div');
    citationsDiv.className = 'gus-citations';
    citationsDiv.innerHTML = '<h4>Sources:</h4>';
    gus.source_citations.forEach(cite => {
      const bubble = document.createElement('span');
      bubble.className = 'gus-citation-bubble';
      bubble.textContent = `${cite.source} p.${cite.page}`;
      bubble.title = cite.context;
      citationsDiv.appendChild(bubble);
    });
    containerEl.appendChild(citationsDiv);
  }

  // Answer-path buttons OR completion state
  if (gus.requires_input && gus.answer_path_prompts && gus.answer_path_prompts.length > 0) {
    textInputEl.disabled = true;
    textInputEl.placeholder = "Select an option above — text input disabled during diagnostics.";

    const buttonsDiv = document.createElement('div');
    buttonsDiv.className = 'gus-buttons';
    gus.answer_path_prompts.forEach(option => {
      const btn = document.createElement('button');
      btn.className = 'gus-answer-btn';
      btn.textContent = option;
      btn.onclick = () => {
        const msg = buildUserMessage(option, gus);
        // Send 'msg' to AnythingLLM chat API
        sendToAnythingLLM(msg);
      };
      buttonsDiv.appendChild(btn);
    });
    containerEl.appendChild(buttonsDiv);
  } else {
    // Diagnostic complete — re-enable text input
    textInputEl.disabled = false;
    textInputEl.placeholder = "Diagnostic complete. Type a new symptom to start again.";
    const complete = document.createElement('div');
    complete.className = 'gus-complete';
    complete.innerHTML = '<h3>✅ DIAGNOSTIC COMPLETE</h3>';
    containerEl.appendChild(complete);
  }
}

/**
 * Send message to AnythingLLM workspace chat API.
 * Replace WORKSPACE_SLUG and API_KEY with your values.
 */
async function sendToAnythingLLM(message) {
  const WORKSPACE_SLUG = "1975-mercedes-benz-450sl";
  const API_KEY = "YOUR_INTERNAL_API_KEY";

  const resp = await fetch(`https://YOUR_SERVER_IP/api/v1/workspace/${WORKSPACE_SLUG}/chat`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ message, mode: "chat" })
  });
  const data = await resp.json();
  const gus = parseGusResponse(data.textResponse);
  renderGusResponse(
    gus,
    document.getElementById('gus-container'),
    document.getElementById('symptom-input')
  );
}
```

---

## PHASE 10: OPERATIONAL UTILITIES

### 10A: Sequential Ingestion Script (Prevents Mistral 429)

```bash
cat > $ENGINE_DIR/sync_ingest.py << 'INGEST_EOF'
import requests, time, os, glob, re

API_URL = "http://127.0.0.1:3001/api/v1"
API_KEY = os.popen("grep INTERNAL_API_KEY ~/diagnostic_engine/.env | tail -1 | cut -d '=' -f2").read().strip()
HEADERS = {"Authorization": f"Bearer {API_KEY}"}
WORKSPACE_SLUG = "1975-mercedes-benz-450sl"  # CHANGE PER VEHICLE
CHUNKS_DIR = os.path.expanduser("~/diagnostic_engine/extracted_manuals")
RATE_LIMIT_DELAY = 12  # seconds between uploads

def preprocess_markdown_tables(md_content, max_rows=20):
    """Split oversized tables, prepending header rows to each sub-table."""
    lines = md_content.split('\n')
    output = []
    i = 0
    part = 0
    while i < len(lines):
        if '|' in lines[i] and i + 1 < len(lines) and re.match(r'\|[\s\-:]+\|', lines[i + 1]):
            header_row = lines[i]
            separator = lines[i + 1]
            data_rows = []
            i += 2
            while i < len(lines) and '|' in lines[i] and lines[i].strip().startswith('|'):
                data_rows.append(lines[i])
                i += 1
            if len(data_rows) <= max_rows:
                output.extend([header_row, separator] + data_rows)
            else:
                for j in range(0, len(data_rows), max_rows):
                    part += 1
                    output.append(f"### Table Continuation (Part {part})")
                    output.extend([header_row, separator] + data_rows[j:j+max_rows] + [""])
        else:
            output.append(lines[i])
            i += 1
    return '\n'.join(output)

results = {"success": [], "failed": []}

for chunk_path in sorted(glob.glob(os.path.join(CHUNKS_DIR, "*.pdf"))):
    filename = os.path.basename(chunk_path)
    print(f"Uploading: {filename}")

    with open(chunk_path, 'rb') as f:
        resp = requests.post(
            f"{API_URL}/document/upload",
            headers=HEADERS,
            files={"file": (filename, f, "application/pdf")}
        )

    if resp.status_code != 200:
        print(f"  UPLOAD FAILED: {resp.status_code}")
        results["failed"].append(filename)
        continue

    doc_location = resp.json().get("documents", [{}])[0].get("location", "")
    embed_resp = requests.post(
        f"{API_URL}/workspace/{WORKSPACE_SLUG}/update-embeddings",
        headers={**HEADERS, "Content-Type": "application/json"},
        json={"adds": [doc_location], "deletes": []}
    )

    if embed_resp.status_code == 200:
        print(f"  EMBEDDED: {filename}")
        results["success"].append(filename)
    else:
        print(f"  EMBED FAILED: {embed_resp.status_code}")
        results["failed"].append(filename)

    time.sleep(RATE_LIMIT_DELAY)

print(f"\n=== INGESTION REPORT ===")
print(f"Success: {len(results['success'])}")
print(f"Failed:  {len(results['failed'])}")
for f in results["failed"]:
    print(f"  MISSING: {f}")
INGEST_EOF
```

### 10B: Post-Ingestion Verification Script

```bash
cat > $ENGINE_DIR/verify_ingestion.py << 'VERIFY_EOF'
import requests, os, glob

API_URL = "http://127.0.0.1:3001/api/v1"
API_KEY = os.popen("grep INTERNAL_API_KEY ~/diagnostic_engine/.env | tail -1 | cut -d '=' -f2").read().strip()
HEADERS = {"Authorization": f"Bearer {API_KEY}"}
WORKSPACE_SLUG = "1975-mercedes-benz-450sl"

# Count expected chunks on disk
chunks_dir = os.path.expanduser("~/diagnostic_engine/extracted_manuals")
expected = set(f for f in os.listdir(chunks_dir) if f.endswith('.pdf'))

# Count embedded documents in workspace
resp = requests.get(f"{API_URL}/workspace/{WORKSPACE_SLUG}", headers=HEADERS)
if resp.status_code == 200:
    docs = resp.json().get("workspace", {}).get("documents", [])
    embedded_names = set(d.get("name", "") for d in docs)
    print(f"Expected chunks on disk: {len(expected)}")
    print(f"Embedded in workspace:   {len(embedded_names)}")
    missing = expected - embedded_names
    if missing:
        print(f"\nMISSING CHUNKS ({len(missing)}):")
        for m in sorted(missing):
            print(f"  ✗ {m}")
    else:
        print("\n✓ ALL CHUNKS VERIFIED. Full FSM coverage confirmed.")
else:
    print(f"API error: {resp.status_code}")
VERIFY_EOF
```

### 10C: Ledger Token Budget Validator

```bash
cat > $ENGINE_DIR/validate_ledger.py << 'LEDGER_EOF'
import tiktoken, sys

MAX_LEDGER_TOKENS = 1500
SYSTEM_PROMPT_TOKENS = 500
LLM_LIMIT = 4000
MIN_RAG_BUDGET = 2000

def validate(ledger_path):
    enc = tiktoken.encoding_for_model("gpt-4")  # Close approximation for Claude tokenization
    with open(ledger_path, 'r') as f:
        content = f.read()
    count = len(enc.encode(content))
    rag_budget = LLM_LIMIT - SYSTEM_PROMPT_TOKENS - count

    print(f"Ledger tokens:  {count} / {MAX_LEDGER_TOKENS}")
    print(f"RAG budget:     {rag_budget} tokens (minimum: {MIN_RAG_BUDGET})")

    if count > MAX_LEDGER_TOKENS:
        print(f"\nREJECTED: Ledger exceeds cap by {count - MAX_LEDGER_TOKENS} tokens.")
        print("ACTION: Archive oldest entries to non-pinned MASTER_LEDGER_ARCHIVE.md.")
        return False
    if rag_budget < MIN_RAG_BUDGET:
        print(f"\nWARNING: RAG budget dangerously low ({rag_budget} tokens).")
        return False
    print("\nAPPROVED: Ledger within budget.")
    return True

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "MASTER_LEDGER.md"
    validate(path)
LEDGER_EOF
```

Run with: `$ENGINE_DIR/venv/bin/python3 $ENGINE_DIR/validate_ledger.py /path/to/MASTER_LEDGER.md`

---

## DEPLOYMENT COMPLETE — OPERATIONAL CHECKLIST

| # | Action | Command/Location |
|:--|:-------|:-----------------|
| 1 | Verify Nginx | `curl -I http://YOUR_SERVER_IP` (should 301 → HTTPS) |
| 2 | Verify WebSocket | Browser → `https://YOUR_SERVER_IP`, open DevTools Network → WS tab |
| 3 | Verify Docker | `docker ps` → `diagnostic_rag_engine` running |
| 4 | Verify Daemon | `sudo systemctl status manual-ingest.service` → active |
| 5 | Upload FSM chunks | `$ENGINE_DIR/venv/bin/python3 $ENGINE_DIR/sync_ingest.py` |
| 6 | Verify ingestion | `$ENGINE_DIR/venv/bin/python3 $ENGINE_DIR/verify_ingestion.py` |
| 7 | Verify backups | `crontab -l` → two entries visible |
| 8 | Test Gus | Send: "My 1975 450SL cranks but won't start when hot" |
| 9 | Validate JSON | Response starts with `{`, ends with `}`, contains `current_state` |
| 10 | Verify citations | `source_citations` array is non-empty with real filenames |

> [!IMPORTANT]
> **SYSTEM IS NOW LOCKED, DETERMINISTIC, AND DEPLOYED WITH ALL 60+ AUDIT FIXES FROM PHASES 1–4.**
