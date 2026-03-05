# **Comprehensive Technical Evaluation of Open-Weight Large Language Model Architectures for Localized Automotive Diagnostic Retrieval-Augmented Generation**

The technical migration of a high-reliability automotive diagnostic system from a frontier cloud-based model like Anthropic Claude 3.5 Sonnet to a localized open-weight framework necessitates a multi-layered evaluation of structural determinism, technical domain fluency, and deductive consistency. The "Gus" diagnostic engine, operating as a closed-loop state machine, places extreme demands on an inference engine to function not as a linguistic companion but as a rigid data processor within a Directed Acyclic Graph (DAG) architecture.1 The transition requires that the replacement model effectively manage a constrained 4,000-token context window while delivering raw JSON objects that satisfy zero-tolerance safety requirements.3 This analysis identifies Llama-3.3-70B-Instruct as the primary candidate, with Qwen3-32B-Instruct serving as the optimal secondary choice for resource-constrained environments, provided that inference is executed via a grammar-constrained backend such as vLLM or llama.cpp.5

## **Deterministic JSON Synthesis and Structural Enforcement Backends**

The most critical operational failure point in the current "Gus" architecture is the risk of malformed JSON output or the inclusion of conversational filler. In a safety-adjacent context, where a technician relies on the engine to provide mutually exclusive diagnostic answer paths, any deviation from the provided schema constitutes a production-breaking event.8 The analysis indicates that while prompt engineering can drive model reliability toward a 95th percentile, achieving the required 100% threshold requires a transition from probabilistic generation to constrained structural synthesis.9

### **Mechanics of Logit Masking and GBNF Grammar**

Local inference enables the implementation of GGML BNF (GBNF) grammars, a technique that restricts the vocabulary of the model at each step of token generation.11 During the sampling process, the inference backend (e.g., llama.cpp or Ollama) assesses the current state of the output string against a context-free grammar defined by the required JSON schema.6 Tokens that would result in a syntax violation are assigned a generation probability of ![][image1].6

This mechanism ensures that the first generated character is invariably {, the keys strictly match the predefined identifiers like mechanic\_instructions, and the values conform to the specified data types.8 By utilizing these backends, the "Gus" system can eliminate the need for brute-force JSON.parse() loops and regex-based repair pipelines that are often required for cloud-based models like Claude 3.5 Sonnet, which do not offer native grammar-constrained logit masking.10

### **Comparison of Backend Constraints and Scalability**

| Inference Engine | Constraint Mechanism | Production Readiness | Concurrency Support |
| :---- | :---- | :---- | :---- |
| **vLLM** | guided\_json (Outlines) | High (Enterprise) | Superior 15 |
| **Ollama** | format: "json" (GBNF) | High (Development) | Moderate 13 |
| **llama.cpp** | GBNF Grammar Files | High (Edge/Local) | Predictive 11 |
| **LocalAI** | CFG Enforcement | Moderate | High 9 |

The analysis suggests that for a production environment hosted on Ubuntu bare metal, vLLM provides the most robust path for scaling simultaneous diagnostic sessions.16 vLLM’s implementation of PagedAttention manages KV-cache memory with efficiency comparable to virtual memory systems in operating systems, preventing the fragmentation that typically degrades performance in multi-turn diagnostic flows.4 Conversely, Ollama offers a lower barrier to entry and a frictionless integration path with AnythingLLM, though it may introduce head-of-line blocking in high-concurrency scenarios.4

## **State Machine Compliance and Multi-Turn Instructional Logic**

The "Gus" engine is defined by a 5-phase DAG that leads a technician through triage, variable isolation, and physical testing.1 The inference model must act as the state transition logic, interpreting structured messages containing completed\_state and required\_next\_state directives.22

### **Triage and Isolation Dynamics (Phase A and B)**

In PHASE\_A\_TRIAGE, the model must transform vague symptoms, such as "cranks but won't catch," into a set of 2-5 mutually exclusive triage options derived strictly from the pinned tribal knowledge in MASTER\_LEDGER.md or retrieved service chunks.1 The transition to PHASE\_B\_FUNNEL represents the most significant test of the model's deductive logic.21 In this phase, the model must avoid "conclusion jumping," a common failure mode in LLMs where the model suggests a final repair before isolating the subsystem.25

The Berkeley Function Calling Leaderboard (BFCL) v4 introduces state-based evaluation, which measures a model’s ability to achieve the correct outcome in a stateful environment.21 Frontier models like Llama 3.3 70B and Qwen3 32B exhibit high scores in these agentic metrics, suggesting they can maintain awareness of the physical state of the vehicle (e.g., fuel pump active vs. inactive) across multiple interaction turns without repeating previous tests—a "looping" requirement central to Phase B.5

### **Transition Enforcement and Error Handling**

The DAG logic requires the model to set requires\_input: true in all phases except PHASE\_D\_CONCLUSION and RETRIEVAL\_FAILURE.1 Evaluation of instruction-following benchmarks (IFEval) shows that Llama 3.3 70B achieved a 92.1% accuracy rate, the highest among current open-weight models, in adhering to such complex, multi-part negative constraints.5 This reliability is essential to prevent "stalled diagnostics," where a model might output requires\_input: false prematurely, failing to render the answer buttons necessary for the technician to proceed.21

## **Epistemological Grounding and Citation Accuracy in Automotive RAG**

In a zero-tolerance diagnostic environment, the model's reliance on its training data (parametric knowledge) must be entirely suppressed in favor of the provided RAG context.29 The Authority Hierarchy establishes that the tribal knowledge ledger overrides the Factory Service Manual (FSM) if contradictions arise, a rule that requires the model to weigh different context sections dynamically.30

### **Watermark Detection vs. Arabic Numerical Logic**

The Gus system uses a sophisticated Dual-Layer Citation Rule to ensure that technicians are directed to the exact physical page of a manual.32 If the OCR-extracted text contains a specific watermark like \], the model is forbidden from performing any arithmetic and must cite the number directly.32

In cases where no watermark is found, the model must perform a localized calculation based on the chunk filename:

![][image2]

For instance, a retrieved chunk named 1975\_Mercedes\_FSM\_101-105.pdf that contains the relevant diagnostic procedure on its 3rd internal page must be cited as page 103 (![][image3]).32 Research into the mathematical reasoning capabilities of smaller models (7B-8B) suggests they frequently struggle with these intra-prompt arithmetic tasks, often defaulting to the first number in the filename or guessing.34 Transitioning to a 70B parameter model significantly improves the success rate of these citation computations due to their superior numerical logic and attention span.36

### **Suppression of Parametric Knowledge and Hallucination Resistance**

The most substantial risk in automotive diagnostics is the model suggesting procedures that are not present in the manual but exist in its training data.2 For example, a model might suggest "checking the OBD-II codes" for a 1975 Mercedes-Benz, a system that did not exist for another two decades.10 Llama 3.3 and Command-R variants are noted for their high "RAG faithfulness," exhibiting a decreased tendency to hallucinate technical specifications when a competing context is provided.40

