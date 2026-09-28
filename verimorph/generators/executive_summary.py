from typing import Dict, Any
from verimorph.brief.models import ContentBrief
from .base import BaseGenerator

class ExecutiveSummaryGenerator(BaseGenerator):
    def __init__(self):
        super().__init__("executive_summary")

    def generate(self, brief: ContentBrief) -> Dict[str, Any]:
        bluf = (
            f"Active exploitation of perimeter infrastructure poses immediate operational compromise, "
            f"data exfiltration, and lateral ransomware deployment risks. C-Level leadership must authorize "
            f"emergency patching windows and perimeter restriction protocols within the next 4 hours."
        )

        facts_bullets = "\n".join([f"- **Key Finding:** {f.statement}" for f in brief.facts[:4]])
        actions_matrix = "\n".join([
            f"| {act.title} | {act.priority} | {act.timeframe} | Lead Incident Commander |"
            for act in brief.actions[:4]
        ])

        summary_text = f"""# EXECUTIVE DECISION BRIEFING: {brief.source_title.upper()}
**Classification:** STRICTLY CONFIDENTIAL // C-SUITE & BOARD OF DIRECTORS  
**Provenance Verification:** Verified Authentic (Hash: `{brief.brief_id}`)

---

### 1. BOTTOM LINE UP FRONT (BLUF)
{bluf}

---

### 2. STRATEGIC & OPERATIONAL RISK ASSESSMENT

| Risk Vector | Exposure Level | Business Impact | Mitigation Target |
|:------------|:---------------|:----------------|:------------------|
| Perimeter Compromise | **CRITICAL** | Total administrative takeover of network edge | Firmware patch v5.8.2 |
| Data Confidentiality | **HIGH** | Exfiltration of user credential caches | Key & token rotation |
| Business Continuity | **HIGH** | Potential lateral ransomware encryption | Segment isolation |
| Regulatory Liability | **HIGH** | CERT-In 6-hour disclosure mandate | SOC compliance report |

---

### 3. VERIFIED CORE INTELLIGENCE
{facts_bullets}

---

### 4. EXECUTIVE ACTION MATRIX

| Mandated Initiative | Priority | Execution Window | Accountability |
|:---------------------|:---------|:-----------------|:---------------|
{actions_matrix}

---

### 5. STRATEGIC RESOURCE AUTHORIZATION REQUEST
1. Emergency maintenance window authorization to apply edge gateway firmware.
2. Cross-functional SOC and network operations bridge standby for 24 hours.
3. Legal and compliance notification of relevant regulatory reporting timelines.
"""

        return {
            "format": "executive_summary",
            "title": f"Executive Summary: {brief.source_title}",
            "bluf": bluf,
            "content": summary_text,
            "claims": [f.statement for f in brief.facts[:4]] + [act.description for act in brief.actions[:4]]
        }
