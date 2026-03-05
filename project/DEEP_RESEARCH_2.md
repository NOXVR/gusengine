# GusEngine: component selection and architecture for a self-hosted automotive RAG platform

**Qdrant, Docling, BGE-M3, and Open WebUI form the optimal stack for a production-grade, air-gappable RAG system that matches NotebookLM's retrieval architecture on a single Linux server.** After evaluating 50+ tools across eight component areas, the recommended stack eliminates the need for AnythingLLM, replaces Voyage AI with a local embedding model, and delivers structural PDF parsing with spatial citation metadata — all via Docker Compose on Ubuntu 24.04 LTS. The total resource footprint fits within **16–32 GB RAM and 4–8 CPU cores**, with GPU acceleration optional but beneficial for the ingestion pipeline. Every component below is open-source, self-hostable, and proven in production.

---

## A. Docling is the clear winner for structural PDF parsing with spatial metadata

The ingestion layer is the foundation of GusEngine's architecture. Of the ten tools evaluated, **Docling (by IBM, MIT license, v2.70+, ~15K GitHub stars)** is the only tool that natively produces structural chunks with full spatial metadata — page number and bounding box per element — out of the box.

Docling's RT-DETR-based layout model classifies page elements into categories (Text, Title, Table, Image, List, Formula) and its **TableFormer vision transformer** achieves best-in-class table structure recognition at **97.9% accuracy** — critical for the specification tables in vintage Mercedes FSMs. Its built-in `HybridChunker` respects document section boundaries (headings, page breaks, paragraphs), producing variable-length excerpts that preserve the structural hierarchy the target architecture demands. Each chunk carries provenance metadata: `page_no`, `bbox: {l, t, r, b}`, heading path, and element type.

Performance is strong: **0.49 sec/page on GPU, 3.1 sec/page on CPU**. For 500+ manuals averaging 200 pages each, that's roughly 86 hours on CPU or 14 hours on GPU — a one-time batch job. Docling supports multiple OCR backends (EasyOCR, Tesseract, RapidOCR) switchable per use case, and its `docling-serve` provides a Docker-based REST API for distributed processing.

**Key configuration for vintage FSMs:**

| Parameter | Recommended Value | Rationale |
|---|---|---|
| `do_ocr` | `True` | All vintage manuals are scanned |
| OCR engine | EasyOCR (default) | Better than Tesseract on degraded prints |
| OCR DPI | 300 | Higher for degraded 1960s documents |
| `max_tokens` (HybridChunker) | 512–1024 | Matches BGE-M3's sweet spot |
| Export format | JSON (lossless) | Preserves full spatial provenance |
| Languages | `["en", "de"]` | Some vintage MB manuals use German terms |

**Fallback for severely degraded pages:** Surya (by VikParuchuri, GPL-3.0) provides tunable `DETECTOR_BLANK_THRESHOLD` and `DETECTOR_TEXT_THRESHOLD` parameters specifically for faint/degraded text. Use Surya as a secondary OCR pass on pages where Docling's primary OCR produces low-confidence output. Pre-processing with OpenCV binarization, deskewing, and denoising is mandatory for 1960s-era scans regardless of OCR engine.

**Alternatives considered:** MinerU (54.6K stars, AGPL) is fastest on GPU at 0.21 sec/page but lacks Docling's native structural chunker and has a restrictive license. Marker/Surya produce excellent OCR but require more custom code to generate the spatial metadata map. Unstructured.io's open-source version underperforms Docling in benchmarks and does not benefit from GPU acceleration. LayoutParser is unmaintained (last release ~2022). PyMuPDF and pdfplumber cannot handle scanned PDFs without external OCR integration.

**Wiring schematics and exploded-view illustrations** cannot be "read" by any OCR tool. The correct approach: extract these as images with positional metadata during parsing, store alongside text chunks, and display the original PDF region to the technician when cited.

---

## B. Qdrant delivers hybrid search in a single container

