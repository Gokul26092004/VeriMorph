"""
Content Brief Engine
Synthesizes source documents into a unified, reusable ContentBrief data structure.
"""

from .models import ContentBrief, Fact, Entity, ActionItem, KeyMetric
from .brief_generator import generate_content_brief

__all__ = [
    "ContentBrief",
    "Fact",
    "Entity",
    "ActionItem",
    "KeyMetric",
    "generate_content_brief"
]
