# Source: https://docs.cohere.com/docs/models
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
- An Overview of Cohere's Models | Cohere
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
- What can These Models Be Used For?
- Command
- Using Command Models on Different Platforms
- Embed
- Using Embed Models on Different Platforms
- Rerank
- Using Rerank Models on Different Platforms
- Aya
- Using Aya Models on Different Platforms

Models
# An Overview of Cohere's Models

Copy page

Cohere has a variety of models that cover many different use cases. If you need more customization, you can train a model to tune it to your specific use case.

Cohere models are currently available on the following platforms:

- Cohere’s proprietary platform

- Amazon SageMaker

- Amazon Bedrock

- Microsoft Azure

- Oracle GenAI Service

At the end of each major section below, you’ll find technical details about how to call a given model on a particular platform.

## What can These Models Be Used For?

In this section, we’ll provide some high-level context on Cohere’s offerings, and what the strengths of each are.

- The Command family of models includes Command A, Command R7B, Command A Translate, Command A Reasoning, Command A Vision, Command R+, Command R, and Command

. Together, they are the text-generation LLMs powering tool-using agents, retrieval augmented generation (RAG), translation, copywriting, and similar use cases. They work through the Chat endpoint, which can be used with or without RAG.

- Rerank

 is the fastest way to inject the intelligence of a language model into an existing search system. It can be accessed via the Rerank endpoint.

- Embed

 improves the accuracy of search, classification, clustering, and RAG results. It powers the Embed endpoint.

- The Aya

 family of models are aimed at expanding the number of languages covered by generative AI. Aya Expanse covers 23 languages, and Aya Vision is fully multimodal, allowing you to pass in images and text and get a single coherent response. Both are available on the Chat endpoint.

## Command

Command is Cohere’s default generation model that takes a user instruction (or command) and generates text following the instruction. Our Command models also have conversational capabilities, meaning they are well-suited for chat applications, and Command A Vision can interact with image inputs.

Model NameStatusDescriptionModalityContext LengthMaximum Output TokensEndpoints`command-a-03-2025`LiveCommand A is our most performant model to date, excelling at tool use, agents, retrieval augmented generation (RAG), and multilingual use cases. Command A has a context length of 256K, only requires two GPUs to run, and has 150% higher throughput compared to Command R+ 08-2024.Text256k8kChat`command-r7b-12-2024`Live`command-r7b-12-2024` is a small, fast update delivered in December 2024. It excels at RAG, tool use, agents, and similar tasks requiring complex reasoning and multiple steps.Text128k4kChat`command-a-translate-08-2025`LiveCommand A Translate is Cohere’s state of the art machine translation model, excelling at a variety of translation tasks on 23 languages: English, French, Spanish, Italian, German, Portuguese, Japanese, Korean, Chinese, Arabic, Russian, Polish, Turkish, Vietnamese, Dutch, Czech, Indonesian, Ukrainian, Romanian, Greek, Hindi, Hebrew, Persian.Text8K8kChat`command-a-reasoning-08-2025`LiveCommand A Reasoning is Cohere’s first reasoning model, able to ‘think’ before generating an output in a way that allows it to perform well in certain kinds of nuanced problem-solving and agent-based tasks in 23 languages.Text256k32kChat`command-a-vision-07-2025`LiveCommand A Vision is our first model capable of processing images, excelling in enterprise use cases such as analyzing charts, graphs, and diagrams, table understanding, OCR, document Q&A, and object detection. It officially supports English, Portuguese, Italian, French, German, and Spanish.Text, Images128K8KChat`command-r-08-2024`Live`command-r-08-2024` is an update of the Command R model, delivered in August 2024. Find more information hereText128k4kChat`command-r-plus-08-2024`Live`command-r-plus-08-2024` is an update of the Command R+ model, delivered in August 2024. Find more information hereText128k4kChat`command-r-03-2024`Deprecated Sept 15, 2025Command R is an instruction-following conversational model that performs language tasks at a higher quality, more reliably, and with a longer context than previous models. It can be used for complex workflows like code generation, retrieval augmented generation (RAG), tool use, and agents.Text128k4kChat`command-r-plus-04-2024`Deprecated Sept 15, 2025Command R+ is an instruction-following conversational model that performs language tasks at a higher quality, more reliably, and with a longer context than previous models. It is best suited for complex RAG workflows and multi-step tool use.Text128k4kChat`command-r-plus`Deprecated Sept 15, 2025Alias for `command-r-plus-04-2024`Text128k4kChat`command-r`Deprecated Sept 15, 2025Alias for `command-r-03-2024`Text128k4kChat`command-light`Deprecated Sept 15, 2025A smaller, faster version of `command`. Almost as capable, but a lot faster.Text4k4kChat`command`Deprecated Sept 15, 2025An instruction-following conversational model that performs language tasks with high quality, more reliably and with a longer context than our base generative models.Text4k4kChat