**Qdrant (v1.15+, Apache 2.0, ~22K GitHub stars)** eliminates the need for a separate keyword search engine entirely. Since v1.10, Qdrant supports **native hybrid search** combining dense vectors (cosine similarity) and sparse BM25 vectors with built-in Reciprocal Rank Fusion (RRF) — all in a single query, a single container, using **1–2 GB RAM** for 50K excerpts.

The hybrid search mechanism works through Qdrant's `prefetch` API: two search branches (dense + sparse) execute in parallel server-side, and results merge via RRF or Distribution-Based Score Fusion (DBSF). Since v1.15.2, BM25 tokenization happens directly in the Qdrant server — no client-side sparse vector generation needed. This is architecturally identical to the target design: vector track and keyword track running simultaneously against the entire unified corpus.

**Exact-match search for part numbers** like "000 074 03 01" and wire codes like "1.5 bk/vi" requires a multi-layer approach. BM25 sparse search catches most keyword matches, but critical identifiers should also be indexed as `keyword` payload fields with exact-match filtering. A query classifier (simple regex) detects identifier-like patterns and adds payload filters automatically:

```python
# Qdrant collection setup
client.create_collection(
    collection_name="gus_engine",
    vectors_config={"dense": VectorParams(size=1024, distance=Distance.COSINE)},
    sparse_vectors_config={"bm25": SparseVectorParams(modifier=Modifier.IDF)},
)
# Payload indexes for exact matching
client.create_payload_index("gus_engine", "part_numbers", PayloadSchemaType.KEYWORD)
client.create_payload_index("gus_engine", "page_number", PayloadSchemaType.INTEGER)
client.create_payload_index("gus_engine", "manual_id", PayloadSchemaType.KEYWORD)
```

**Dynamic top-K via score thresholding** is implemented at the application layer: retrieve a generous pool (limit=200), compute the max RRF score, and filter results below **40% of the top score**. Additionally, score-gap detection (cut off when the gap between consecutive scores exceeds 2× the median gap) provides a second safety net. Weaviate's built-in `autocut` feature performs similar score-based truncation natively, but Qdrant's lower resource footprint and simpler single-container deployment make it the better choice for a single-server setup.

**Why not the alternatives:** Weaviate (BSD-3, strong hybrid search with `alpha` tuning) is a solid runner-up but consumes 2–4 GB RAM in Go runtime overhead. Milvus requires **three containers** (milvus + etcd + MinIO) and 8 GB minimum RAM — overkill. ChromaDB has no self-hosted hybrid search. Elasticsearch/OpenSearch require 4–8 GB RAM and are designed for billions of documents. pgvector requires manually implementing RRF via SQL CTEs.

**Docker deployment:**
```yaml
services:
  qdrant:
    image: qdrant/qdrant:v1.15.2
    ports: ["6333:6333", "6334:6334"]
    volumes: ["./qdrant_data:/qdrant/storage"]
    deploy:
      resources:
        limits:
          memory: 4G
```

---

## C. BGE-M3 paired with HuggingFace TEI replaces Voyage AI locally

**BAAI/bge-m3 (MIT license, 568M parameters, 1024 dimensions, 8192-token context)** is the recommended replacement for Voyage-3-large. It achieves **MTEB 63.0** versus Voyage-3-large's 66.8 — a ~4-point gap that represents the best achievable quality without external API dependencies. The gap narrows significantly with domain-specific fine-tuning on automotive service manual content.

BGE-M3's killer feature for GusEngine: it natively supports **dense + sparse + multi-vector retrieval simultaneously**, meaning it can generate both the dense embedding for semantic search AND the sparse representation for BM25 keyword search from a single model. Combined with Qdrant's dual-index architecture, this creates an end-to-end hybrid retrieval pipeline with minimal components. The **8192-token maximum input** is critical — it accommodates variable-length service manual chunks without truncation, unlike the 512-token limit on popular alternatives (BGE-large-en-v1.5, all-mpnet-base-v2, Arctic Embed).

