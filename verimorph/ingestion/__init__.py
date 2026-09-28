"""
Multi-Input Ingestion Engine
Supports raw text, PDF, DOCX, web URLs, OCR images, and audio/video transcripts.
"""

from .text_parser import parse_text, TextChunk
from .doc_parser import parse_document
from .url_scraper import scrape_url
from .media_extractor import extract_media_transcript

__all__ = [
    "parse_text",
    "TextChunk",
    "parse_document",
    "scrape_url",
    "extract_media_transcript"
]
