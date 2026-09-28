import os
from pathlib import Path
from typing import Dict, Any
from .text_parser import parse_text

def parse_document(file_path: str) -> Dict[str, Any]:
    """
    Parses PDF, DOCX, or TXT file into text and structured chunks.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = path.suffix.lower()
    extracted_text = ""

    if ext in [".txt", ".md", ".json", ".log"]:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            extracted_text = f.read()

    elif ext == ".pdf":
        try:
            import fitz  # PyMuPDF
            doc = fitz.open(path)
            pages = []
            for page in doc:
                pages.append(page.get_text())
            extracted_text = "\n\n".join(pages)
        except ImportError:
            # Fallback reading
            try:
                import pypdf
                reader = pypdf.PdfReader(str(path))
                extracted_text = "\n\n".join([page.extract_text() or "" for page in reader.pages])
            except ImportError:
                with open(path, "rb") as f:
                    content = f.read()
                    extracted_text = f"[PDF Document parsed as raw stream: {path.name}, bytes: {len(content)}]"

    elif ext in [".docx", ".doc"]:
        try:
            import docx
            doc = docx.Document(path)
            paragraphs = [p.text for p in doc.paragraphs if p.text]
            extracted_text = "\n\n".join(paragraphs)
        except ImportError:
            with open(path, "rb") as f:
                content = f.read()
                extracted_text = f"[DOCX Document parsed as raw stream: {path.name}, bytes: {len(content)}]"

    else:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            extracted_text = f.read()

    parsed = parse_text(extracted_text)
    parsed["source_file"] = path.name
    parsed["source_format"] = ext
    return parsed