**Serving infrastructure:** HuggingFace Text Embeddings Inference (TEI) is the production-grade serving layer. Written in Rust, it provides dynamic batching, Flash Attention, Prometheus metrics, and an OpenAI-compatible `/v1/embeddings` API endpoint. The CPU Docker image (`ghcr.io/huggingface/text-embeddings-inference:cpu-1.9`) runs BGE-M3 at **~20–30ms per query** using **3–4 GB RAM**.

For air-gapped deployment, pre-download the model weights (`git lfs clone https://huggingface.co/BAAI/bge-m3`) and mount them as a local volume:

```yaml
services:
  embeddings:
    image: ghcr.io/huggingface/text-embeddings-inference:cpu-1.9
    ports: ["8080:80"]
    volumes: ["./models/bge-m3:/data/bge-m3"]
    command: --model-id /data/bge-m3 --max-concurrent-requests 64
    deploy:
      resources:
        limits:
          memory: 8G
```

**Runner-up models worth noting:**

- **Qwen3-Embedding-0.6B** (Apache 2.0): MTEB 70.58, 32K-token context, flexible dimensions. Higher quality than BGE-M3 but 40–80ms latency on CPU. Choose this if a GPU is available or if multilingual German support is a priority.
- **nomic-embed-text-v1.5** (Apache 2.0): Only 137M parameters, 768 dimensions, 8192 tokens. At ~1–2 GB RAM and ~10ms latency, it's the budget option. Supports Matryoshka representation (truncatable to 256/128/64 dims) for storage savings.
- **Fine-tuning path**: Use `sentence-transformers` with `MultipleNegativesRankingLoss` on ~500 query-passage pairs created from your FSM corpus. Expected gain: **+10–30% retrieval accuracy** on domain-specific queries.

---

## D. Dynamic context filling replaces the catastrophic fixed TopN=4

The V9 system's fixed TopN=4 retrieval was insufficient. NotebookLM loaded **190 excerpts from 30 documents** in a single turn. GusEngine must implement a greedy fill algorithm that packs the 200K-token Claude context window to capacity.

**Token budget allocation for Claude Sonnet (200K window):**

| Component | Tokens | Notes |
|---|---|---|
| System prompt | ~2,500 | Role, citation format, domain constraints |
| Conversation history | 10,000–30,000 | Raw last 4 turns + summarized older turns |
| Safety margin | 2,000 | Buffer for estimation error |
| Generation headroom | 4,096 | `max_tokens` for Claude response |
| **Retrieved excerpts** | **~158,000–182,000** | Greedy fill from ranked candidates |

**Token counting without a local Claude tokenizer** is a real challenge — Anthropic does not provide one for Claude 3+ models. The recommended approach: **train a simple linear regression** (`tokens ≈ a×bytes + b×words + c×lines + d`) on ~500 representative chunks using the free Anthropic Token Count API as ground truth. This achieves **<1.5% mean absolute percentage error** on domain-specific content, far better than tiktoken's ~5–12% error rate on Claude text.

