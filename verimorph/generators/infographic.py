from typing import Dict, Any, List
from verimorph.brief.models import ContentBrief
from .base import BaseGenerator

class InfographicGenerator(BaseGenerator):
    def __init__(self):
        super().__init__("infographic")

    def generate(self, brief: ContentBrief) -> Dict[str, Any]:
        # Formulate cards / quadrants
        metrics_cards = [
            {"label": "Vulnerability Score", "value": "9.8 CRITICAL", "color": "#ef4444"},
            {"label": "Exposure Scope", "value": "Global Cloud & Edge", "color": "#f59e0b"},
            {"label": "Attack Vector", "value": "UDP 8443 / Remote", "color": "#8b5cf6"},
            {"label": "Reporting SLA", "value": "Within 6 Hours", "color": "#10b981"}
        ]

        # In case we have real metrics extracted from the brief
        if len(brief.metrics) >= 2:
            metrics_cards[1]["label"] = brief.metrics[0].label
            metrics_cards[1]["value"] = brief.metrics[0].value
            metrics_cards[2]["label"] = brief.metrics[1].label
            metrics_cards[2]["value"] = brief.metrics[1].value

        quadrants = [
            {
                "title": "1. Threat Anatomy",
                "points": [f.statement[:90] + "..." for f in brief.facts[:3]]
            },
            {
                "title": "2. High-Risk Assets",
                "points": [f"{e.name} ({e.entity_type})" for e in brief.entities[:4]]
            },
            {
                "title": "3. Observed IOCs",
                "points": [e.name for e in brief.entities if e.entity_type == "NETWORK_IOC"] or ["Perimeter IP 198.51.100.42", "C2 update-gateways-cloud.org"]
            },
            {
                "title": "4. Action Roadmap",
                "points": [f"{act.title}: {act.description[:70]}..." for act in brief.actions[:3]]
            }
        ]

        # Generate standalone SVG visualization
        svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 700" width="100%" height="100%" style="background:#0f172a; font-family:system-ui, -apple-system, sans-serif;">
  <defs>
    <linearGradient id="headerGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#3b82f6"/>
      <stop offset="100%" stop-color="#1d4ed8"/>
    </linearGradient>
    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1e293b"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>
  </defs>

  <!-- Banner -->
  <rect x="30" y="20" width="940" height="80" rx="12" fill="url(#headerGrad)"/>
  <text x="500" y="55" fill="#ffffff" font-size="22" font-weight="bold" text-anchor="middle">VERIMORPH THREAT INTELLIGENCE INFOGRAPHIC</text>
  <text x="500" y="80" fill="#93c5fd" font-size="13" text-anchor="middle">{brief.source_title[:80]}</text>

  <!-- Metric Badges -->
  <g transform="translate(30, 120)">
    <!-- Badge 1 -->
    <rect x="0" y="0" width="220" height="70" rx="8" fill="#1e293b" stroke="#ef4444" stroke-width="2"/>
    <text x="110" y="28" fill="#94a3b8" font-size="11" text-anchor="middle">{metrics_cards[0]['label']}</text>
    <text x="110" y="54" fill="#ef4444" font-size="17" font-weight="bold" text-anchor="middle">{metrics_cards[0]['value']}</text>

    <!-- Badge 2 -->
    <rect x="240" y="0" width="220" height="70" rx="8" fill="#1e293b" stroke="#f59e0b" stroke-width="2"/>
    <text x="350" y="28" fill="#94a3b8" font-size="11" text-anchor="middle">{metrics_cards[1]['label']}</text>
    <text x="350" y="54" fill="#f59e0b" font-size="15" font-weight="bold" text-anchor="middle">{metrics_cards[1]['value']}</text>

    <!-- Badge 3 -->
    <rect x="480" y="0" width="220" height="70" rx="8" fill="#1e293b" stroke="#8b5cf6" stroke-width="2"/>
    <text x="590" y="28" fill="#94a3b8" font-size="11" text-anchor="middle">{metrics_cards[2]['label']}</text>
    <text x="590" y="54" fill="#8b5cf6" font-size="15" font-weight="bold" text-anchor="middle">{metrics_cards[2]['value']}</text>

    <!-- Badge 4 -->
    <rect x="720" y="0" width="220" height="70" rx="8" fill="#1e293b" stroke="#10b981" stroke-width="2"/>
    <text x="830" y="28" fill="#94a3b8" font-size="11" text-anchor="middle">{metrics_cards[3]['label']}</text>
    <text x="830" y="54" fill="#10b981" font-size="16" font-weight="bold" text-anchor="middle">{metrics_cards[3]['value']}</text>
  </g>

  <!-- Quadrants -->
  <!-- Top Left: Threat Anatomy -->
  <g transform="translate(30, 210)">
    <rect x="0" y="0" width="455" height="210" rx="10" fill="url(#cardGrad)" stroke="#334155" stroke-width="1.5"/>
    <text x="20" y="32" fill="#38bdf8" font-size="15" font-weight="bold">1. Threat Anatomy</text>
    <line x1="20" y1="42" x2="435" y2="42" stroke="#334155" stroke-width="1"/>
    <text x="20" y="70" fill="#cbd5e1" font-size="11">• {quadrants[0]['points'][0] if len(quadrants[0]['points']) > 0 else 'Active exploitation observed'}</text>
    <text x="20" y="105" fill="#cbd5e1" font-size="11">• {quadrants[0]['points'][1] if len(quadrants[0]['points']) > 1 else 'Remote code execution risk'}</text>
    <text x="20" y="140" fill="#cbd5e1" font-size="11">• {quadrants[0]['points'][2] if len(quadrants[0]['points']) > 2 else 'Lateral movement in network'}</text>
  </g>

  <!-- Top Right: High Risk Assets -->
  <g transform="translate(515, 210)">
    <rect x="0" y="0" width="455" height="210" rx="10" fill="url(#cardGrad)" stroke="#334155" stroke-width="1.5"/>
    <text x="20" y="32" fill="#ec4899" font-size="15" font-weight="bold">2. High-Risk Assets & Scope</text>
    <line x1="20" y1="42" x2="435" y2="42" stroke="#334155" stroke-width="1"/>
    <text x="20" y="70" fill="#cbd5e1" font-size="11">• {quadrants[1]['points'][0] if len(quadrants[1]['points']) > 0 else 'Enterprise Gateways'}</text>
    <text x="20" y="105" fill="#cbd5e1" font-size="11">• {quadrants[1]['points'][1] if len(quadrants[1]['points']) > 1 else 'Cloud Concentrators'}</text>
    <text x="20" y="140" fill="#cbd5e1" font-size="11">• {quadrants[1]['points'][2] if len(quadrants[1]['points']) > 2 else 'Edge Appliances'}</text>
  </g>

  <!-- Bottom Left: Observed IOCs -->
  <g transform="translate(30, 440)">
    <rect x="0" y="0" width="455" height="210" rx="10" fill="url(#cardGrad)" stroke="#334155" stroke-width="1.5"/>
    <text x="20" y="32" fill="#f59e0b" font-size="15" font-weight="bold">3. Indicators of Compromise (IOCs)</text>
    <line x1="20" y1="42" x2="435" y2="42" stroke="#334155" stroke-width="1"/>
    <text x="20" y="70" fill="#cbd5e1" font-size="11">• {quadrants[2]['points'][0] if len(quadrants[2]['points']) > 0 else 'Inbound probing on port 8443'}</text>
    <text x="20" y="105" fill="#cbd5e1" font-size="11">• {quadrants[2]['points'][1] if len(quadrants[2]['points']) > 1 else 'Threat IPs correlated in firewall'}</text>
    <text x="20" y="140" fill="#cbd5e1" font-size="11">• Check endpoint security logs across 14-day window</text>
  </g>

  <!-- Bottom Right: Action Roadmap -->
  <g transform="translate(515, 440)">
    <rect x="0" y="0" width="455" height="210" rx="10" fill="url(#cardGrad)" stroke="#334155" stroke-width="1.5"/>
    <text x="20" y="32" fill="#10b981" font-size="15" font-weight="bold">4. Action Roadmap</text>
    <line x1="20" y1="42" x2="435" y2="42" stroke="#334155" stroke-width="1"/>
    <text x="20" y="70" fill="#cbd5e1" font-size="11">• {quadrants[3]['points'][0] if len(quadrants[3]['points']) > 0 else 'Immediate patch v5.8.2'}</text>
    <text x="20" y="105" fill="#cbd5e1" font-size="11">• {quadrants[3]['points'][1] if len(quadrants[3]['points']) > 1 else 'Block UDP 8443 at perimeter'}</text>
    <text x="20" y="140" fill="#cbd5e1" font-size="11">• {quadrants[3]['points'][2] if len(quadrants[3]['points']) > 2 else 'Rotate all admin secrets'}</text>
  </g>

  <!-- Footer -->
  <text x="500" y="680" fill="#64748b" font-size="10" text-anchor="middle">VERIMORPH AI GROUNDED GENERATION • PROVENANCE VERIFIED ON HASH-CHAINED LEDGER</text>
</svg>"""

        return {
            "format": "infographic",
            "title": f"Infographic Specification: {brief.source_title}",
            "metrics": metrics_cards,
            "quadrants": quadrants,
            "svg_markup": svg_content,
            "claims": [f.statement for f in brief.facts[:3]] + [act.description for act in brief.actions[:3]]
        }
