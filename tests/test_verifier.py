import pytest
from verimorph.ingestion import parse_text
from verimorph.verifier import verify_claims

def test_verify_claims_high_grounding():
    source_text = "Adversary exploiting CVE-2026-4419 on UDP port 8443 to gain root privileges."
    parsed = parse_text(source_text)
    
    claims = [
        "CVE-2026-4419 is being exploited on UDP port 8443 to achieve root privileges.",
        "Completely unrelated text about tropical fruit markets in Alaska."
    ]

    report = verify_claims(claims, parsed["chunks"])
    assert report["summary"]["total_claims"] == 2
    assert report["summary"]["verified"] >= 1
    assert report["summary"]["flagged"] >= 1
    assert report["claims_report"][0]["status"] == "VERIFIED"
    assert report["claims_report"][1]["status"] == "FLAGGED"
