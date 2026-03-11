# backend/ingestion/image_catalog.py
# Extract and catalog embedded images from PDFs for searchable image references
import os
import logging

logger = logging.getLogger(__name__)


def extract_image_references(pdf_path: str, source: str) -> list[dict]:
    """Extract image context from a PDF for searchable image references.
    
    For each page with images, creates a chunk containing:
    - The surrounding text context (captions, headings)
    - Image metadata (page number, count)
    - type="image_reference" in the payload
    
    This allows RAG to find relevant diagrams/figures when users ask about
    topics that are illustrated in the manual (e.g., "wiring diagram",
    "exploded view", "torque sequence diagram").
    
    Does NOT extract the actual image data — just catalogues what's there
    and indexes the contextual text for search.
    """
    try:
        import fitz  # PyMuPDF
    except ImportError:
        logger.warning("PyMuPDF not available — skipping image catalog")
        return []

    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        logger.error(f"Cannot open PDF for image catalog: {e}")
        return []

    image_chunks = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        images = page.get_images(full=True)
        
        if not images:
            continue
        
        # Get the page text for context
        page_text = page.get_text().strip()
        if not page_text:
            # Image-only page — create a minimal reference
            page_text = f"[Image-only page {page_num + 1}]"
        
        # Look for figure/diagram captions in the text
        captions = _find_captions(page_text)
        
        # Build the searchable context text
        context_parts = []
        if captions:
            context_parts.append("Figures/Diagrams: " + "; ".join(captions))
        
        # Include a summary of the page text (first 500 chars for context)
        text_preview = page_text[:500].strip()
        if text_preview:
            context_parts.append(text_preview)
        
        context_text = "\n\n".join(context_parts) if context_parts else f"Page {page_num + 1} contains {len(images)} image(s)"
        
        image_chunks.append({
            "text": context_text,
            "source": source,
            "page_numbers": [page_num + 1],
            "headings": captions[:2] if captions else [],
            "token_count": len(context_text.split()),  # Rough estimate
            "type": "image_reference",
            "image_count": len(images),
        })
    
    doc.close()
    
    if image_chunks:
        total_images = sum(c["image_count"] for c in image_chunks)
        logger.info(
            f"Image catalog: {len(image_chunks)} pages with images, "
            f"{total_images} total images across {source}"
        )
    
    return image_chunks


def _find_captions(text: str) -> list[str]:
    """Find figure/diagram captions in page text.
    
    Looks for common FSM caption patterns:
    - "Figure X-Y: Description"
    - "Fig. X: Description"  
    - "Diagram X: Description"
    - "FIGURE X-Y DESCRIPTION"
    """
    import re
    
    patterns = [
        r'(?:Figure|Fig\.?|FIGURE)\s+\d+[-.]?\d*[:\s—–-]+([^\n]{5,80})',
        r'(?:Diagram|DIAGRAM)\s+\d+[-.]?\d*[:\s—–-]+([^\n]{5,80})',
        r'(?:Illustration|ILLUSTRATION)\s+\d+[-.]?\d*[:\s—–-]+([^\n]{5,80})',
        r'(?:View|VIEW)\s+[A-Z][-.]?\d*[:\s—–-]+([^\n]{5,80})',
    ]
    
    captions = []
    for pattern in patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            # Get the full match (including "Figure X:") not just the group
            full_match = match.group(0).strip()
            if full_match not in captions:
                captions.append(full_match)
    
    return captions
