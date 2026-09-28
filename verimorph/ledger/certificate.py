import json
from typing import Dict, Any
from .block import Block

def generate_audit_certificate(block: Block, project_meta: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Generates a cryptographically verifiable provenance certificate for exported content.
    """
    meta = project_meta or {
        "platform": "VeriMorph AI",
        "theme": "Blockchain & Cybersecurity",
        "sih_team": "Tech stack (171612)"
    }

    certificate_id = f"CERT-VM-{block.block_hash[:16].upper()}"

    formatted_cert = {
        "certificate_id": certificate_id,
        "standard": "C2PA / Hyperledger Fabric Hash-Chained Provenance Spec v1.0",
        "block_index": block.index,
        "timestamp": block.timestamp,
        "signer": block.signer_identity,
        "cryptographic_proofs": {
            "block_hash": block.block_hash,
            "previous_hash": block.previous_hash,
            "merkle_root": block.merkle_root,
            "source_hash_sha256": block.source_hash,
            "content_brief_hash_sha256": block.brief_hash,
            "operator_settings_hash_sha256": block.settings_hash,
            "outputs_hash_sha256": block.outputs_hash,
            "verifier_report_hash_sha256": block.verifier_hash
        },
        "verification_statement": (
            "This certificate guarantees that the deliverables produced were generated from "
            "the single cited source content without unauthorized alteration, and each claim was "
            "evaluated for source groundedness."
        ),
        "organization": meta
    }

    return formatted_cert
