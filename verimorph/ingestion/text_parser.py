import re
from typing import List, Dict, Any
from pydantic import BaseModel

class TextChunk(BaseModel):
    chunk_id: int
    text: str
    word_count: int
    char_start: int
    char_end: int

def parse_text(raw_text: str, chunk_size_words: int = 120) -> Dict[str, Any]:
    """
    Parses raw text into clean paragraphs and indexable chunks with character spans.
    """
    if not raw_text or not raw_text.strip():
        return {
            "title": "Untitled Input",
            "content": "",
            "chunks": [],
            "total_words": 0,
            "total_chunks": 0
        }

    cleaned = raw_text.strip()
    lines = cleaned.splitlines()
    
    # Try to derive title from the first non-empty line
    title = "Content Document"
    for line in lines:
        stripped = line.strip().strip("#").strip()
        if stripped:
            title = stripped[:80]
            break

    # Paragraph-based chunking
    paragraphs = [p.strip() for p in re.split(r'\n\s*\n', cleaned) if p.strip()]
    
    chunks: List[TextChunk] = []
    chunk_id = 1
    current_offset = 0

    for para in paragraphs:
        words = para.split()
        if len(words) <= chunk_size_words:
            char_start = cleaned.find(para, current_offset)
            if char_start == -1:
                char_start = current_offset
            char_end = char_start + len(para)
            current_offset = char_end

            chunks.append(TextChunk(
                chunk_id=chunk_id,
                text=para,
                word_count=len(words),
                char_start=char_start,
                char_end=char_end
            ))
            chunk_id += 1
        else:
            # Sub-divide large paragraphs
            for i in range(0, len(words), chunk_size_words):
                sub_words = words[i:i + chunk_size_words]
                sub_text = " ".join(sub_words)
                char_start = cleaned.find(sub_text, current_offset)
                if char_start == -1:
                    char_start = current_offset
                char_end = char_start + len(sub_text)
                current_offset = char_end

                chunks.append(TextChunk(
                    chunk_id=chunk_id,
                    text=sub_text,
                    word_count=len(sub_words),
                    char_start=char_start,
                    char_end=char_end
                ))
                chunk_id += 1

    total_words = len(cleaned.split())

    return {
        "title": title,
        "content": cleaned,
        "chunks": [c.model_dump() for c in chunks],
        "total_words": total_words,
        "total_chunks": len(chunks)
    }
