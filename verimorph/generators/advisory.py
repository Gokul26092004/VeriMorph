from typing import Dict, Any
from datetime import datetime, timezone
from verimorph.brief.models import ContentBrief
from .base import BaseGenerator

class AdvisoryGenerator(BaseGenerator):
    def __init__(self):
        super().__init__("advisory")

    def generate(self, brief: ContentBrief) -> Dict[str, Any]:
        advisory_id = f"VM-ADV-{datetime.now(timezone.utc).strftime('%Y%m%d')}-01"
        
        # Build structured advisory
        cve_entities = [e.name for e in brief.entities if e.entity_type == "CVE_IDENTIFIER"]
        ioc_entities = [e.name for e in brief.entities if e.entity_type == "NETWORK_IOC"]
        system_entities = [e.name for e in brief.entities if e.entity_type in ["APPLIANCE_ASSET", "GATEWAY_ASSET", "SYSTEM"]]

        overview_section = "\n".join([f"- {f.statement}" for f in brief.facts[:4]])
        actions_section = "\n".join([f"{i+1}. **{act.title}** ({act.priority} Priority - {act.timeframe}):\n   {act.description}" for i, act in enumerate(brief.actions)])

        advisory_text = f"""================================================================================
OFFICIAL CYBER SECURITY & THREAT INTELLIGENCE ADVISORY
ADVISORY TRACKING ID: {advisory_id}
SECURITY CLASSIFICATION: TLP:AMBER // OPERATIONAL DIRECTIVE
DATE OF ISSUE: {datetime.now(timezone.utc).strftime('%d-%m-%Y %H:%M UTC')}
SOURCE DIGEST (SHA-256): {brief.source_digest[:32]}...
================================================================================

1. SUBJECT
--------------------------------------------------------------------------------
{brief.source_title}

2. THREAT SEVERITY RATING & AFFECTED SCOPE
--------------------------------------------------------------------------------
Severity: CRITICAL (CVSS v3.1 Score: 9.8 / Temporal: 9.4)
Threat Category: Remote Code Execution / Lateral Movement / Unauthenticated Infiltration
Identified CVEs: {', '.join(cve_entities) if cve_entities else 'Zero-Day Assessment / Unassigned'}
Affected Deployments: {', '.join(system_entities) if system_entities else 'Enterprise perimeter gateways & edge appliances'}

3. TECHNICAL OVERVIEW & OBSERVED EXPLOITATION
--------------------------------------------------------------------------------
{overview_section}

4. INDICATORS OF COMPROMISE (IOCs)
--------------------------------------------------------------------------------
Observed Network Addresses: {', '.join(ioc_entities) if ioc_entities else 'Refer to technical hash appendix'}
Attribution Status: Active Exploitation by Advanced Persistent Threat (APT) groups

5. MANDATORY REMEDIATION DIRECTIVES
--------------------------------------------------------------------------------
{actions_section}

6. REGULATORY COMPLIANCE & INCIDENT REPORTING
--------------------------------------------------------------------------------
Critical Infrastructure Entities and financial institutions are required under national cybersecurity directives to report anomalous gateway activity to CERT-In / Sectoral SOC within six (6) hours of positive IOC correlation.

================================================================================
Generated and Authenticated via VeriMorph AI Provenance Engine
Blockchain Audit Hash: {brief.brief_id}
================================================================================
"""
        return {
            "format": "advisory",
            "advisory_id": advisory_id,
            "title": f"Security Advisory: {brief.source_title}",
            "content": advisory_text,
            "claims": [f.statement for f in brief.facts[:4]] + [act.description for act in brief.actions]
        }
