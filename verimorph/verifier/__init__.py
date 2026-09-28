"""
Claim Verifier & Hallucination Defense Engine
Evaluates factual groundedness against source passages to prevent confabulation.
"""

from .passage_matcher import find_best_matching_chunk, normalize_text
from .groundedness_checker import verify_claims, verify_all_deliverables

__all__ = [
    "find_best_matching_chunk",
    "normalize_text",
    "verify_claims",
    "verify_all_deliverables"
]