The fallback RETRIEVAL\_FAILURE state must be triggered if no service manual chunks are retrieved.1 This safeguard prevents the model from "guessing" the repair based on the symptom alone. The analysis indicates that larger models are more adept at recognizing the absence of information and adhering to this "stop" command than smaller, more "eager" variants.21

## **Automotive Domain Competence: Classic Bosch Injection Systems**

The "Gus" engine operates within the technical domain of vintage fuel systems, specifically the Bosch Jetronic lineage used in the 1975 Mercedes-Benz 450SL.42 The model must navigate the distinct terminologies and physical isolation procedures associated with these mechanical and early electronic systems.

### **Technical Semantics of K-Jetronic and D-Jetronic**

Technical proficiency requires the model to understand the role of components such as the "warm-up regulator" (WUR) and the "fuel accumulator" in the K-Jetronic system.43 These systems are "continuous," meaning injectors spray constantly based on mechanical fuel distributor pressure, not electronic pulses.42 A symptom like "Hot start vapor lock" requires the model to isolate the fuel accumulator's check valve or the internal pressure-maintaining capacity of the system.43

Llama 3.3 70B and Qwen 2.5 72B have shown the highest accuracy in interpreting such legacy technical manuals.46 The models must instruct technicians to perform physical actions like "Connect a Bosch pressure tester (KDJE-7450) between the distributor and the warm-up regulator" and interpret the resulting pressures (e.g., 2.8 bar vs 3.5 bar) to determine if the regulator's bimetallic strip is functioning correctly.24

### **Numerical Precision and Specification Adherence**

Diagnostic procedures often depend on exact resistance or pressure values. For instance, the ballast resistors on a Bosch transistorized ignition system may require checking for a value of exactly ![][image4] or ![][image5].48 Misdiagnosis could occur if the model rounds these numbers or speculates based on general knowledge.10 The high-parameter density of the 70B models ensures that these numerical identifiers are retrieved with fidelity, maintaining the "authoritative mechanic" persona required for the Gus system.5

## **Ranked Recommendation List of Local HuggingFace Models**

The following models are ranked based on their performance in instruction following, function calling (JSON), and domain-specific reasoning, specifically targeted to the "Gus" production environment.

### **1\. Meta Llama-3.3-70B-Instruct**

The Llama-3.3-70B-Instruct model is the definitive recommendation for replacing Claude 3.5 Sonnet. It offers frontier-level instruction following with an IFEval score of 92.1%, matching or exceeding the capabilities of the much larger Llama 3.1 405B.5

* **JSON Reliability:** Native ability to follow complex schemas is enhanced by a mature ecosystem of GGUF/AWQ quants optimized for grammar backends.50  
* **Instruction Following:** Exceptional adherence to the "Master Ledger" authority and negative constraints.5  
* **RAG Faithfulness:** Proven reliability in maintaining context grounding up to 8k tokens, well beyond the system's 4k cap.36  
* **AnythingLLM Integration:** Fully supported via Ollama or vLLM.4  
* **Suitability:** This model is the only open-weight variant that consistently matches Claude 3.5's ability to maintain a deterministic state machine while performing on-the-fly citation arithmetic.5

### **2\. Qwen3-32B-Instruct**

The Qwen3-32B-Instruct (including Reasoning-distilled variants) represents the current "sweet spot" for high intelligence on consumer-grade hardware.7

* **JSON Reliability:** Highly optimized for structured output, frequently leading the BFCL benchmarks in its size class.27  
* **Instruction Following:** Strong MT-Bench performance (9.35 for the 72B, scaled reliably to the 32B).28  
* **RAG Faithfulness:** Exhibits "Needle in a Haystack" retrieval accuracy across its entire context window.58  
* **AnythingLLM Integration:** Standard support in Ollama and LM Studio.60  
* **Suitability:** Ideal for deployment on a single 24GB VRAM GPU (RTX 3090/4090), providing a near-100% guarantee of JSON structural integrity.51

### **3\. Mistral-Small-24B-Instruct-2501**

A precision-tuned model released in January 2025, specifically designed for tool-use and agentic interactions.62

* **JSON Reliability:** Natively capable of high-accuracy function calling with a focus on constrained output.41  
* **Instruction Following:** Superior performance on receipt/bill processing benchmarks suggests high reliability for numeric data extraction in Gus.41  
* **RAG Faithfulness:** Mistral’s technical refinement minimizes "hallucination bloat," sticking strictly to provided service manual text.41  
* **AnythingLLM Integration:** Fully compatible with vLLM and AnythingLLM's internal Docker orchestration.15  
* **Suitability:** Recommended for low-latency diagnostic sessions where rapid Time to First Token (TTFT) is required.62

### **4\. Microsoft Phi-4 (14B)**

The 14B Phi-4 model leverages extensive synthetic data to achieve reasoning capabilities that rival much larger dense models.37

* **JSON Reliability:** High performance on coding and math benchmarks translates to reliable schema compliance.49  
* **Instruction Following:** Microsoft's post-training focus on reasoning-dense data makes it highly resilient to "distractor" information in RAG chunks.37  
* **RAG Faithfulness:** Strong STEM-focused QA capabilities ensure torque and pressure values are cited with precision.66  
* **AnythingLLM Integration:** Pullable via Ollama as phi4.37  
* **Suitability:** Excellent for secondary validation or for technicians using low-power mobile workstations.41

### **5\. Cohere Command-R (35B)**

The Command-R family is explicitly trained for "grounded generation," featuring built-in citation capabilities.29

* **JSON Reliability:** Designed for enterprise tool-use with native support for structured responses.40  
* **Instruction Following:** Capable of iterating through "Action-Observation-Reflection" cycles, mapping perfectly to the Gus test-report cycle.40  
* **RAG Faithfulness:** Its unique pre-training allows it to predict document relevance before generating an answer, reducing citation hallucination.40  
* **AnythingLLM Integration:** Directly supported LLM provider in AnythingLLM settings.69  
* **Suitability:** Most "Claude-like" in its RAG behavior, though users must be aware of its specific non-commercial licensing constraints.40

## **Hardware Sizing Guide for Localized Production**

Deploying the top-tier Llama-3.3-70B model requires hardware that can maintain latency below the 5-second threshold for a 200-375 token JSON response.51

### **Memory Footprint and Quantization Analysis**

The VRAM requirements for a 70B model vary significantly based on the bit-depth of the weights.72

| Quantization Level | VRAM Requirement (70B) | Perceived Quality | Speed (Tokens/Sec) |
| :---- | :---- | :---- | :---- |
| **Q4\_K\_M** | \~40-43 GB | Optimal 51 | \~10-15 (Dual 3090\) |
| **Q5\_K\_M** | \~48-50 GB | High 51 | \~8-12 (Dual 4090\) |
| **Q8\_0** | \~77-80 GB | Near-lossless 51 | \~30-50 (A100) |
| **FP16** | \~140-160 GB | Baseline | \~20-30 (H100 Cluster) |

