# Source: https://docs.mistral.ai/capabilities/document_ai/document_qna (manual capture)
# Downloaded: 2026-02-16

---

# Document AI QnA

The Document QnA capability combines OCR with large language model capabilities to enable natural language interaction with document content. This allows you to extract information and insights from documents by asking questions in natural language.

> **Tip:** Before continuing, we recommend reading the Chat Completions documentation to learn more about the chat completions API and how to use it before proceeding.

## Before You Start

### Workflow and Capabilities

The workflow consists of two main steps:

1. **Document Processing:** OCR extracts text, structure, and formatting, creating a machine-readable version of the document.
2. **Language Model Understanding:** The extracted document content is analyzed by a large language model. You can ask questions or request information in natural language. The model understands context and relationships within the document and can provide relevant answers based on the document content.

### Key Capabilities
- Question answering about specific document content
- Information extraction and summarization
- Document analysis and insights
- Multi-document queries and comparisons
- Context-aware responses that consider the full document

### Common Use Cases
- Analyzing research papers and technical documents
- Extracting information from business documents
- Processing legal documents and contracts
- Building document Q&A applications
- Automating document-based workflows

## Usage

### Leverage Document QnA

The examples below show how to interact with a PDF document using natural language.

#### QnA with a PDF Url

Be sure the URL is public and accessible by our API.

```python
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
                "text": "what is the last sentence in the document"
            },
            {
                "type": "document_url",
                "document_url": "https://arxiv.org/pdf/1805.04770"
            }
        ]
    }
]

chat_response = client.chat.complete(
    model=model,
    messages=messages
)
```
