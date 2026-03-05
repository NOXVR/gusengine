# Source: https://docs.cohere.com/docs/rate-limits
# Downloaded: 2026-02-16

---

- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- Different Types of API Keys and Rate Limits | Cohere
- 
- 
- 
Search/Ask AI

- 
- 
- Guides and conceptsAPI ReferenceRelease NotesLLMUCookbooks
Search/Ask AI

Guides and concepts
API Reference
Release Notes
LLMU
Cookbooks
- Get Started
- Introduction
- Installation
- Creating a client
- Quickstart

- Playground
- FAQs
- Models
- An Overview of Cohere's Models
- Command

- Embed
- Rerank
- Aya

- Text Generation
- Introduction to Text Generation at Cohere
- Using the Chat API
- Reasoning
- Image Inputs
- Streaming Responses
- Structured Outputs

- Predictable Outputs
- Advanced Generation Parameters
- Retrieval Augmented Generation (RAG)

- Tool Use

- Tokens and Tokenizers
- Summarizing Text
- Safety Modes
- Embeddings (Vectors, Search, Retrieval)
- Introduction to Embeddings at Cohere
- Semantic Search with Embeddings
- Multimodal Embeddings
- Batch Embedding Jobs
- Reranking

- Going to Production
- API Keys and Rate Limits
- Going Live
- Deprecations
- How Does Cohere's Pricing Work?
- Integrations
- Integrating Embedding Models with Other Tools

- Cohere and LangChain

- LlamaIndex and Cohere
- Deployment Options
- Overview
- SDK Compatibility
- Private Deployment

- Cloud AI Services

- Model Vault

- Tutorials
- Cookbooks
- LLM University
- Build Things with Cohere!

- Agentic RAG

- Cohere on Azure

- Responsible Use
- Security

- Usage Policy
- Command A Technical Report

- Command R and Command R+ Model Card
- Cohere Labs
- Cohere Labs Acceptable Use Policy
- More Resources
- Cohere Toolkit
- Datasets
- Improve Cohere Docs

LightOn this page
- Chat API (per model)
- Other API Endpoints

Going to Production
# Different Types of API Keys and Rate Limits

Copy page

Cohere offers two kinds of API keys: evaluation keys (free but limited in usage), and production keys (paid and much less limited in usage). You can create a trial or production key on the API keys page

. For more details on pricing please see our pricing docs.

Prod keys work like trial keys for newer model variants such as Command A Reasoning. Please contact sales@cohere.com

 if you intend to use those models in production.

Trial keys (and prod keys on newer Chat model variants) are limited to 1,000 API calls a month.

## Chat API (per model)

ModelTrial rate limitProduction rate limitCommand A Reasoning20 req / minContact sales@cohere.com

Command A Translate20 req / minContact sales@cohere.com

Command A Vision20 req / minContact sales@cohere.com

Command A20 req / min500 req / minCommand R+20 req / min500 req / minCommand R20 req / min500 req / minCommand R7B20 req / min500 req / min

## Other API Endpoints

EndpointTrial rate limitProduction rate limitEmbed2,000 inputs / min2,000 inputs / minEmbed (Images)5 inputs / min400 inputs / minRerank10 req / min1,000 req / minTokenize100 req / min2,000 req / minEmbedJob5 req / min50 req / minDefault (anything not covered above)500 req / min500 req / min

If you have any questions or want to speak about getting a rate limit increase, reach out to support@cohere.com

.
Was this page helpful?

Yes

No

Edit this pageBuilt with

docsv2 API

v2 API

DASHBOARDPLAYGROUNDDOCSCOMMUNITYLOG IN
