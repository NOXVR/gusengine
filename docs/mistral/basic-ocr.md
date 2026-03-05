# Source: https://docs.mistral.ai/capabilities/document_ai/basic_ocr
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
- OCR Processor | Mistral Docs
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

- OCR Processor
- Annotations
- Document QnA
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

# Document AI - OCR Processor

Mistral Document AI API comes with a Document OCR (Optical Character Recognition) processor, powered by our latest OCR model `mistral-ocr-latest`, which enables you to extract text and structured content from PDF documents.

Before You StartCopy section link

# Before You Start

### Key Features

- Extracts text in content while maintaining document structure and hierarchy.

- Preserves formatting like headers, paragraphs, lists and tables.

- Table formatting can be toggled between `null`, `markdown` and `html` via the `table_format` parameter.

- `null`: Tables are returned inline as markdown within the extracted page.

- `markdown`: Tables are returned as markdown tables separately.

- `html`: Tables are returned as html tables separately.

- Option to extract headers and footers via the `extract_header` and the `extract_footer` parameter, when used, the headers and footers content will be provided in the `header` and `footer` fields. By default, headers and footers are considered as part of the main content output.

- Returns results in markdown format for easy parsing and rendering.

- Handles complex layouts including multi-column text and mixed content and returns hyperlinks when available.

- Processes documents at scale with high accuracy

- Supports multiple document formats including:

- `image_url`: png, jpeg/jpg, avif and more...

- `document_url`: pdf, pptx, docx and more...

- For a non-exaustive more comprehensive list, visit our FAQ.

Learn more about our API here.

iInformation
Table formatting as well as header and footer extraction is only available for OCR 2512 or newer.

The OCR processor returns the extracted text content, images bboxes and metadata about the document structure, making it easy to work with the recognized content programmatically.

OCR with Images and PDFsCopy section link

# OCR with Images and PDFs

### OCR your Documents

We provide different methods to OCR your documents. You can either OCR a PDF or an Image.

PDFsCopy section link

## PDFs

Among the PDF methods, you can use a public available URL, a base64 encoded PDF or by uploading a PDF in our Cloud.

OCR with a PDF Url

OCR with a Base64 Encoded PDFOCR with an Uploaded PDFClose
Be sure the URL is public and accessible by our API.

pythontypescriptcurlOutput

import os
from mistralai import Mistral

api_key = os.environ["MISTRAL_API_KEY"]

client = Mistral(api_key=api_key)

ocr_response = client.ocr.process(
    model="mistral-ocr-latest",
    document={
        "type": "document_url",
        "document_url": "https://arxiv.org/pdf/2201.04234"
    },
    table_format="html", # default is None
    # extract_header=True, # default is False
    # extract_footer=True, # default is False
    include_image_base64=True
)

import os
from mistralai import Mistral

api_key = os.environ["MISTRAL_API_KEY"]

client = Mistral(api_key=api_key)

ocr_response = client.ocr.process(
    model="mistral-ocr-latest",
    document={
        "type": "document_url",
        "document_url": "https://arxiv.org/pdf/2201.04234"
    },
    table_format="html", # default is None
    # extract_header=True, # default is False
    # extract_footer=True, # default is False
    include_image_base64=True
)

The output will be a JSON object containing the extracted text content, images bboxes, metadata and other information about the document structure.

{
  "pages": [ # The content of each page
    {
      "index": int, # The index of the corresponding page
      "markdown": str, # The main output and raw markdown content
      "images": list, # Image information when images are extracted
      "tables": list, # Table information when using `table_format=html` or `table_format=markdown`
      "hyperlinks": list, # Hyperlinks detected
      "header": str|null, # Header content when using `extract_header=True`
      "footer": str|null, # Footer content when using `extract_footer=True`
      "dimensions": dict # The dimensions of the page
    }
  ],
  "model": str, # The model used for the OCR
  "document_annotation": dict|null, # Document annotation information when used, visit the Annotations documentation for more information
  "usage_info": dict # Usage information
}

