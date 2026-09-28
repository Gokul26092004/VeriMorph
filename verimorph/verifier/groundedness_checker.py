from typing import Dict, Any, List
from .passage_matcher import find_best_matching_chunk

def verify_claims(
    claims: List[str],
    source_chunks: List[Dict[str, Any]],
    threshold_verified: float = 0.50,
    threshold_inferred: float = 0.25
) -> Dict[str, Any]:
    """
    Evaluates each claim generated in a deliverable against source document chunks.
    Tags each claim as VERIFIED, INFERRED, or FLAGGED (unsupported).
    Calculates aggregate groundedness score and provides precise citation coordinates.
    """
    verified_count = 0
    inferred_count = 0
    flagged_count = 0

    evaluations = []

    for idx, claim in enumerate(claims, 1):
        clean_claim = claim.strip()
        if not clean_claim:
            continue

        best_chunk, confidence = find_best_matching_chunk(clean_claim, source_chunks)
        c_id = best_chunk.get("chunk_id", 0)
        c_text = best_chunk.get("text", "")

        if confidence >= threshold_verified:
            status = "VERIFIED"
            verified_count += 1
        elif confidence >= threshold_inferred:
            status = "INFERRED"
            inferred_count += 1
        else:
            status = "FLAGGED"
            flagged_count += 1

        evaluations.append({
            "claim_id": f"CLM-{idx:02d}",
            "claim_text": clean_claim,
            "status": status,
            "confidence_score": confidence,
            "citation": {
                "chunk_id": c_id,
                "source_excerpt": c_text[:200] + ("..." if len(c_text) > 200 else ""),
                "char_start": best_chunk.get("char_start", 0),
                "char_end": best_chunk.get("char_end", 0)
            }
        })

    total_evaluated = len(evaluations)
    groundedness_score = 0.0
    if total_evaluated > 0:
        # Weighted score: VERIFIED = 1.0, INFERRED = 0.5, FLAGGED = 0.0
        weighted_points = (verified_count * 1.0) + (inferred_count * 0.5)
        groundedness_score = round((weighted_points / total_evaluated) * 100, 1)

    overall_status = "PASS" if flagged_count == 0 else ("WARNING" if flagged_count <= 2 else "FAIL")

    return {
        "groundedness_score_percent": groundedness_score,
        "overall_status": overall_status,
        "summary": {
            "total_claims": total_evaluated,
            "verified": verified_count,
            "inferred": inferred_count,
            "flagged": flagged_count
        },
        "claims_report": evaluations
    }

def verify_all_deliverables(
    generated_outputs: Dict[str, Any],
    source_chunks: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Runs Claim Verifier across all 7 generated deliverable outputs.
    """
    verification_results = {}
    aggregate_verified = 0
    aggregate_claims = 0

    for fmt, payload in generated_outputs.items():
        claims = payload.get("claims", [])
        if not claims and "content" in payload:
            # Fallback extract sentences
            claims = [s.strip() for s in payload["content"].split("\n") if len(s.strip()) > 20][:5]

        report = verify_claims(claims, source_chunks)
        verification_results[fmt] = report

        aggregate_verified += report["summary"]["verified"]
        aggregate_claims += report["summary"]["total_claims"]

    avg_score = round((aggregate_verified / aggregate_claims * 100), 1) if aggregate_claims > 0 else 100.0

    return {
        "platform_groundedness_score": avg_score,
        "total_claims_audited": aggregate_claims,
        "deliverable_reports": verification_results
    }