### Using Command Models on Different Platforms

In this table, we provide some important context for using Cohere Command models on Amazon Bedrock, Amazon SageMaker, and more.

Model NameAmazon Bedrock Model IDAmazon SageMakerAzure AI FoundryOracle OCI Generative AI Service`command-a-03-2025`(Coming Soon)Unique per deploymentUnique per deployment`cohere.command-a-03-2025``command-r7b-12-2024`N/AN/AN/AN/A`command-r-plus``cohere.command-r-plus-v1:0`Unique per deploymentUnique per deployment`cohere.command-r-plus v1.2``command-r``cohere.command-r-v1:0`Unique per deploymentUnique per deployment`cohere.command-r-16k v1.2``command``cohere.command-text-v14`N/AN/A`cohere.command v15.6``command-nightly`N/AN/AN/AN/A`command-light``cohere.command-light-text-v14`N/AN/A`cohere.command-light v15.6``command-light-nightly`N/AN/AN/AN/A

## Embed

These models can be used to generate embeddings from text or classify it based on various parameters. Embeddings can be used for estimating semantic similarity between two sentences, choosing a sentence which is most likely to follow another sentence, or categorizing user feedback. The Representation model comes with a variety of helper functions, such as for detecting the language of an input.

Model NameDescriptionModalitiesDimensionsContext LengthSimilarity MetricEndpoints`embed-v4.0`A model that allows for text and images to be classified or turned into embeddingsText, Images, Mixed texts/images (i.e. PDFs)One of ‘[256, 512, 1024, 1536 (default)]‘128kCosine Similarity, Dot Product Similarity, Euclidean DistanceEmbed,  
Embed Jobs`embed-english-v3.0`A model that allows for text to be classified or turned into embeddings. English only.Text, Images1024512Cosine SimilarityEmbed,  
Embed Jobs`embed-english-light-v3.0`A smaller, faster version of `embed-english-v3.0`. Almost as capable, but a lot faster. English only.Text, Images384512Cosine SimilarityEmbed,  
Embed Jobs`embed-multilingual-v3.0`Provides multilingual classification and embedding support. See supported languages here.Text, Images1024512Cosine SimilarityEmbed, Embed Jobs`embed-multilingual-light-v3.0`A smaller, faster version of `embed-multilingual-v3.0`. Almost as capable, but a lot faster. Supports multiple languages.Text, Images384512Cosine SimilarityEmbed,  
Embed Jobs

### Using Embed Models on Different Platforms

In this table, we provide some important context for using Cohere Embed models on Amazon Bedrock, Amazon SageMaker, and more.

Model NameAmazon Bedrock Model IDAmazon SageMakerAzure AI FoundryOracle OCI Generative AI Service`embed-v4.0`(Coming Soon)Unique per deployment`cohere-embed-v-4-plan`(Coming Soon)`embed-english-v3.0``cohere.embed-english-v3`Unique per deploymentUnique per deployment`cohere.embed-english-image-v3.0` (for images), `cohere.embed-english-v3.0` (for text)`embed-english-light-v3.0`N/AUnique per deploymentN/A`cohere.embed-english-light-image-v3.0` (for images), `cohere.embed-english-light-v3.0` (for text)`embed-multilingual-v3.0``cohere.embed-multilingual-v3`Unique per deploymentUnique per deployment`cohere.embed-multilingual-image-v3.0` (for images), `cohere.embed-multilingual-v3.0` (for text)`embed-multilingual-light-v3.0`N/AUnique per deploymentN/A`cohere.embed-multilingual-light-image-v3.0` (for images), `cohere.embed-multilingual-light-v3.0` (for text)`embed-english-v2.0`N/AUnique per deploymentN/AN/A`embed-english-light-v2.0`N/AUnique per deploymentN/A`cohere.embed-english-light-v2.0``embed-multilingual-v2.0`N/AUnique per deploymentN/AN/A

