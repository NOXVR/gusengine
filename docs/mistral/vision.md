# Source: https://docs.mistral.ai/capabilities/vision
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
- Vision | Mistral Docs
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

# Vision

Vision capabilities enable models to analyze images and provide insights based on visual content in addition to text. This multimodal approach opens up new possibilities for applications that require both textual and visual understanding.

We provide a variety of models with vision capabilities, all available via the Chat Completions API.

tip
For more specific use cases regarding Document Parsing, OCR and Data Extraction we recommend taking a look at our Document AI stack here.

Before You StartCopy section link

# Before You Start

### Recommended Models with Vision Capabilities

- Mistral Large 3 via `mistral-large-2512`

- Mistral Medium 3.1 via `mistral-medium-2508`

- Mistral Small 3.2 via `mistral-small-2506`

- Ministral 3:

- Ministral 3 14B via `ministral-14b-2512`

- Ministral 3 8B via `ministral-8b-2512`

- Ministral 3 3B via `ministral-3b-2512`

Sending an ImageCopy section link

# Sending an Image

### Use Vision Models

There are two ways to send an image to the Chat Completions API, either by passing a URL or by passing a base64 encoded image.

tip
Before continuing, we recommend reading the Chat Competions documentation to learn more about the chat completions API and how to use it before proceeding.

Passing an Image URL

Passing a Base64 Encoded ImageClose
If the image is hosted online, you can simply provide the publicaly accessible URL of the image in the request. This method is straightforward and does not require any encoding.

pythontypescriptcurlOutput

import os
from mistralai import Mistral

api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-small-latest"

client = Mistral(api_key=api_key)

messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "What's in this image?"
            },
            {
                "type": "image_url",
                "image_url": "https://docs.mistral.ai/img/eiffel-tower-paris.jpg"
            }
        ]
    }
]

chat_response = client.chat.complete(
    model=model,
    messages=messages
)

import os
from mistralai import Mistral

api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-small-latest"

client = Mistral(api_key=api_key)

messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "What's in this image?"
            },
            {
                "type": "image_url",
                "image_url": "https://docs.mistral.ai/img/eiffel-tower-paris.jpg"
            }
        ]
    }
]

chat_response = client.chat.complete(
    model=model,
    messages=messages
)

Use casesCopy section link

# Use cases

Below you can find a few examples of use cases leveraging our models vision, from understanding graphs to extract data, the use cases are diverse.

note
These are simple examples you can use as inspiration to build your own use cases, for OCR and Structured Outputs, we recommend leveraging Document AI and Document AI Annotations.

ChartsCompare imagesTranscribeOCR Old DocumentsOCR with Structured output
¡Meow! Click one of the tabs above to learn more.

FAQCopy section link

# FAQ

### What is the price per image?

### How many tokens correspond to an image and/or what is the maximum resolution?

### Can I fine-tune the image capabilities?

### Can I use them to generate images?

### What types of image files are supported?

### Is there a limit to the size of the image?

### What's the maximum number images per request?

### What is the rate limit?

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
