import pytest
from verimorph.ingestion import parse_text
from verimorph.brief import generate_content_brief

def test_generate_content_brief():
    text = (
        "CERT-In CYBER SECURITY ADVISORY\n"
        "Active Exploitation of CVE-2026-4419 on SecureGate appliances.\n"
        "Remediation:\n"
        "1. Apply vendor firmware emergency patch v5.8.2 immediately.\n"
        "2. Block UDP port 8443 on firewall perimeter."
    )
    parsed = parse_text(text)
    brief = generate_content_brief(parsed)
    assert brief.brief_id.startswith("BRIEF-")
    assert len(brief.source_digest) == 64
    assert len(brief.facts) >= 1
    assert any(e.name == "CVE-2026-4419" for e in brief.entities)
    assert len(brief.actions) >= 1
