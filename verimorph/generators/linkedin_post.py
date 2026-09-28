from typing import Dict, Any
from verimorph.brief.models import ContentBrief
from .base import BaseGenerator

class LinkedInPostGenerator(BaseGenerator):
    def __init__(self):
        super().__init__("linkedin_post")

    def generate(self, brief: ContentBrief) -> Dict[str, Any]:
        settings = brief.operator_settings
        audience = settings.get("audience", "Executives & Decision Makers")
        
        # Extract CVEs / Systems
        entities_text = ", ".join([e.name for e in brief.entities[:4]])
        actions_list = [f"🔹 {act.title}: {act.description}" for act in brief.actions[:4]]
        facts_list = [f"• {f.statement}" for f in brief.facts[:3]]

        post_text = (
            f"🚨 CRITICAL INCIDENT BRIEFING: {brief.source_title}\n\n"
            f"Senior leaders, CISOs, and engineering teams ({audience}) must take immediate note. "
            f"A high-priority operational notice has been issued.\n\n"
            f"📌 THE CORE SITUATION:\n"
            + "\n".join(facts_list) + "\n\n"
            f"⚡ KEY ASSETS & IDENTIFIERS:\n"
            f"Identified entities: {entities_text if entities_text else 'Enterprise perimeter components'}\n\n"
            f"🛡️ MANDATORY CONTAINMENT ROADMAP:\n"
            + "\n".join(actions_list) + "\n\n"
            f"💡 STRATEGIC TAKEAWAY:\n"
            f"Perimeter hygiene and auditable change controls are no longer optional. "
            f"Ensure your SOC team cross-references network logs and enforces immediate perimeter hardening.\n\n"
            f"Has your organization implemented the latest patches? Share your mitigation protocols below.\n\n"
            f"#CyberSecurity #IncidentResponse #ThreatIntel #CISO #EnterpriseSecurity #GovTech #SIH2026 #VeriMorph"
        )

        return {
            "format": "linkedin_post",
            "title": f"LinkedIn Advisory: {brief.source_title}",
            "content": post_text,
            "character_count": len(post_text),
            "claims": [f.statement for f in brief.facts[:3]] + [act.description for act in brief.actions[:4]]
        }
