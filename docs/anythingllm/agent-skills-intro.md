# Source: https://docs.anythingllm.com/agent/custom/introduction
# Downloaded: 2026-02-16

---

Introduction to custom agent skills ~ AnythingLLM
- 
- 
- 
- 
- 🚀 AnythingLLM v1.10.0 is live! Update now →

- ▲ Home
- AnythingLLM Roadmap
- Getting Started
- Introduction
- Feature Overview

- All Features
- AI Agents
- Private Browser Tool
- API Access
- Appearance Customization
- Chat Logs
- Chat Modes
- Embedded Chat Widgets
- Event Logs
- Embedding Models
- Language Models
- Transcription Models
- Vector Database
- Security & Access
- Privacy & Data Handling
- System Prompt Variables
- AnythingLLM Setup

- Embedder Setup

- Overview
- Local

- AnythingLLM Default
- LM Studio
- Local AI
- Ollama
- Cloud

- OpenAI
- Azure OpenAI
- Cohere
- LLM Setup

- Overview
- Local

- AnythingLLM Default
- LM Studio
- Local AI
- Ollama
- KobaldCPP
- Cloud

- Anthropic
- Azure OpenAI
- AWS Bedrock
- Cohere
- Google Gemini
- Groq
- Hugging Face
- Mistral AI
- OpenAI
- OpenAI (generic)
- OpenRouter
- Perplexity AI
- Together AI
- TrueFoundry
- APIpie
- Transcription Setup

- Overview
- Local

- AnythingLLM Default
- Cloud

- OpenAI
- Vector DB Setup

- Overview
- Local

- LanceDB
- Chroma
- Milvus
- Cloud

- AstraDB
- Pinecone
- QDrant
- Weaviate
- Zilliz
- Chat Interface overview
- Other configurations
- AnythingLLM Community Hub
- What is the Community Hub?
- Importing an item
- Uploading an item
- FAQ
- Installation Guides
- AnythingLLM Desktop

- Overview
- System Requirements
- Install for MacOS
- Install for Windows
- Install for Linux
- Desktop FAQ
- Update AnythingLLM
- Where is my data stored?
- Debugging & Logs
- Uninstall AnythingLLM
- Legal & Privacy
- Privacy Policy
- Terms of Use
- AnythingLLM Self-hosted

- Overview
- Docker Images
- System Requirements
- Quickstart
- Local Docker
- Deploy to Cloud VM
- Docker FAQ
- Connecting to localhost
- Debugging & Logs
- AnythingLLM Cloud

- Overview
- Limitations
- 502 Error on AnythingLLM Hosted
- Terms & Conditions
- Terms & Conditions
- Privacy Policy
- AnythingLLM Mobile

- Introduction
- Legal & Privacy
- Terms of Service
- Privacy Policy
- Guides
- MCP Compatibility

- Overview
- MCP on Docker
- MCP on Desktop
- Agent Flows

- What is an Agent Flow?
- Getting Started with Flows
- Tutorial: HackerNews Flow
- All about blocks

- Web Scraper
- API Call
- LLM Instruction
- Read File
- Write File
- Debugging flows
- Using AI Agents

- Overview
- Setup
- Usage
- Custom Skills

- Introduction
- Developer Guide
- plugin.json reference
- handler.js reference
- Importing custom models
- Browser Extension

- Install the AnythingLLM Browser Extension
- Meeting Assistant

- Introduction
- Features
- Frequently Asked Questions
- Using Documents in Chat

- Attaching vs RAG
- RAG in AnythingLLM
- AI Agent not using tools!
- Ollama Connection Debugging
- Fetch failed error on embed
- Manual QNN Model Download
- More
- Beta Previews

- What are beta previews?
- Enable feature previews
- Available previews

- Live document sync
- AI Computer use
- Desktop Changelogs

- Overview
- v1.10.0
- v1.9.1
- v1.9.0
- v1.8.5
- v1.8.4
- v1.8.3
- v1.8.2
- v1.8.1
- v1.8.0
- v1.7.8
- v1.7.7
- v1.7.6
- v1.7.5
- v1.7.4
- v1.7.3
- v1.7.2
- v1.7.1
- v1.7.0
- v1.6.11
- v1.6.10
- v1.6.9
- v1.6.8
- v1.6.7
- v1.6.6
- v1.6.5
- v1.6.4
- v1.6.3
- v1.6.2
- v1.6.1
- v1.6.0
- Contribute
- Community Hub

- FAQ
- Importing from the AnythingLLM Community Hub
- Uploading to the AnythingLLM Community Hub
- What is the Community Hub?
- Support
Light

Using AI Agents
Custom Skills
Introduction⚠️
Warning: Only run custom agent skills you trust.

Custom agent skills are a powerful feature of AnythingLLM, but they can also be dangerous if misused.

Always make sure to test your skills thoroughly before using them in a production environment & never install untrusted code on any machine.

# Introduction to custom agent skills

AnythingLLM allows you to create custom agent skills that can be used to extend the capabilities of your `@agent` invocations. These skills can be anything you want from a simple API call to even operating-system invocations.

The sky is the limit! Depending on how you run AnythingLLM, you can create custom agent skills that can run extra processes like running a local Python script or, on Desktop, even operating-system invocations.

If it can be done in NodeJS, it can likely be done in AnythingLLM.

## The current state of custom agent skills

️💡
Custom agent skills are newly supported in AnythingLLM and may have some bugs, quirks, missing features, unsupported features, etc.

Please report any feature requests or bugs you find to the GitHub repository (opens in a new tab).

- NodeJS programming experience is required to create custom agent skills. Go to the developer guide to get started.

- Custom agent skills must exactly match the requirements listed on this help page.

- There are built in functions and utilities to help you log data or thoughts for an agent.

- There is currently no established tooling for creating custom agent skills - so follow this guide if developing skills for AnythingLLM.

- All skills must return a `string` type response - anything else may break the agent invocation.

## Availability

Custom agent skills are available in the Docker image since commit `d1103e` (opens in a new tab) or release v1.2.2 (opens in a new tab).

Custom agent skills are available in AnythingLLM Desktop version 1.6.5 and later.

Custom agent skills are not available in the AnythingLLM Cloud offering.

## View loaded custom agent skills

You can view the loaded custom agent skills by opening the `Agent Skills` tab in the settings of AnythingLLM.

Any valid custom agent skills loaded into AnythingLLM will be displayed here.

See where to place your custom agent skills for more information.

## Dynamic UI of custom agent skills

Custom agent skills can also have a dynamic UI inputs associated with them. This is useful for providing runtime arguments to your custom agent skills or configurable properties of them.

See how the dynamic UI for a custom agent skill is setup via the `plugin.json` file.

UsageDeveloper Guide

LightMIT 2026 © Mintplex Labs.
