import pytest
from verimorph.ingestion import parse_text
from verimorph.brief import generate_content_brief
from verimorph.generators import generate_all_formats, GENERATOR_REGISTRY

def test_generate_all_formats():
    text = "Critical security alert. Active zero-day exploit detected. 1. Patch immediately. 2. Block port 8443."
    parsed = parse_text(text)
    brief = generate_content_brief(parsed)
    deliverables = generate_all_formats(brief)

    expected_keys = [
        "video_package",
        "linkedin_post",
        "twitter_thread",
        "advisory",
        "infographic",
        "executive_summary",
        "presentation_deck"
    ]
    for key in expected_keys:
        assert key in deliverables
        assert "claims" in deliverables[key]

    # Check video package
    assert len(deliverables["video_package"]["scenes"]) >= 3
    assert "srt_subtitles" in deliverables["video_package"]

    # Check presentation deck
    assert len(deliverables["presentation_deck"]["slides"]) == 6