**The greedy fill algorithm** sorts hybrid search results by relevance score, then iterates: add the highest-scoring excerpt if it fits the remaining token budget, skip (don't truncate) if it doesn't, try the next-smaller excerpt. Key design decisions:

- **Never truncate excerpts** — automotive specs are safety-critical; cutting mid-specification risks dangerous errors
- **Dynamic relevance threshold at 40% of top score** — static cutoffs fail when score distributions vary by query type
- **15% diversity bonus** for excerpts from unrepresented documents — ensures breadth in multi-document queries
- **30% redundancy penalty** for same-document, same-section duplicates
- **Hard cap at 250 excerpts** — prevents degenerate cases while allowing NotebookLM-scale context loads

**Conversation history compression** preserves the last 4 turns verbatim and summarizes older turns into a structured diagnostic context (vehicle ID, system under diagnosis, tests performed, findings). This keeps history under 30K tokens while preserving the diagnostic thread critical for progressive refinement.

**Query rewriting for multi-turn retrieval** uses Claude Haiku (cheapest model) to generate 2–3 retrieval queries that incorporate conversation context, resolve pronouns ("it" → "the fuel pump on the W116 450SL"), and include both user phrasing and technical manual terminology.

---

## E. Open WebUI replaces AnythingLLM with native citation support

**AnythingLLM must be retired from the GusEngine stack.** Research confirms three critical, unfixable limitations: (1) no passthrough mode — you cannot inject pre-retrieved context through its API, (2) no custom citation rendering — sources are just filenames without page numbers or coordinates, and (3) fixed-size chunking hardcoded in the backend. These constraints make AnythingLLM fundamentally incompatible with GusEngine's architecture.

**Open WebUI** is the recommended replacement. It provides a production-ready chat interface with the only extensible citation system among open-source chat UIs. Its **Pipe/Function architecture** allows writing a Python function that calls GusEngine's custom backend, and its `__event_emitter__` with `type: "citation"` provides a native mechanism to pass structured citation metadata (document ID, page number, bounding box, section title) to the frontend.

The migration path is clear: deploy Open WebUI via Docker, write a GusEngine Pipe function that intercepts user messages, calls the custom retrieval backend, constructs the prompt with retrieved context, calls Claude, and emits citation events. The Svelte-based rendering pipeline (`MarkdownTokens.svelte`, `ContentRenderer.svelte`) is modular enough to extend for PDF-level citation rendering without a full fork.

**Citation rendering uses a hybrid pre-render approach:**

1. During ingestion: extract each PDF page as a **WebP image at 150 DPI** using PyMuPDF or pdf2image
2. Store page images alongside source PDFs (~200KB–1MB per page)
3. **Hover** `[N]` → popover shows pre-rendered page image with CSS-positioned highlight overlay (instant, no PDF.js overhead)
4. **Click** `[N]` → opens full PDF.js viewer with `@react-pdf-viewer/highlight` plugin, scrolled to the exact page with bounding box highlight
5. Serve images via a caching endpoint: `/api/pages/{doc_id}/{page_number}.webp`

For the full PDF viewer, **react-pdf-viewer's highlight plugin** accepts `HighlightArea` objects with percentage-based coordinates (`{pageIndex, top, left, height, width}`) derived from the stored bounding box metadata. The `jumpToHighlightArea` method scrolls directly to the citation location.

**LibreChat (MIT license)** is a viable fallback if Open WebUI's recent license change is a concern, but it lacks the citation event emitter system and would require deeper frontend modifications.

---

## F. Custom Python orchestration beats every framework for this pipeline

For a pipeline this bespoke, **custom Python code (~1,200 lines) is the clear winner over LangChain, LlamaIndex, Haystack, or any framework.** The core differentiators — dynamic context window filling, structural chunking with spatial metadata, hybrid search with identifier detection, and citation extraction — require custom code regardless of framework choice. A framework would add abstraction debt (debugging through LCEL chains when your custom retrieval logic breaks), token overhead (**1.5–2.4K extra tokens per request** per AIMultiple 2025 benchmarks), and dependency risk (LangChain is notorious for breaking changes).

The direct library stack is lean and complete:

- **`anthropic`** — Claude API (token counting + messages + streaming)
- **`qdrant-client`** — Vector DB with hybrid search
- **`sentence-transformers`** or **TEI HTTP client** — Local embedding
- **`httpx`** — Async HTTP for service communication
- **`numpy`** — RRF score fusion and normalization

The orchestration pipeline executes five phases per turn: (1) **Query phase** — rewrite query using conversation history via Claude Haiku, generate 2–3 retrieval queries; (2) **Retrieval phase** — embed queries, run hybrid search (dense + BM25 + RRF) in Qdrant, deduplicate across queries; (3) **Selection phase** — apply relevance threshold, execute greedy fill algorithm with diversity/redundancy scoring; (4) **Assembly phase** — format system prompt, compress conversation history if needed, format excerpts with citation markers, validate token budget; (5) **Generation phase** — call Claude Sonnet with streaming, extract `[N]` citations, map to source metadata, update conversation history, flush excerpts.

If a framework is ever desired, **Haystack (by deepset)** is the best option: explicit debuggable pipeline architecture, lowest token overhead (1.57K), native hybrid search support, and easy component swapping for A/B testing retrieval strategies.

---

## G. RAGFlow and Kotaemon are the closest existing projects

No single open-source project implements the full GusEngine vision, but two come close:

**Kotaemon (Apache 2.0, ~20K stars)** has the most directly relevant feature: **in-browser PDF viewing with bounding-box highlights** on citations. Its hybrid search (full-text + vector with re-ranking), question decomposition agents, and extensible Gradio UI make it the strongest foundation candidate. However, it lacks dual-track ingestion and dynamic context window management.

**RAGFlow (Apache 2.0, ~35K stars)** provides the best document understanding capabilities via its DeepDoc component (YOLOv8 layout detection + OCR with positional coordinates). Its unique **"Manual" chunking template** was designed for structured technical documents, and its **chunk visualization editor** allows human verification that torque specs aren't split across chunks. The tradeoff is a heavy Docker footprint (~9 GB).

**Docling + Kotaemon together cover ~70–80% of GusEngine's requirements.** The remaining gaps — automotive domain-specific chunking logic, dynamic context injection, and a mechanic-friendly UI — require custom code. The **RAG Document Viewer** by Preprocess.co is a useful frontend component: pass bounding-box coordinates and it auto-scrolls and spotlights the cited region in a self-contained HTML bundle embeddable via iframe.

Other notable projects: **Onyx/Danswer** (MIT, 25K stars) demonstrates multipass indexing (same document at multiple chunk sizes) via Vespa — a technique worth borrowing. **SurfSense** (7.6K stars) implements 2-tiered RAG with hybrid search + RRF. **Open-Parse** (MIT) provides bounding-box overlay visualization useful for debugging chunking during development.

---

## H. The recommended full-stack architecture

The final component stack, deployable via a single `docker-compose.yml`:

| Layer | Component | Image / Version | RAM | License |
|---|---|---|---|---|
| PDF Parsing | **Docling** | `docling-serve:latest` | 2–4 GB | MIT |
| OCR Fallback | **Surya** (for degraded pages) | Custom container | 2–4 GB | GPL-3.0 |
| Embedding | **BGE-M3** via **TEI** | `ghcr.io/huggingface/text-embeddings-inference:cpu-1.9` | 3–4 GB | MIT / Apache-2.0 |
| Vector + Search | **Qdrant** | `qdrant/qdrant:v1.15.2` | 1–2 GB | Apache-2.0 |
| LLM | **Claude Sonnet** (API) | Anthropic API | — | Commercial |
| Orchestration | **Custom Python** | Custom FastAPI container | 1 GB | — |
| Frontend | **Open WebUI** | `ghcr.io/open-webui/open-webui:main` | 1–2 GB | Custom |
| Page Images | **Nginx** (static file server) | `nginx:alpine` | 128 MB | BSD |
| **Total** | | | **~12–18 GB** | |

**Minimum server specs:** 16 GB RAM, 4 CPU cores, 100 GB NVMe SSD. **Recommended:** 32 GB RAM, 8 cores, 200 GB NVMe (allows GPU passthrough for faster ingestion). The system is fully air-gappable after initial model weight download and Docker image pull.

## Conclusion

The critical architectural insight is that **three tools eliminated entire complexity layers**: Docling's native structural chunker with spatial metadata eliminates the need for a custom parsing pipeline; Qdrant's built-in hybrid search (dense + BM25 + RRF) eliminates the need for a separate Elasticsearch instance; and Open WebUI's citation event emitter eliminates the need for a custom frontend from scratch. The total stack is **7 Docker containers** (including Nginx for page images), roughly **1,200 lines of custom Python** for the orchestration layer, and a one-time ingestion pipeline that pre-renders page images and generates the spatial metadata index. The V9 system's three fundamental limitations — fixed-size chunking, TopN=4 retrieval, and AnythingLLM's inability to inject custom context — are all resolved by this architecture. The remaining engineering risk concentrates in two areas: OCR quality on the most degraded 1960s-era scans (mitigated by Surya fallback with tuned thresholds), and the ~4-point MTEB gap between BGE-M3 and Voyage AI (closeable through domain-specific fine-tuning on automotive service manual content).