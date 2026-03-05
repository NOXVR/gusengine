# GusEngine — Aerospace-Grade Hostile Audit Workspace

This workspace is the **master auditor and validator** for the Gus Diagnostic RAG Engine.

It contains the complete knowledge base required to perform zero-tolerance hostile analysis of every component in the architecture — from the systemd daemon to the AnythingLLM agent skills to the nginx reverse proxy.

## Structure

```
GusEngine/
├── .agent/
│   ├── rules.md              # Supreme mandate — aerospace-grade engineering standards
│   └── workflows/
│       └── hostile-audit.md   # Step-by-step hostile audit execution workflow
├── docs/                      # 245 files of complete official documentation (17.9 MB)
│   ├── anthropic/             # Claude API — messages, models, rate limits, streaming
│   ├── anythingllm/           # Agent skills, API endpoints (source), Docker, config
│   ├── bash/                  # Bash + GNU coreutils, sed, grep, gawk, flock, tar
│   ├── certbot/               # Let's Encrypt — TLS certificate provisioning
│   ├── cohere/                # Rerank API, models, rate limits
│   ├── cron/                  # crontab syntax, cron daemon, scheduling
│   ├── docker/                # Run, build, Dockerfile, compose, volumes, networking, security
│   ├── javascript/            # Node.js core — fs, http, crypto, events, streams, etc.
│   ├── lancedb/               # Vector DB — tables, indexing, search, storage, Python API
│   ├── libguestfs/            # guestmount/guestunmount, FUSE, libguestfs API, security
│   ├── mistral/               # Document AI — OCR processor, annotations, QnA, cookbook
│   ├── nginx/                 # TLS, proxy_pass, WebSocket, location blocks, upstream
│   ├── nhtsa/                 # VPIC VIN Decode API + field reference
│   ├── pymupdf/               # fitz — Document, Page, TextPage, Table, recipes
│   ├── python/                # 48 stdlib modules (os, sys, json, re, venv, etc.)
│   ├── python-requests/       # requests library — HTTP client for API calls
│   ├── ssh/                   # OpenSSH — ssh, scp, ssh_config, sshd_config, ssh-keygen
│   ├── systemd/               # service, unit, exec, timer, kill, systemctl, journalctl
│   ├── tiktoken/              # cl100k_base encoding, token counting cookbook
│   ├── ufw/                   # Uncomplicated Firewall — rule syntax
│   └── voyage-ai/             # Embedding model (voyage-3) + reranker specs
├── project/                   # The actual project under audit
│   ├── ARCHITECTURE_FINAL_V9.md
│   ├── PROJECT_DNA_V9.md
│   ├── V9_CHANGELOG.md
│   └── audit-history/        # All previous verification reports
└── README.md
```

## Usage

Open this workspace in Antigravity. The rules and workflows will load automatically.

To run a hostile audit:
```
/hostile-audit
```