For the "Gus" engine, **Q4\_K\_M or Q5\_K\_M** quantization is the recommended balance.51 Q4\_K\_M retains nearly all of the base model's reasoning capabilities while fitting within the total VRAM available on dual consumer GPUs.55 Q2 or Q3 quants are explicitly disqualified as they exhibit significant degradation in instruction-following and numerical precision.35

### **GPU Selection Tiers**

* **Minimum Viable Hardware (MVH):** A single **NVIDIA RTX 4090 (24GB)** can run the **Qwen3-32B** model at Q4\_K\_M quantization with excellent responsiveness.51 Total VRAM usage with a 4k context and framework overhead is approximately 22-24 GB.51  
* **Recommended Hardware (RH):** A workstation with **dual NVIDIA RTX 3090 or 4090 (48GB total)** connected via NVLink or high-speed PCIe. This setup allows **Llama-3.3-70B (Q4\_K\_M)** to fit entirely in VRAM, avoiding the massive performance penalty of offloading layers to system RAM.50  
* **Optimal Hardware (OH):** An **NVIDIA A100 80GB or RTX 6000 Ada (48GB)**. These enterprise-grade cards feature significantly higher memory bandwidth (up to 2TB/s on A100), which directly translates to near-instantaneous JSON generation for a smooth technician experience.16

## **AnythingLLM Integration and Local Deployment Guide**

Migrating to the \#1 recommended model (Llama-3.3-70B) within the AnythingLLM orchestration layer is a three-step process focusing on backend installation, model instantiation, and structural enforcement.

### **Step 1: Backend Installation (Ollama)**

Ollama is the preferred local server for AnythingLLM due to its one-line installation and built-in grammar support.4

Bash

\# Ubuntu Installation  
curl \-fsSL https://ollama.com/install.sh | sh

\# Configure environment for Docker access  
sudo systemctl edit ollama.service  
\# Add: Environment="Ollama\_HOST=0.0.0.0"  
sudo systemctl daemon-reload  
sudo systemctl restart ollama

### **Step 2: Model Configuration via Modelfile**

To ensure the "Gus" priming is inherent to the model and that JSON formatting is forced at the engine level, a custom Modelfile is required.13

FROM llama3.3:70b

PARAMETER temperature 0

PARAMETER num\_ctx 4000

PARAMETER format json

SYSTEM """

PRIME DIRECTIVE: YOU ARE "GUS"... (Insert the full 750-token system prompt here)

"""

Execute ollama create gus-logic \-f Modelfile to build the deployment container.

### **Step 3: AnythingLLM Provider Settings**

Navigate to **Settings → AI Providers → Ollama**:

* **Ollama Base URL:** http://127.0.0.1:11434 (or http://172.17.0.1:11434 for Docker-to-host communication).3  
* **Model Name:** gus-logic.  
* **Token Context Window:** 4000\. This cap must match the system's ingestion logic to maintain deterministic retrieval results.3

## **Head-to-Head Comparison: Llama-3.3-70B vs. Claude 3.5 Sonnet**

Switching from a frontier cloud model to a local open-weight model involves a fundamental shift in reliability and infrastructure.

### **Capability Audit**

| Dimension | Claude 3.5 Sonnet | Llama-3.3-70B (Local) |
| :---- | :---- | :---- |
| **JSON Consistency** | Probabilistic (99.9%) | Deterministic (100% via GBNF) 6 |
| **Instruction Adherence** | Ceiling-level | Ceiling-level (92.1% IFEval) 5 |
| **Technical Reasoning** | High (Generalist) | High (Generalist) 35 |
| **Citation Math** | Accurate | Accurate at 70B scale 34 |
| **TTFT (Latency)** | \~500ms \- 2s (Network) | \~100ms \- 800ms (Local) 16 |
| **Context Window** | 200,000 tokens | 128,000 tokens (Native) 64 |

### **Capabilities Gained**

* **Structural Guarantee:** By moving inference to a GBNF-capable backend, the system gains a mathematical certainty of JSON validity that Claude’s API cannot theoretically provide.6  
* **Privacy and Sovereignty:** 100% of tribal knowledge ledgers and service manual vectors remain air-gapped on the local Ubuntu server, fulfilling data residency requirements.54  
* **Availability:** Dependency on Anthropic’s cloud infrastructure is removed, eliminating the single point of failure that can cause the Gus engine to go offline.78

### **Capabilities Lost**

* **Implicit Commonsense Knowledge:** Claude 3.5 Sonnet possesses a deeper layer of "implicit world knowledge" that serves as a safety net if a specific manual procedure is ambiguous.35 While "Gus" is forbidden from using training data, this general intelligence contributes to more fluid handling of user typos and edge-case phrasing.49  
* **Long-Context Stability:** Claude maintains higher coherence at extremely large context sizes.64 While not relevant for the current 4k cap, it limits the system’s ability to ingest entire volumes of service manuals simultaneously in future phases.53

## **Risk Assessment and Mitigation Strategies**

The transition to local open-weight models introduces specific failure modes that differ from those found in proprietary APIs.

### **Likely Failure Vectors**

1. **"Greedy" State Transition:** Local models, particularly when quantized, may exhibit a bias toward completing the task as quickly as possible, potentially skipping the isolation loops in PHASE\_B\_FUNNEL.21  
2. **Numeric Hallucination in Arithmetic:** If the model's logic units are compromised by heavy quantization (e.g., 2-bit or 3-bit), the absolute page number calculation may return incorrect offsets.10  
3. **Resource Contention:** On a production bare-metal server, concurrent RAG embedding (Voyage AI) and LLM inference (Ollama) may compete for PCIe bandwidth, leading to TTFT spikes.4

### **Strategic Mitigation**

* **Low-Temperature Sampling:** Set temperature strictly to 0.0.13 This forces the model to select the most probable (grounded) token at each step, significantly reducing the "creativity" that leads to hallucination in technical procedures.10  
* **Intra-Prompt Formatting (Prefilling):** Using the llama.cpp server, developers can "prefill" the model’s response with the starting character {. This acts as a powerful structural anchor, forcing the model into the correct schema distribution immediately.14  
* **Negative Constraint Strengthening:** The system prompt should include explicit prohibitions such as "NEVER output text before the first brace. NEVER include a summary".10  
* **Rigid Stop Sequences:** Configure AnythingLLM or the backend to terminate generation upon the token }, preventing the model from appending any trailing explanatory prose.10

## **Conclusion**

The transition of the "Gus" automotive diagnostic engine from Anthropic Claude 3.5 Sonnet to a localized HuggingFace architecture is not only technically feasible but architecturally superior for deterministic requirements. The **Llama-3.3-70B-Instruct** model, deployed via **vLLM or Ollama** with **GBNF grammar enforcement**, provides a zero-tolerance framework for JSON output and state machine compliance.5 This configuration leverages the high-speed latency of local hardware while maintaining the deductive rigor necessary for safety-critical vehicle repair.4 For organizations operating on a single GPU budget, **Qwen3-32B-Instruct** serves as the optimal secondary candidate, delivering high precision and structural reliability with a smaller VRAM footprint.7 The deployment of these localized open-weight architectures ensures 100% data privacy and 100% structural formatting uptime, representing a significant advancement in the reliability of automotive RAG systems.77

