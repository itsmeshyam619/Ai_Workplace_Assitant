"""
Document reader and chunking utilities.

Assumptions and choices:
- Chunking is done by characters with overlap. We use ~1500-char chunks with 200-char overlap.
- This is a simple heuristic approximating 300-500 tokens.
- Text extraction uses PyPDF2 for PDF, python-docx for DOCX, and raw decode for TXT.
"""
from typing import List
from io import BytesIO
from PyPDF2 import PdfReader
import docx


def extract_text_from_pdf_bytes(data: bytes) -> str:
    reader = PdfReader(BytesIO(data))
    texts = []
    for page in reader.pages:
        try:
            texts.append(page.extract_text() or "")
        except Exception:
            continue
    return "\n".join(texts)


def extract_text_from_docx_bytes(data: bytes) -> str:
    bio = BytesIO(data)
    document = docx.Document(bio)
    paragraphs = [p.text for p in document.paragraphs]
    return "\n".join(paragraphs)


def extract_text_from_txt_bytes(data: bytes) -> str:
    return data.decode("utf-8", errors="ignore")


def extract_text_from_file(filename: str, data: bytes) -> str:
    lower = filename.lower()
    if lower.endswith(".pdf"):
        return extract_text_from_pdf_bytes(data)
    elif lower.endswith(".docx"):
        return extract_text_from_docx_bytes(data)
    elif lower.endswith(".txt"):
        return extract_text_from_txt_bytes(data)
    else:
        raise ValueError("Unsupported file type")


def chunk_text(text: str, chunk_size: int = 1500, overlap: int = 200) -> List[str]:
    """Chunk text into overlapping character chunks.

    chunk_size: number of characters per chunk (heuristic for ~300-500 tokens)
    overlap: overlapping characters between chunks
    """
    if not text:
        return []
    text = text.replace("\r", "")
    chunks = []
    start = 0
    length = len(text)
    while start < length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk.strip())
        if end >= length:
            break
        start = end - overlap
    return [c for c in chunks if c]
