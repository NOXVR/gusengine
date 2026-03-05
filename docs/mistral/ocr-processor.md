# Source: https://docs.mistral.ai/capabilities/document_ai/basic_ocr (manual capture)
# Downloaded: 2026-02-16

---

# Document AI - OCR Processor

Mistral Document AI API comes with a Document OCR (Optical Character Recognition) processor, powered by our latest OCR model `mistral-ocr-latest`, which enables you to extract text and structured content from PDF documents.

## Before You Start

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

> **Note:** Table formatting as well as header and footer extraction is only available for OCR 2512 or newer.

The OCR processor returns the extracted text content, images bboxes and metadata about the document structure, making it easy to work with the recognized content programmatically.

## OCR with Images and PDFs

We provide different methods to OCR your documents. You can either OCR a PDF or an Image.

### PDFs

Among the PDF methods, you can use a public available URL, a base64 encoded PDF or by uploading a PDF in our Cloud.

#### OCR with a PDF Url

Be sure the URL is public and accessible by our API.

```python
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
```

#### Output Structure

```json
{
  "pages": [
    {
      "index": "int",
      "markdown": "str",
      "images": "list",
      "tables": "list",
      "hyperlinks": "list",
      "header": "str|null",
      "footer": "str|null",
      "dimensions": "dict"
    }
  ],
  "model": "str",
  "document_annotation": "dict|null",
  "usage_info": "dict"
}
```

> **Note:** When extracting images and tables they will be replaced with placeholders, such as:
> `![img-0.jpeg](img-0.jpeg)` and `[tbl-3.html](tbl-3.html)`
> You can map them to the actual images and tables by using the `images` and `tables` fields.

### Images

To perform OCR on an image, you can either pass a URL to the image or directly use a Base64 encoded image.

#### OCR with an Image URL

```python
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
```

The output follows the same JSON structure as the PDF output above.

## OCR at Scale

When performing OCR at scale, we recommend using our Batch Inference service, this allows you to process large amounts of documents in parallel while being more cost-effective than using the OCR API directly. We also support Annotations for structured outputs and other features.

## Cookbooks
- Tool Use
- Batch OCR

## FAQ

### Are there any limits regarding the OCR API?
Yes, there are certain limitations for the OCR API. Uploaded document files must not exceed **50 MB** in size and should be no longer than **1,000 pages**.

### What document types are supported?

| Documents | Images |
|-----------|--------|
| PDF (.pdf) | JPEG (.jpg, .jpeg) |
| Word Documents (.docx) | PNG (.png) |
| PowerPoint (.pptx) | AVIF (.avif) |
| Text Files (.txt) | TIFF (.tiff) |
| EPUB (.epub) | GIF (.gif) |
| XML/DocBook (.xml) | HEIC/HEIF (.heic, .heif) |
| RTF (.rtf) | BMP (.bmp) |
| OpenDocument Text (.odt) | WebP (.webp) |
| BibTeX/BibLaTeX (.bib) | |
| FictionBook (.fb2) | |
| Jupyter Notebooks (.ipynb) | |
| JATS XML (.xml) | |
| LaTeX (.tex) | |
| OPML (.opml) | |
| Troff (.1, .man) | |
