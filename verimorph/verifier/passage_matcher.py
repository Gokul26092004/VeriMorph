import re
from typing import List, Dict, Any, Tuple

def normalize_text(text: str) -> set:
    """Tokenize and normalize text to lowercase alphanumeric word set."""
    words = re.findall(r'\b\w+\b', text.lower())
    # Exclude common stop words for high-fidelity semantic overlap
    stop_words = {
        "the", "a", "an", "and", "or", "in", "on", "at", "to", "for", "with", "by", "of",
        "is", "are", "was", "were", "be", "been", "that", "this", "it", "as", "from"
    }
    return {w for w in words if w not in stop_words and len(w) > 2}

def find_best_matching_chunk(claim: str, chunks: List[Dict[str, Any]]) -> Tuple[Dict[str, Any], float]:
    """
    Finds the source text chunk with highest lexical and semantic alignment to the claim.
    Returns (best_chunk, confidence_score).
    """
    claim_tokens = normalize_text(claim)
    if not claim_tokens:
        return (chunks[0] if chunks else {}, 0.0)

    best_score = 0.0
    best_chunk = chunks[0] if chunks else {}

    for chunk in chunks:
        chunk_text = chunk.get("text", "")
        chunk_tokens = normalize_text(chunk_text)
        if not chunk_tokens:
            continue

        overlap = claim_tokens.intersection(chunk_tokens)
        
        # Jaccard / containment overlap
        containment_score = len(overlap) / len(claim_tokens)
        
        # Boost for exact entity or keyword preservation (e.g. CVE, IPs, ports, versions)
        exact_boost = 0.0
        cves = re.findall(r'CVE-\d{4}-\d+', claim, re.IGNORECASE)
        for cve in cves:
            if cve.lower() in chunk_text.lower():
                exact_boost += 0.25

        ips = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', claim)
        for ip in ips:
            if ip in chunk_text:
                exact_boost += 0.25

        score = min(1.0, containment_score + exact_boost)

        if score > best_score:
            best_score = score
            best_chunk = chunk

    return (best_chunk, round(best_score, 3))