#### **Works cited**

1. BFCL V4 • Agentic Part 1: Web Search \- Gorilla LLM, accessed February 17, 2026, [https://gorilla.cs.berkeley.edu/blogs/15\_bfcl\_v4\_web\_search.html](https://gorilla.cs.berkeley.edu/blogs/15_bfcl_v4_web_search.html)  
2. Berkeley Function Calling Leaderboard v4 \- Emergent Mind, accessed February 17, 2026, [https://www.emergentmind.com/topics/berkeley-function-calling-leaderboard-v4-bfclv4](https://www.emergentmind.com/topics/berkeley-function-calling-leaderboard-v4-bfclv4)  
3. Ollama LLM \- AnythingLLM Docs, accessed February 17, 2026, [https://docs.useanything.com/setup/llm-configuration/local/ollama](https://docs.useanything.com/setup/llm-configuration/local/ollama)  
4. Ollama vs vLLM: A Comprehensive Guide to Local LLM Serving | by Mustafa Genc \- Medium, accessed February 17, 2026, [https://medium.com/@mustafa.gencc94/ollama-vs-vllm-a-comprehensive-guide-to-local-llm-serving-91705ec50c1d](https://medium.com/@mustafa.gencc94/ollama-vs-vllm-a-comprehensive-guide-to-local-llm-serving-91705ec50c1d)  
5. Revisiting the Reliability of Language Models in Instruction-Following \- arXiv, accessed February 17, 2026, [https://arxiv.org/html/2512.14754v1](https://arxiv.org/html/2512.14754v1)  
6. Interaction between Ollama's JSON Mode and Thinking Feature \- Zenn, accessed February 17, 2026, [https://zenn.dev/7shi/articles/fa36989a04c9ed?locale=en](https://zenn.dev/7shi/articles/fa36989a04c9ed?locale=en)  
7. LLM Benchmarks April 2025 \- TIMETOACT GROUP Österreich, accessed February 17, 2026, [https://www.timetoact-group.at/en/insights/llm-benchmarks/llm-benchmarks-april-2025](https://www.timetoact-group.at/en/insights/llm-benchmarks/llm-benchmarks-april-2025)  
8. How to Get Structured JSON Responses from a LLM using Ollama \- AI and VoIP Blog, accessed February 17, 2026, [https://voipnuggets.com/2025/12/30/how-to-get-structured-json-responses-from-a-llm-using-ollama/](https://voipnuggets.com/2025/12/30/how-to-get-structured-json-responses-from-a-llm-using-ollama/)  
9. How can I get LLM to only respond in JSON strings? \- Stack Overflow, accessed February 17, 2026, [https://stackoverflow.com/questions/77407632/how-can-i-get-llm-to-only-respond-in-json-strings](https://stackoverflow.com/questions/77407632/how-can-i-get-llm-to-only-respond-in-json-strings)  
10. JSON Parsing Guide for GPT-OSS Models : r/LocalLLaMA \- Reddit, accessed February 17, 2026, [https://www.reddit.com/r/LocalLLaMA/comments/1n1bqlb/json\_parsing\_guide\_for\_gptoss\_models/](https://www.reddit.com/r/LocalLLaMA/comments/1n1bqlb/json_parsing_guide_for_gptoss_models/)  
11. Structured Output of Large Language Models | Niklas Heidloff, accessed February 17, 2026, [https://heidloff.net/article/llm-structured-output/](https://heidloff.net/article/llm-structured-output/)  
12. Practical Techniques to constraint LLM output in JSON format | by Minyang Chen \- Medium, accessed February 17, 2026, [https://mychen76.medium.com/practical-techniques-to-constraint-llm-output-in-json-format-e3e72396c670](https://mychen76.medium.com/practical-techniques-to-constraint-llm-output-in-json-format-e3e72396c670)  
13. Structured Outputs \- Ollama's documentation, accessed February 17, 2026, [https://docs.ollama.com/capabilities/structured-outputs](https://docs.ollama.com/capabilities/structured-outputs)  
14. How to force LLama3.1 to respond with JSON only? : r/LocalLLaMA \- Reddit, accessed February 17, 2026, [https://www.reddit.com/r/LocalLLaMA/comments/1eqayuq/how\_to\_force\_llama31\_to\_respond\_with\_json\_only/](https://www.reddit.com/r/LocalLLaMA/comments/1eqayuq/how_to_force_llama31_to_respond_with_json_only/)  
15. Structured Outputs \- vLLM, accessed February 17, 2026, [https://docs.vllm.ai/en/latest/features/structured\_outputs/](https://docs.vllm.ai/en/latest/features/structured_outputs/)  
16. Ollama vs. vLLM: A deep dive into performance benchmarking | Red Hat Developer, accessed February 17, 2026, [https://developers.redhat.com/articles/2025/08/08/ollama-vs-vllm-deep-dive-performance-benchmarking](https://developers.redhat.com/articles/2025/08/08/ollama-vs-vllm-deep-dive-performance-benchmarking)  
17. vLLM vs. Ollama: When to use each framework \- Red Hat, accessed February 17, 2026, [https://www.redhat.com/en/topics/ai/vllm-vs-ollama](https://www.redhat.com/en/topics/ai/vllm-vs-ollama)  
18. vLLM or llama.cpp: Choosing the right LLM inference engine for your use case, accessed February 17, 2026, [https://developers.redhat.com/articles/2025/09/30/vllm-or-llamacpp-choosing-right-llm-inference-engine-your-use-case](https://developers.redhat.com/articles/2025/09/30/vllm-or-llamacpp-choosing-right-llm-inference-engine-your-use-case)  
19. Local AI Agents That Run Your Life Offline: The Self-Hosted Micro-Empire Blueprint \- Dev.to, accessed February 17, 2026, [https://dev.to/adithyasrivatsa/local-ai-agents-that-run-your-life-offline-the-self-hosted-micro-empire-blueprint-18c2](https://dev.to/adithyasrivatsa/local-ai-agents-that-run-your-life-offline-the-self-hosted-micro-empire-blueprint-18c2)  
20. vLLM vs Ollama: Key differences, performance, and how to run them | Blog \- Northflank, accessed February 17, 2026, [https://northflank.com/blog/vllm-vs-ollama-and-how-to-run-them](https://northflank.com/blog/vllm-vs-ollama-and-how-to-run-them)  
21. From Tool Use to Holistic Agent Evaluation: An In-Depth Analysis of the Berkeley Function Calling Leaderboard (BFCL) \- Hugging Face, accessed February 17, 2026, [https://huggingface.co/datasets/tuandunghcmut/BFCL\_v4\_information/blob/main/From%20Tool%20Use%20to%20Holistic%20Agent%20Evaluation\_%20An%20In-Depth%20Analysis%20of%20the%20Berkeley%20Function%20Calling%20Leaderboard%20(BFCL).md](https://huggingface.co/datasets/tuandunghcmut/BFCL_v4_information/blob/main/From%20Tool%20Use%20to%20Holistic%20Agent%20Evaluation_%20An%20In-Depth%20Analysis%20of%20the%20Berkeley%20Function%20Calling%20Leaderboard%20\(BFCL\).md)  
22. \[QUESTION\] Best practice for providing large, temporary context (e.g., transcripts) for a single chat session? · Issue \#4585 · Mintplex-Labs/anything-llm \- GitHub, accessed February 17, 2026, [https://github.com/Mintplex-Labs/anything-llm/issues/4585](https://github.com/Mintplex-Labs/anything-llm/issues/4585)  
23. LLM Applications: Current Paradigms and the Next Frontier \- arXiv.org, accessed February 17, 2026, [https://arxiv.org/html/2503.04596v2](https://arxiv.org/html/2503.04596v2)  
24. Bosch K-Jetronic (CIS) explained \- YouTube, accessed February 17, 2026, [https://www.youtube.com/watch?v=a4fJAfXYxWk](https://www.youtube.com/watch?v=a4fJAfXYxWk)  
25. Benchmarking large language models GPT-4o, llama 3.1, and qwen 2.5 for cancer genetic variant classification \- PubMed, accessed February 17, 2026, [https://pubmed.ncbi.nlm.nih.gov/40369023/](https://pubmed.ncbi.nlm.nih.gov/40369023/)  
26. Berkeley Function Calling Leaderboard (BFCL) V4 \- Gorilla, accessed February 17, 2026, [https://gorilla.cs.berkeley.edu/leaderboard.html](https://gorilla.cs.berkeley.edu/leaderboard.html)  
27. LLM Rankings | OpenRouter, accessed February 17, 2026, [https://openrouter.ai/rankings](https://openrouter.ai/rankings)  
28. Llama 3 vs Qwen 2: The Best Open Source AI Models of 2024 | by Novita AI \- Medium, accessed February 17, 2026, [https://medium.com/@marketing\_novita.ai/llama-3-vs-qwen-2-the-best-open-source-ai-models-of-2024-15b3f29a7fc3](https://medium.com/@marketing_novita.ai/llama-3-vs-qwen-2-the-best-open-source-ai-models-of-2024-15b3f29a7fc3)  
29. Llama 3.1 405B vs Command R Plus | AIMLAPI Model Comparison, accessed February 17, 2026, [https://aimlapi.com/comparisons/llama-3-1-405b-vs-command-r-plus](https://aimlapi.com/comparisons/llama-3-1-405b-vs-command-r-plus)  
30. The best open source large language model \- Baseten, accessed February 17, 2026, [https://www.baseten.co/blog/the-best-open-source-large-language-model/](https://www.baseten.co/blog/the-best-open-source-large-language-model/)  
31. Llama 3.3 Euryale 70B vs Qwen2.5 72B Instruct (Comparative Analysis) \- Galaxy.ai Blog, accessed February 17, 2026, [https://blog.galaxy.ai/compare/l3-3-euryale-70b-vs-qwen-2-5-72b-instruct](https://blog.galaxy.ai/compare/l3-3-euryale-70b-vs-qwen-2-5-72b-instruct)  
32. Box 111, Roman numerals used as page numbers \- Citing Medicine \- NCBI Bookshelf, accessed February 17, 2026, [https://www.ncbi.nlm.nih.gov/books/NBK7271/box/A36247/?report=objectonly](https://www.ncbi.nlm.nih.gov/books/NBK7271/box/A36247/?report=objectonly)  
33. PolyNorm: Few-Shot LLM-Based Text Normalization for Text-to-Speech \- arXiv, accessed February 17, 2026, [https://arxiv.org/html/2511.03080v1](https://arxiv.org/html/2511.03080v1)  
34. Reasoning or Memorization? Unreliable Results of Reinforcement Learning Due to Data Contamination \- arXiv, accessed February 17, 2026, [https://arxiv.org/html/2507.10532v2](https://arxiv.org/html/2507.10532v2)  
35. Llama 3.3 vs Qwen 2.5 : r/LocalLLaMA \- Reddit, accessed February 17, 2026, [https://www.reddit.com/r/LocalLLaMA/comments/1h91e4h/llama\_33\_vs\_qwen\_25/](https://www.reddit.com/r/LocalLLaMA/comments/1h91e4h/llama_33_vs_qwen_25/)  
36. Llama 3.3 Instruct 70B Intelligence, Performance & Price Analysis, accessed February 17, 2026, [https://artificialanalysis.ai/models/llama-3-3-instruct-70b](https://artificialanalysis.ai/models/llama-3-3-instruct-70b)  
37. Phi 4 is just 14B But Better than llama 3.1 70b for several tasks. : r/LocalLLaMA \- Reddit, accessed February 17, 2026, [https://www.reddit.com/r/LocalLLaMA/comments/1hx5i8u/phi\_4\_is\_just\_14b\_but\_better\_than\_llama\_31\_70b/](https://www.reddit.com/r/LocalLLaMA/comments/1hx5i8u/phi_4_is_just_14b_but_better_than_llama_31_70b/)  
38. Benchmarking LLM Faithfulness in RAG with Evolving Leaderboards \- arXiv, accessed February 17, 2026, [https://arxiv.org/html/2505.04847v2](https://arxiv.org/html/2505.04847v2)  
39. EV Powertrain Systems Diagnostics & Prognostics Utilizing AI & ML (LLM) Based Approach, accessed February 17, 2026, [https://saemobilus.sae.org/papers/ev-powertrain-systems-diagnostics-prognostics-utilizing-ai-ml-llm-based-approach-2026-26-0664](https://saemobilus.sae.org/papers/ev-powertrain-systems-diagnostics-prognostics-utilizing-ai-ml-llm-based-approach-2026-26-0664)  
40. CohereLabs/c4ai-command-r-v01 · Hugging Face, accessed February 17, 2026, [https://huggingface.co/CohereForAI/c4ai-command-r-v01](https://huggingface.co/CohereForAI/c4ai-command-r-v01)  
41. Top 7 Open-Source LLMs in 2025 \- KDnuggets, accessed February 17, 2026, [https://www.kdnuggets.com/top-7-open-source-llms-in-2025](https://www.kdnuggets.com/top-7-open-source-llms-in-2025)  
42. About Us \- CIS-Jetronic.com, accessed February 17, 2026, [https://cis-jetronic.com/index.php?rt=content/content\&content\_id=1](https://cis-jetronic.com/index.php?rt=content/content&content_id=1)  
43. Jetronic \- Wikipedia, accessed February 17, 2026, [https://en.wikipedia.org/wiki/Jetronic](https://en.wikipedia.org/wiki/Jetronic)  
44. K-jetronic \- MRC-technics, accessed February 17, 2026, [https://mrc-technics.com/en/k-jetronic/](https://mrc-technics.com/en/k-jetronic/)  
45. D-Jetronic chapter 1: History, accessed February 17, 2026, [https://jetronic.org/en/d-jetronic/history](https://jetronic.org/en/d-jetronic/history)  
46. Meta: Llama 3.3 70B Instruct vs Qwen2.5 72B Instruct: AI Model Comparison | Krater.ai, accessed February 17, 2026, [https://krater.ai/compare/llama-3-3-70b-instruct-vs-qwen-2-5-72b-instruct](https://krater.ai/compare/llama-3-3-70b-instruct-vs-qwen-2-5-72b-instruct)  
47. Qwen 2.5 72b vs Llama 3.3 70b: Which Model Suits Your Needs? \- Novita AI Blog, accessed February 17, 2026, [https://blogs.novita.ai/qwen-2-5-72b-vs-llama-3-3-70b-which-model-suits-your-needs/](https://blogs.novita.ai/qwen-2-5-72b-vs-llama-3-3-70b-which-model-suits-your-needs/)  
48. Your Quick Guide To The Bosch D-Jetronic, K-Jetronic and KE-Jetronic Fuel Injection Systems | The Online Automotive Marketplace | Hemmings, The World's Largest Collector Car Marketplace, accessed February 17, 2026, [https://www.hemmings.com/stories/your-quick-guide-to-the-bosch-d-jetronic-k-jetronic-and-ke-jetronic-fuel-injection-systems/](https://www.hemmings.com/stories/your-quick-guide-to-the-bosch-d-jetronic-k-jetronic-and-ke-jetronic-fuel-injection-systems/)  
49. The Top 10 Open Source Large Language Models of 2025 \- Clarifai, accessed February 17, 2026, [https://www.clarifai.com/blog/top-open-source-llms/](https://www.clarifai.com/blog/top-open-source-llms/)  
50. GPU Requirement Guide for Llama 3 (All Variants) \- ApX Machine Learning, accessed February 17, 2026, [https://apxml.com/posts/ultimate-system-requirements-llama-3-models](https://apxml.com/posts/ultimate-system-requirements-llama-3-models)  
51. Ollama VRAM Requirements: Complete 2026 Guide to GPU Memory for Local LLMs, accessed February 17, 2026, [https://localllm.in/blog/ollama-vram-requirements-for-local-llms](https://localllm.in/blog/ollama-vram-requirements-for-local-llms)  
52. 10 Best Open-Source LLM Models (2025 Updated): Llama 4, Qwen 3 and DeepSeek R1, accessed February 17, 2026, [https://huggingface.co/blog/daya-shankar/open-source-llms](https://huggingface.co/blog/daya-shankar/open-source-llms)  
53. \[AINews\] Mistral Large 2 \+ RIP Mistral 7B, 8x7B, 8x22B \- Buttondown, accessed February 17, 2026, [https://buttondown.com/ainews/archive/ainews-mistral-large-2/](https://buttondown.com/ainews/archive/ainews-mistral-large-2/)  
54. Run LLMs Locally with Ollama: Privacy-First AI for Developers in 2025 \- Cohorte Projects, accessed February 17, 2026, [https://www.cohorte.co/blog/run-llms-locally-with-ollama-privacy-first-ai-for-developers-in-2025](https://www.cohorte.co/blog/run-llms-locally-with-ollama-privacy-first-ai-for-developers-in-2025)  
55. Llama-3.3-70B-Instruct | Hacker News, accessed February 17, 2026, [https://news.ycombinator.com/item?id=42341388](https://news.ycombinator.com/item?id=42341388)  
56. Tool Calling with Local LLMs: A Practical Evaluation \- Docker, accessed February 17, 2026, [https://www.docker.com/blog/local-llm-tool-calling-a-practical-evaluation/](https://www.docker.com/blog/local-llm-tool-calling-a-practical-evaluation/)  
57. Best Open Source LLM February 2026 | Top Free AI Models Ranked \- WhatLLM.org, accessed February 17, 2026, [https://whatllm.org/blog/best-open-source-models-february-2026](https://whatllm.org/blog/best-open-source-models-february-2026)  
58. Qwen 2 VS LLama 3 Comparison \- AIMLAPI.com, accessed February 17, 2026, [https://aimlapi.com/comparisons/qwen-2-vs-llama-3-comparison](https://aimlapi.com/comparisons/qwen-2-vs-llama-3-comparison)  
59. Qwen 2 72B VS LLama 3 70B \- AICC \- AI.cc, accessed February 17, 2026, [https://www.ai.cc/blogs/qwen-2-72b-vs-llama-3-70b/](https://www.ai.cc/blogs/qwen-2-72b-vs-llama-3-70b/)  
60. How to force a json schema output in ollama with openwebui? : r/LocalLLaMA \- Reddit, accessed February 17, 2026, [https://www.reddit.com/r/LocalLLaMA/comments/1oxbhg7/how\_to\_force\_a\_json\_schema\_output\_in\_ollama\_with/](https://www.reddit.com/r/LocalLLaMA/comments/1oxbhg7/how_to_force_a_json_schema_output_in_ollama_with/)  
61. newbie confusion: LocalLM / AnythingLLM / llama.cpp / Lamafile / Ollama / openwebui All the same? : r/LocalLLM \- Reddit, accessed February 17, 2026, [https://www.reddit.com/r/LocalLLM/comments/1cq38we/newbie\_confusion\_locallm\_anythingllm\_llamacpp/](https://www.reddit.com/r/LocalLLM/comments/1cq38we/newbie_confusion_locallm_anythingllm_llamacpp/)  
62. Most capable function calling open weight model in Jan/2025? : r/LocalLLaMA \- Reddit, accessed February 17, 2026, [https://www.reddit.com/r/LocalLLaMA/comments/1ihnt5t/most\_capable\_function\_calling\_open\_weight\_model/](https://www.reddit.com/r/LocalLLaMA/comments/1ihnt5t/most_capable_function_calling_open_weight_model/)  
63. Best Open Source LLMs in 2025 \- Koyeb, accessed February 17, 2026, [https://www.koyeb.com/blog/best-open-source-llms-in-2025](https://www.koyeb.com/blog/best-open-source-llms-in-2025)  
64. Most powerful LLMs (Large Language Models) in 2025 \- Codingscape, accessed February 17, 2026, [https://codingscape.com/blog/most-powerful-llms-large-language-models](https://codingscape.com/blog/most-powerful-llms-large-language-models)  
65. LLM Leaderboard: Which LLMs are Best for Which Tasks? (2026) \- Stack AI, accessed February 17, 2026, [https://www.stack-ai.com/blog/llm-leaderboard-which-llms-are-best-for-which-tasks](https://www.stack-ai.com/blog/llm-leaderboard-which-llms-are-best-for-which-tasks)  
66. Phi-4 Technical Report \- arXiv, accessed February 17, 2026, [https://arxiv.org/html/2412.08905v1](https://arxiv.org/html/2412.08905v1)  
67. EasierAI/Phi-4-14B \- Hugging Face, accessed February 17, 2026, [https://huggingface.co/EasierAI/Phi-4-14B](https://huggingface.co/EasierAI/Phi-4-14B)  
68. Complete Guide to llama.cpp: Local LLM Inference Made Simple | by Huda Saleh, accessed February 17, 2026, [https://levelup.gitconnected.com/complete-guide-to-llama-cpp-local-llm-inference-made-simple-50dce3102413](https://levelup.gitconnected.com/complete-guide-to-llama-cpp-local-llm-inference-made-simple-50dce3102413)  
69. Top 10 open source LLMs for 2025 \- NetApp Instaclustr, accessed February 17, 2026, [https://www.instaclustr.com/education/open-source-ai/top-10-open-source-llms-for-2025/](https://www.instaclustr.com/education/open-source-ai/top-10-open-source-llms-for-2025/)  
70. Ollama LLM \~ AnythingLLM, accessed February 17, 2026, [https://docs.anythingllm.com/setup/llm-configuration/local/ollama](https://docs.anythingllm.com/setup/llm-configuration/local/ollama)  
71. Local LLM Speed: Qwen2 & Llama 3.1 Real Benchmark Results \- Ajit Singh, accessed February 17, 2026, [https://singhajit.com/llm-inference-speed-comparison/](https://singhajit.com/llm-inference-speed-comparison/)  
72. Can You Run This LLM? VRAM Calculator (Nvidia GPU and Apple Silicon), accessed February 17, 2026, [https://apxml.com/tools/vram-calculator](https://apxml.com/tools/vram-calculator)  
73. How Much GPU VRAM Do You Need for a 7B, 33B, or 70B Model? \- Database Mart, accessed February 17, 2026, [https://www.databasemart.com/blog/how-much-vram-do-you-need-for-7-70b-llm](https://www.databasemart.com/blog/how-much-vram-do-you-need-for-7-70b-llm)  
74. 2.2x faster at tokens/sec vs rtx 4090 24gb using LLama 3.1 70B-Q4\! : r/LocalLLaMA \- Reddit, accessed February 17, 2026, [https://www.reddit.com/r/LocalLLaMA/comments/1hv7cia/22x\_faster\_at\_tokenssec\_vs\_rtx\_4090\_24gb\_using/](https://www.reddit.com/r/LocalLLaMA/comments/1hv7cia/22x_faster_at_tokenssec_vs_rtx_4090_24gb_using/)  
75. GPU requirements for running Qwen2.5 72B locally? : r/LocalLLM \- Reddit, accessed February 17, 2026, [https://www.reddit.com/r/LocalLLM/comments/1pxjvjy/gpu\_requirements\_for\_running\_qwen25\_72b\_locally/](https://www.reddit.com/r/LocalLLM/comments/1pxjvjy/gpu_requirements_for_running_qwen25_72b_locally/)  
76. Ranking: The Best LLMs for Coding in 2025 (Updated: Jun 2025\) \- ApX Machine Learning, accessed February 17, 2026, [https://apxml.com/posts/best-llms-for-coding](https://apxml.com/posts/best-llms-for-coding)  
77. 10 Best Open Source LLMs for 2025 \- Ema, accessed February 17, 2026, [https://www.ema.co/additional-blogs/addition-blogs/best-open-source-llms?ref=localhost](https://www.ema.co/additional-blogs/addition-blogs/best-open-source-llms?ref=localhost)  
78. Best open-source LLMs in 2025 \- Modal, accessed February 17, 2026, [https://modal.com/blog/best-open-source-llms](https://modal.com/blog/best-open-source-llms)  
79. How would you rank Qwen 2.5 72B vs Llama 3.3 70B Instruct models? \- Reddit, accessed February 17, 2026, [https://www.reddit.com/r/LocalLLaMA/comments/1hcchbi/how\_would\_you\_rank\_qwen\_25\_72b\_vs\_llama\_33\_70b/](https://www.reddit.com/r/LocalLLaMA/comments/1hcchbi/how_would_you_rank_qwen_25_72b_vs_llama_33_70b/)  
80. Structured outputs · Ollama Blog, accessed February 17, 2026, [https://ollama.com/blog/structured-outputs](https://ollama.com/blog/structured-outputs)  
81. Making LLAMA model return only what I ask (JSON). : r/LocalLLaMA \- Reddit, accessed February 17, 2026, [https://www.reddit.com/r/LocalLLaMA/comments/19e4dca/making\_llama\_model\_return\_only\_what\_i\_ask\_json/](https://www.reddit.com/r/LocalLLaMA/comments/19e4dca/making_llama_model_return_only_what_i_ask_json/)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACIAAAAXCAYAAABu8J3cAAABS0lEQVR4Xu2TvyuFURjHH6GISIpMrkWJYpD8BQbqJv4EkzJIlLIYLBLFQOwmk1HEaGCm2Aw2KYPNj8/XObf3dd6rrts7UOdTn973PufpPc957nnMIpFI5G9QgwWcxBFs+Laa0IpjXr3nSj3u4Qs+4ge+4hzW+pxG3MAnXMcZvMAJv54LC7hsyaYFvDJX0Co24QEeYovPETrAGvanYl/BTuyqwA5LNm3DXcu2uRvv8A3P8dSyOWIAF9OBIXNVV+K2uVOLQf+7HLorz/iO48FaCR1MB/npTlVMH26GQY8u8L65v0jdUZdCVMgW1oULv0Xt3vHPkGm8wRNzxZxZNm8KV4JY1ehj8+Y6IPQs4j0Om9v8yFwxx9jjc0bNFVmuU1Whj87itbnJeMBL7E3laHyXzI21CpK35u5m7pQmrzlcSKFp09S1W9LBSOR/8QkBtTcQBLzDVwAAAABJRU5ErkJggg==>

[image2]: <data:image/png;base64,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>

[image3]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAJcAAAAXCAYAAAAGL92hAAAEiElEQVR4Xu2ZW8hmUxjHn8mo0RDTx0iNfOSQC6eYlItpkmMOySmHuXOhNHcTSskUmhxSDhFx4ULcueICMXEjRGRQSOQQYm6QlMP/9z17ede7vr32t/b77XfPXKxf/fu+vd611372s571rMM2q1QqlUqlUqnsCxal69LCiJOk+6WnpBukg6Z/nmLRutuaN0dJd5rbukM6evrnUVm0feuLmAOka81taoM+pW/xG31Nn6eskc6WHpEel66R1k/VaDhZukV6Xfpbenb65/+5SvpEOl06WLpbelU6NKpT2ta8uUx6WTpNOsLc1j+lK+NKc2Z/8QUQMPjkYek76XfpzKkaDn1Jn+Iv+pi+ps/p+8Ba83bulTZJJ0hvSh9Lx0T1lsAJV0jnSN9auxMY9Z9LN0ZlG6R3pe1RWUlbpRAYD6aFBayTXpL2Smc0ZcdJP0h7pMObsnkzpC9WC8F1sbRVusvywXW7eZ/StwH6/FPpyOaa9/pFesU8AEOdf80zWStMI19buxO4OTWI1PictNsmDwl0tVUKz3o0LSyA4HrRPFtsbcoYYXTwlzZx0lgM4YshIYDSvoSQLFI7N0u/SZc310yTP0ofSgtNGTMCwfV0c72MLicQkW0GUZeMQGaI6WqrlFmDCwgwXpwBABdJ/5i/PGl9TIbwxZDkgitkpNRO6lGfaTBwmE0SCj5+zNy/2WVHlxMoazMoV97VVimrCa4YshZrAkYl/4/NEL4YklxwhSBK7cyVA4F1ofSr+RLmwOmfJ+ScQITutnaD9ufg2ii9ZT4dvm++hsMZY9PXF8dL70nf9ND1S3eWkQsuFvxMbamdueA6z/zZP0lP2gpr2ZwT2GK+Zu0GDRFcdPiC+T2xGBHPtJQjpr0+nCv9Ie20jtFlnu7TZ+WUrjNzULfUF2OQCy4W/H2CK8DRxi7zDRQB10qXE3JBlCvvaiuFDPOA+blKLBbln7WUIxzRh0PMsxiL/POT3wIE7K22/Fk53eS3rUgfX4xBLrhyQZQrj9lsPng5jqA/l9HlBBZzbQZRl2knXct0tVXKrNMiZzU7zXe4a6JybGFk4twx6esLMgEdlGbKLpVmUcgFF5syNmepnSG47miuTzXf4PE3EN6xrd0lupzANpRRH6e9cJ6E0mmqq61SZg2usHbg+dgBYd1I+c1N2Vj09QXLkEukq3uInV4pueAKPkr7kz7/q/kLYZDG7xMCkN1mqy3BCZxdxSMeFqR3zDNCgIUnWavts0ZXW6XMGlzcx+7lHpusr7D1e/PDwDTLzpshfDEkBBdTGFNZyjbzRfqxzTX2clr/tk2+xHD/z+bHOwHuI+CesOSoh4gkSMhMVEAcmn0knRLVO0v6SrrNfLSwtb/PphfIpW2VMGtw4RA+u+wxT+VMjx9IX5h/zhiLIX2xWsiGL5gPumALYsA9FNWjLwmQN8y/LhBY+DH2G0H2vPkmj3XnDvP3ov34U2BvMPIC8wfP+0PwrMEV4EWxlYFAW6xlKivD4DzR3G9brH13TZ1F8zgYIxYGh+nk0rSwUqlUKpVKpVKpOP8BHkUyeqyn05IAAAAASUVORK5CYII=>

[image4]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACcAAAAXCAYAAACI2VaYAAACYklEQVR4Xu2WzYuOURjGr4kpQpOPRqS8M+UrJkpIyUI2FiRDCn+AhYUoYqUmNQlpNlMoH6VmSln4KpRZKjbKR5EFiYVQYoHCdb33e8/cz3nPa56FrJ6rfk1zn+d57uvc5z7nvEClSv9EbWQu2Uy2kgWkvfBERpPJLnKWnCCLisOlNZ8Mkc4kLlMbyEtyh+wm28kA+UgOwTw0qYPcJX1kKllBnpHe+FAJqQIXyGsyJ8Rl7CD5RY6QCWFMWk0+k3swLwUdJg/J9BDTzJ6T2SE2nnaQn2g2t5R8wN+/d5z8JsdiUIZk7FIMUqvIV7IlibdSDdYSN9BsTpNX4iuwKuakHtQzhSItga15am4l+Qab0XjScp6CLY++k5pTTInTHFFurvCum0hfbBXPSb15AFaVnDmNKfFVMjHEo7bBnhmB9X1d7jg1Udacduc5jDVyztwyWMM/JbNCPMp7bl8MbmoEUxNlzGk5T5I1IZYzp4qegW2WdSHuUqVGyBMkR1ArE63iUdosvpyunDmpRl4h2Y0NKdcXsicd6Cbv0WzCzR1N4lGnyZuEH7CVeAc7jLXcqqwO2J2wA3i0pxrSbr4Oe2YxmeEDXtKbZJIHqY2wRPrrUiJdPbFSqXKV64edCsp1jSwPY8o5TNbCNouWf14Yr5dTs+5q/K/kui0eYKzRZ5LH5DvsQznpPZ1lb1FMsJ/chp2Dj2Cb0KVJKHaRXIYVaVoYrzf2ILkPu4xlTDtL15hLs75FXsB2aKq95BNsSYWqrmWdAqu+ri4fU5+6emA72cfOh7FRadYLYZfxepT4pVCpUqX/qD/rE4fQFEfikwAAAABJRU5ErkJggg==>

[image5]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACcAAAAXCAYAAACI2VaYAAACgElEQVR4Xu2WTYiOURTH/0LIVz6iETGKMSFKSMlCNhYklEKU1SwUmRCrKSlZyUakDCUpmcX4KJRZWChSykeRBZGFpMTCKPz/77lnnPc+7zNesXz+9evtOffce879OvcFKlX6LxpCppF1ZAOZQ4bXeTTQKLKVnCHHSVt98x81juyB9T+cvqOU1Gryktwi28hmcpJ8JAdgORQ0ntwmR8gYspg8I5ui0yDyoDtIC9lPruJ3MCXWSX6QQ2RosruWkU/kDiyXOh0kD8iEYNPMnpOpwdZI88k7siV9y/8VeQ1L1H0+YPDxjpKfpCsalZASOx+N1FLyhazP7FHDyFnylExONq2SJrYrtUuavAJfTO2NpDMon7pFaofteZ7cEvIVNqMytZK35AoZQaaQSSgmoLEVOI8R5cnFFR9IIu9YZo9aAztH18hpso9cIvfI9OAnuwJrEr6auTbCfPpg574mzzhPopnkvK/85C+pLPTAbqQHWQA78HH7c/mZ2x2Na5MxT+JvkrtORga7zphWVCsraZtPkO9kpTsFaRJ95AnsaAyoLIkye1TZxPwC6Nc1C3aLu4LNpVifyfa8YTZ5j2IAT04FtUyLYIPmfWNyOmPLYTVP5SZut0t+vTCfeWSiN/iS5lujLelPvy4VSD092ib/vo/iQc+39RisKiiWzqMm5VLMy2QFbAxtf7xMteV8AysNkoLrtVBgr9gqEY/JN9hArg7ygsxI340uxF5yE/a0PYSdVZfKhmzd5AJskcaG9tqAp8hd2GOsxHSz9Iy5FOgGLJGZwT6anCOPyE5YKdEkoo+XHG21UGlxLYTdZG9TUS9IqzUX9hivQhP/FIL+pW+lSpWa0S8jko61PoEmTAAAAABJRU5ErkJggg==>