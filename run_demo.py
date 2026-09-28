"""
VeriMorph CLI Demo Runner
Smart India Hackathon 2026 | Problem Statement 26154 | Team ID: 171612 (Tech stack)

Executes an end-to-end multi-format transformation from a single source document,
runs the Claim Verifier, mints a cryptographic block on the Blockchain Ledger,
and outputs all 7 deliverables.
"""

import sys
import os
import json
from pathlib import Path

# Fix Windows console UTF-8 encoding for emojis
if sys.platform == "win32" and hasattr(sys.stdout, "buffer"):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from verimorph.config import DATA_DIR, SIH_METADATA
from verimorph.ingestion import parse_text
from verimorph.brief import generate_content_brief
from verimorph.generators import generate_all_formats
from verimorph.verifier import verify_all_deliverables
from verimorph.ledger import ProvenanceLedger, generate_audit_certificate

def main():
    print("=" * 80)
    print(f"🛡️  VERIMORPH: {SIH_METADATA['tagline']}")
    print(f"🏆  Smart India Hackathon 2026 | PS ID: {SIH_METADATA['problem_statement_id']}")
    print(f"👥  Team: {SIH_METADATA['team_name']} (ID: {SIH_METADATA['team_id']})")
    print("=" * 80)

    # 1. Load Sample CERT-In Advisory
    sample_path = DATA_DIR / "cert_in_advisory_sample.txt"
    if not sample_path.exists():
        print(f"Error: Sample data not found at {sample_path}")
        return

    with open(sample_path, "r", encoding="utf-8") as f:
        source_text = f.read()

    print(f"\n[STEP 1/5] Ingesting Source Content: '{sample_path.name}'...")
    parsed_input = parse_text(source_text)
    print(f"  ✓ Ingested {parsed_input['total_words']} words across {parsed_input['total_chunks']} indexable chunks.")

    # 2. Build Content Brief
    print("\n[STEP 2/5] Synthesizing Single Content Brief ('Analyze Once')...")
    operator_settings = {
        "audience": "Technical Specialists & Cyber Cells",
        "tone": "Urgent & Alert",
        "language": "English",
        "detail": "Standard",
        "objective": "Incident Containment & Action"
    }
    brief = generate_content_brief(parsed_input, operator_settings)
    print(f"  ✓ Content Brief ID: {brief.brief_id}")
    print(f"  ✓ Extracted {len(brief.facts)} ground-truth facts cited to source chunks.")
    print(f"  ✓ Extracted {len(brief.entities)} threat entities/IOCs.")
    print(f"  ✓ Extracted {len(brief.actions)} mandatory mitigation directives.")

    # 3. Parallel Format Generation (7 formats)
    print("\n[STEP 3/5] Executing 7 Parallel Format Generators...")
    deliverables = generate_all_formats(brief)
    for fmt_name in deliverables.keys():
        print(f"  ✓ Generated: {fmt_name.upper()}")

    # 4. Claim Verifier
    print("\n[STEP 4/5] Running Grounded Claim Verifier (Hallucination Defense)...")
    verification_report = verify_all_deliverables(deliverables, parsed_input["chunks"])
    print(f"  ✓ Total Claims Audited: {verification_report['total_claims_audited']}")
    print(f"  ✓ Platform Groundedness Index: {verification_report['platform_groundedness_score']}%")

    # 5. Blockchain Provenance Ledger
    print("\n[STEP 5/5] Minting Cryptographic Provenance Block on Blockchain Ledger...")
    ledger = ProvenanceLedger()
    block = ledger.record_transformation(
        source_content=parsed_input["content"],
        brief_data=brief.model_dump(),
        settings_data=operator_settings,
        outputs_data=deliverables,
        verifier_report=verification_report,
        signer="TechStack_Operator_171612"
    )
    print(f"  ✓ MINTED BLOCK #{block.index}")
    print(f"    - Block Hash:   {block.block_hash}")
    print(f"    - Merkle Root:  {block.merkle_root}")
    print(f"    - Prev Hash:    {block.previous_hash}")

    is_valid, msg = ledger.verify_integrity()
    print(f"  ✓ Ledger Integrity Status: {msg}")

    # Generate Audit Certificate
    cert = generate_audit_certificate(block, SIH_METADATA)
    print(f"  ✓ Audit Certificate Created: {cert['certificate_id']}")

    print("\n" + "=" * 80)
    print("🎯  DEMONSTRATION COMPLETE: Single Source transformed into 7 Audited Channels!")
    print("    To launch the interactive dashboard, run:")
    print("    python -m uvicorn verimorph.web.app:app --reload --port 8000")
    print("=" * 80)

if __name__ == "__main__":
    main()