## Rerank

The Rerank model can improve created models by re-organizing their results based on certain parameters. This can be used to improve search algorithms.

Model NameDescriptionModalitiesContext LengthEndpoints`rerank-v4.0-pro`A multilingual model that allows for re-ranking English and non-english documents and semi-structured data (JSON). This model is better suited for state-of-the-art quality and complex use-cases than its `fast` variant.Text32kRerank`rerank-v4.0-fast`A light version of `rerank-v4.0-pro`, this is a multilingual model that allows for re-ranking English and non-english documents and semi-structured data (JSON). This model is better suited for low latency and high throughput use-cases than its `pro` variant.Text32kRerank`rerank-v3.5`A model that allows for re-ranking English Language documents and semi-structured data (JSON). This model has a context length of 4096 tokens.Text4kRerank`rerank-english-v3.0`A model that allows for re-ranking English Language documents and semi-structured data (JSON). This model has a context length of 4096 tokens.Text4kRerank`rerank-multilingual-v3.0`A model for documents and semi-structure data (JSON) that are not in English. Supports the same languages as `embed-multilingual-v3.0`. This model has a context length of 4096 tokens.Text4kRerank

### Using Rerank Models on Different Platforms

In this table, we provide some important context for using Cohere Rerank models on Amazon Bedrock, SageMaker, and more.

Model NameAmazon Bedrock Model IDAmazon SageMakerAzure AI FoundryOracle OCI Generative AI Service`rerank-v4.0-pro`N/AUnique per deployment`cohere-rerank-v4-pro`N/A`rerank-v4.0-fast`N/AUnique per deployment`cohere-rerank-v4-fast`N/A`rerank-v3.5``cohere.rerank-v3-5:0`Unique per deployment`Cohere-rerank-v3.5``cohere.rerank.3-5``rerank-english-v3.0`N/AUnique per deployment`Cohere-rerank-v3-english`N/A`rerank-multilingual-v3.0`N/AUnique per deployment`Cohere-rerank-v3-multilingual`N/A

Rerank accepts full strings rather than tokens, so the token limit works a little differently. Rerank will automatically chunk documents longer than 510 tokens, and there is therefore no explicit limit to how long a document can be when using rerank. See our best practice guide for more info about formatting documents for the Rerank endpoint.

## Aya

Aya

 is a family of multilingual large language models designed to expand the number of languages covered by generative AI for purposes of research and to better-serve minority linguistic communities.

Its 8-billion and 32-billion parameter “Expanse” offerings are optimized to perform well in these 23 languages: Arabic, Chinese (simplified & traditional), Czech, Dutch, English, French, German, Greek, Hebrew, Hebrew, Hindi, Indonesian, Italian, Japanese, Korean, Persian, Polish, Portuguese, Romanian, Russian, Spanish, Turkish, Ukrainian, and Vietnamese.

Its 8-billion and 32-billion parameter “Vision” models are state-of-the-art multimodal models excelling at a variety of critical benchmarks for language, text, and image capabilities.

Model NameDescriptionModalityContext LengthMaximum Output TokensEndpoints`c4ai-aya-expanse-8b`Aya Expanse is a highly performant 8B multilingual model, designed to rival monolingual performance through innovations in instruction tuning with data arbitrage, preference training, and model merging. Serves 23 languages.Text8k4kChat`c4ai-aya-expanse-32b`Aya Expanse is a highly performant 32B multilingual model, designed to rival monolingual performance through innovations in instruction tuning with data arbitrage, preference training, and model merging. Serves 23 languages.Text128k4kChat`c4ai-aya-vision-8b`Aya Vision is a state-of-the-art multimodal model excelling at a variety of critical benchmarks for language, text, and image capabilities. This 8 billion parameter variant is focused on low latency and best-in-class performance.Text, Images16k4kChat`c4ai-aya-vision-32b`Aya Vision is a state-of-the-art multimodal model excelling at a variety of critical benchmarks for language, text, and image capabilities. Serves 23 languages. This 32 billion parameter variant is focused on state-of-art multilingual performance.Text, Images16k4kChat

### Using Aya Models on Different Platforms

Aya isn’t available on other platforms, but it can be used with WhatsApp. Find more information here.
Was this page helpful?

Yes

No

Edit this pageBuilt with

docsv2 API

v2 API

DASHBOARDPLAYGROUNDDOCSCOMMUNITYLOG IN
