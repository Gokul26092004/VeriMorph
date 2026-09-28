import pytest
from verimorph.ingestion import parse_text

def test_parse_text_basic():
    sample_text = "This is a security alert. Remote code execution detected on port 8443.\n\nImmediate patching required."
    result = parse_text(sample_text)
    assert result["total_words"] > 0
    assert result["total_chunks"] >= 1
    assert len(result["chunks"]) >= 1
    assert "chunk_id" in result["chunks"][0]
    assert "char_start" in result["chunks"][0]

def test_parse_empty_text():
    result = parse_text("")
    assert result["total_words"] == 0
    assert result["chunks"] == []
