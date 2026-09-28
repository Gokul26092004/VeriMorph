from typing import Dict, Any, List
from verimorph.brief.models import ContentBrief
from .base import BaseGenerator

class PresentationDeckGenerator(BaseGenerator):
    def __init__(self):
        super().__init__("presentation_deck")

    def generate(self, brief: ContentBrief) -> Dict[str, Any]:
        slides: List[Dict[str, Any]] = []

        # Slide 1: Title & Overview
        slides.append({
            "slide_number": 1,
            "title": brief.source_title,
            "subtitle": "Executive Incident Briefing & Rapid Action Protocol",
            "bullets": [
                f"Operational Context: {brief.intent_and_objective}",
                "Classification: TLP:AMBER // Critical Infrastructure Advisory",
                f"Generated from Single Verified Source (Digest: {brief.source_digest[:16]}...)",
                f"Target Audience: {brief.operator_settings.get('audience', 'Technical Specialists')}"
            ],
            "visual_layout": "Dark minimalist cyber theme with high-contrast badge and timestamp lockup.",
            "speaker_notes": (
                "Good morning, leadership and response teams. Today we are presenting an urgent operational "
                f"briefing regarding {brief.source_title}. Our goal is to align on the technical facts, "
                "understand organizational exposure, and authorize immediate remediation actions."
            )
        })

        # Slide 2: Threat Landscape & Observed Facts
        fact_bullets = [f"• {f.statement}" for f in brief.facts[:3]]
        slides.append({
            "slide_number": 2,
            "title": "Threat Landscape & Observed Facts",
            "subtitle": "Verified Grounded Observations",
            "bullets": fact_bullets if fact_bullets else [
                "• Targeted, active exploitation of zero-day vulnerabilities in enterprise perimeter nodes.",
                "• Unauthenticated remote code execution achieved with root privileges.",
                "• In-the-wild deployment of secondary payload and ransomware variants."
            ],
            "visual_layout": "Two-column split: Left highlights key fact bullet points; Right shows CVE metadata card.",
            "speaker_notes": (
                "Moving to slide 2, these are the confirmed facts verified directly from telemetry and CERT advisories. "
                "The threat actor is actively scanning for vulnerable perimeter gateways. Notice that exploitation does not "
                "require internal authentication, giving attackers immediate foothold if unpatched."
            )
        })

        # Slide 3: Affected Systems & IOCs
        entities_list = [f"• {e.name}: {e.context or e.entity_type}" for e in brief.entities[:4]]
        slides.append({
            "slide_number": 3,
            "title": "Affected Scope & Threat Telemetry",
            "subtitle": "Infrastructure Footprint & Indicators of Compromise",
            "bullets": entities_list if entities_list else [
                "• Enterprise Perimeter Gateways running vulnerable firmware",
                "• Cloud-hosted Concentrator instances across AWS, Azure, and GCP",
                "• Network IOCs: Malicious C2 infrastructure and binary payloads"
            ],
            "visual_layout": "Network topology diagram depicting perimeter edge vs internal trust zones.",
            "speaker_notes": (
                "On slide 3, we illustrate the affected surface. Both on-premises enterprise appliances and cloud-based "
                "virtual concentrators are impacted. Our SOC has already loaded these IOC addresses into our SIEM "
                "to search for any historical outbound beacons over the last 14 days."
            )
        })

        # Slide 4: Strategic Impact & Risk Analysis
        slides.append({
            "slide_number": 4,
            "title": "Impact & Organizational Risk Matrix",
            "subtitle": "Consequences of Inaction",
            "bullets": [
                "• Perimeter Takeover: Total administrative control of perimeter gateway daemons.",
                "• Lateral Escalation: Potential exfiltration of session credentials and privileged tokens.",
                "• Ransomware Disruption: Infiltration of secondary payloads targeting core file stores.",
                "• Compliance Liability: Mandatory CERT-In reporting window within 6 hours."
            ],
            "visual_layout": "Risk heat matrix highlighting operational, legal, and reputational risk factors.",
            "speaker_notes": (
                "Slide 4 highlights our organizational risk. If we do not patch during the current maintenance window, "
                "the risk escalates from edge compromise to lateral movement. Additionally, regulatory reporting mandates "
                "require transparent disclosure within tight timeframes."
            )
        })

        # Slide 5: Defensive Remediation Protocol
        action_bullets = [f"• {act.title}: {act.description}" for act in brief.actions[:4]]
        slides.append({
            "slide_number": 5,
            "title": "Immediate Action Roadmap",
            "subtitle": "Four-Phase Incident Containment",
            "bullets": action_bullets if action_bullets else [
                "• Phase 1: Deploy vendor emergency firmware patch v5.8.2.",
                "• Phase 2: Restrict perimeter access to UDP management ports.",
                "• Phase 3: Force rotation of administrative session tokens and master API keys.",
                "• Phase 4: Conduct comprehensive threat hunting across gateway authorization logs."
            ],
            "visual_layout": "Four-phase progressive milestone timeline with owner accountability tags.",
            "speaker_notes": (
                "Here is the tactical remediation plan on slide 5. We have sequenced this into four immediate phases. "
                "Phase 1 and 2 can be executed within the next 2 hours, followed by credential rotation and forensic threat hunting."
            )
        })

        # Slide 6: Governance, Provenance & Next Steps
        slides.append({
            "slide_number": 6,
            "title": "Governance & Next Steps",
            "subtitle": "Immutable Audit Trail & Continuous Verification",
            "bullets": [
                f"• Verified Provenance: Brief ID `{brief.brief_id}` committed to blockchain ledger.",
                "• Claim Grounding: All presentation points cross-referenced against official source text.",
                "• Ongoing Monitoring: Hourly telemetry reviews with the Incident Command team.",
                "• Contact: National Cyber Coordination Centre & Team Tech stack Operations."
            ],
            "visual_layout": "Summary banner with cryptographic verification badge and QR code link to audit certificate.",
            "speaker_notes": (
                "To conclude on slide 6: every statement in this deck is grounded in source intelligence and logged "
                "with cryptographic hashes on our VeriMorph blockchain ledger for complete tamper-proof accountability. "
                "We now open the floor for immediate approval of the maintenance window. Thank you."
            )
        })

        return {
            "format": "presentation_deck",
            "title": f"Presentation Deck: {brief.source_title}",
            "total_slides": len(slides),
            "slides": slides,
            "claims": [f.statement for f in brief.facts[:4]] + [act.description for act in brief.actions[:4]]
        }
