# Source: https://docs.mistral.ai/getting-started/clients
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
- SDK Clients | Mistral Docs
- 
- 
- 
- 
- 
Docs & API

Search docs⌘K

Toggle themeReach outTry Studio 

Search docs⌘KGetting Started
- Introduction
- Models

- Quickstart
- SDK Clients
- Model Customization
- Glossary
- ChangelogCapabilities
- Chat Completions

- Vision
- Audio & Transcription
- Reasoning
- Document AI

- Coding
- Embeddings

- Function Calling
- Citations & References
- Structured Outputs

- Moderation & Guardrailing
- Fine-Tuning

- Batch Inference
- Predicted outputsAgents
- Agents Introduction
- Agents & Conversations
- Tools

- HandoffsDeployment
- AI Studio

- Cloud

- Self-Deployment
Mistral Vibe
- CLI Introduction

- Agents & Skills
- Offline / Local
- Mistral AI Crawlers

Copy markdown

# SDK Clients

SDK Clients allow you to interact with Mistral AI's API in your preferred programming language, they implement clean and simple interfaces to our API endpoints and services.

We strongly recommend using the official SDKs to interact with our APIs.

SDKsCopy section link

# SDKs

We provide official SDK clients in both Python and Typescript, you can also find third-party non-official SDKs in other languages.

Python SDK

Typescript SDKThird-party SDKsClose
You can install our Python Client by running:

Bash

`pip install mistralai`

`pip install mistralai`

Once installed, you can for example run the chat completion as follows:

pythonOutput

import os
from mistralai import Mistral

api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-medium-latest"

client = Mistral(api_key=api_key)

chat_response = client.chat.complete(
    model = model,
    messages = [
        {
            "role": "user",
            "content": "What is the best French cheese?",
        },
    ]
)

import os
from mistralai import Mistral

api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-medium-latest"

client = Mistral(api_key=api_key)

chat_response = client.chat.complete(
    model = model,
    messages = [
        {
            "role": "user",
            "content": "What is the best French cheese?",
        },
    ]
)

See more examples here.
Go to Top

### WHY MISTRAL
About usOur customersCareersContact us
### EXPLORE
AI SolutionsPartnersResearch
### DOCUMENTATION
DocumentationContributingCookbooks
### BUILD
AI StudioLe ChatMistral CodeMistral ComputeTry the API
### LEGAL
Terms of servicePrivacy policyLegal noticePrivacy ChoicesBrand
### COMMUNITY
Discord↗X↗Github↗LinkedIn↗Ambassador
Mistral AI © 2026

Toggle theme
