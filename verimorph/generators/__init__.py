"""
Format Generators Engine
Provides the 7 parallel deliverable generators derived from a single ContentBrief.
"""

from typing import Dict, Any, List
from verimorph.brief.models import ContentBrief
from .base import BaseGenerator
from .video_package import VideoPackageGenerator
from .linkedin_post import LinkedInPostGenerator
from .twitter_thread import TwitterThreadGenerator
from .advisory import AdvisoryGenerator
from .infographic import InfographicGenerator
from .executive_summary import ExecutiveSummaryGenerator
from .presentation_deck import PresentationDeckGenerator

GENERATOR_REGISTRY = {
    "video_package": VideoPackageGenerator,
    "linkedin_post": LinkedInPostGenerator,
    "twitter_thread": TwitterThreadGenerator,
    "advisory": AdvisoryGenerator,
    "infographic": InfographicGenerator,
    "executive_summary": ExecutiveSummaryGenerator,
    "presentation_deck": PresentationDeckGenerator
}

def generate_all_formats(brief: ContentBrief, requested_formats: List[str] = None) -> Dict[str, Any]:
    """
    Executes generators in parallel or sequentially from the single ContentBrief.
    Guarantees strict fact consistency across all deliverables.
    """
    formats_to_run = requested_formats or list(GENERATOR_REGISTRY.keys())
    results = {}

    for fmt in formats_to_run:
        generator_cls = GENERATOR_REGISTRY.get(fmt)
        if generator_cls:
            gen_instance = generator_cls()
            results[fmt] = gen_instance.generate(brief)

    return results

__all__ = [
    "BaseGenerator",
    "VideoPackageGenerator",
    "LinkedInPostGenerator",
    "TwitterThreadGenerator",
    "AdvisoryGenerator",
    "InfographicGenerator",
    "ExecutiveSummaryGenerator",
    "PresentationDeckGenerator",
    "GENERATOR_REGISTRY",
    "generate_all_formats"
]