{
  "pages": [ # The content of each page
    {
      "index": int, # The index of the corresponding page
      "markdown": str, # The main output and raw markdown content
      "images": list, # Image information when images are extracted
      "tables": list, # Table information when using `table_format=html` or `table_format=markdown`
      "hyperlinks": list, # Hyperlinks detected
      "header": str|null, # Header content when using `extract_header=True`
      "footer": str|null, # Footer content when using `extract_footer=True`
      "dimensions": dict # The dimensions of the page
    }
  ],
  "model": str, # The model used for the OCR
  "document_annotation": dict|null, # Document annotation information when used, visit the Annotations documentation for more information
  "usage_info": dict # Usage information
}

note
When extracting images and tables they will be replaced with placeholders, such as:

- `![img-0.jpeg](img-0.jpeg)`

- `[tbl-3.html](tbl-3.html)`

You can map them to the actual images and tables by using the `images` and `tables` fields.

ImagesCopy section link

## Images

To perform OCR on an image, you can either pass a URL to the image or directly use a Base64 encoded image.

OCR with an Image URL

OCR with a Base64 encoded ImageClose
You can perform OCR with any public available image as long as a direct url is available.

pythontypescriptcurlOutput

import os
from mistralai import Mistral

api_key = os.environ["MISTRAL_API_KEY"]

client = Mistral(api_key=api_key)

ocr_response = client.ocr.process(
    model="mistral-ocr-latest",
    document={
        "type": "image_url",
        "image_url": "https://raw.githubusercontent.com/mistralai/cookbook/refs/heads/main/mistral/ocr/receipt.png"
    },
    # table_format=None,
    include_image_base64=True
)

import os
from mistralai import Mistral

api_key = os.environ["MISTRAL_API_KEY"]

client = Mistral(api_key=api_key)

ocr_response = client.ocr.process(
    model="mistral-ocr-latest",
    document={
        "type": "image_url",
        "image_url": "https://raw.githubusercontent.com/mistralai/cookbook/refs/heads/main/mistral/ocr/receipt.png"
    },
    # table_format=None,
    include_image_base64=True
)

The output will be a JSON object containing the extracted text content, images bboxes, metadata and other information about the document structure.

{
  "pages": [ # The content of each page
    {
      "index": int, # The index of the corresponding page
      "markdown": str, # The main output and raw markdown content
      "images": list, # Image information when images are extracted
      "tables": list, # Table information when using `table_format=html` or `table_format=markdown`
      "hyperlinks": list, # Hyperlinks detected
      "header": str|null, # Header content when using `extract_header=True`
      "footer": str|null, # Footer content when using `extract_footer=True`
      "dimensions": dict # The dimensions of the page
    }
  ],
  "model": str, # The model used for the OCR
  "document_annotation": dict|null, # Document annotation information when used, visit the Annotations documentation for more information
  "usage_info": dict # Usage information
}

{
  "pages": [ # The content of each page
    {
      "index": int, # The index of the corresponding page
      "markdown": str, # The main output and raw markdown content
      "images": list, # Image information when images are extracted
      "tables": list, # Table information when using `table_format=html` or `table_format=markdown`
      "hyperlinks": list, # Hyperlinks detected
      "header": str|null, # Header content when using `extract_header=True`
      "footer": str|null, # Footer content when using `extract_footer=True`
      "dimensions": dict # The dimensions of the page
    }
  ],
  "model": str, # The model used for the OCR
  "document_annotation": dict|null, # Document annotation information when used, visit the Annotations documentation for more information
  "usage_info": dict # Usage information
}

note
When extracting images and tables they will be replaced with placeholders, such as:

- `![img-0.jpeg](img-0.jpeg)`

- `[tbl-3.html](tbl-3.html)`

You can map them to the actual images and tables by using the `images` and `tables` fields.

OCR at ScaleCopy section link

# OCR at Scale

When performing OCR at scale, we recommend using our Batch Inference service, this allows you to process large amounts of documents in parallel while being more cost-effective than using the OCR API directly. We also support Annotations for structured outputs and other features.

CookbooksCopy section link

# Cookbooks

For more information and guides on how to make use of OCR, we have the following cookbooks:

- Tool Use

- Batch OCR

FAQCopy section link

# FAQ

### Are there any limits regarding the OCR API?

### What document types are supported?

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
