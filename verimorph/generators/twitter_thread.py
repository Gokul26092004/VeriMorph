from typing import Dict, Any, List
from verimorph.brief.models import ContentBrief
from .base import BaseGenerator

class TwitterThreadGenerator(BaseGenerator):
    def __init__(self):
        super().__init__("twitter_thread")

    def generate(self, brief: ContentBrief) -> Dict[str, Any]:
        settings = brief.operator_settings
        
        tweets: List[str] = []

        # Tweet 1: Hook
        t1 = (
            f"1/6 🚨 URGENT ADVISORY: {brief.source_title}.\n\n"
            f"Active exploitation detected in enterprise environments. "
            f"Here is a breakdown of the threat vector, affected systems, and immediate fix 🧵👇"
        )
        tweets.append(t1)

        # Tweet 2: The Core Vulnerability / Threat
        fact1 = brief.facts[0].statement if len(brief.facts) > 0 else "Perimeter vulnerability being actively leveraged."
        t2 = f"2/6 🔍 What is happening:\n\n{fact1}\n\nThreat actors are targeting vulnerable interfaces to gain privileged execution."
        tweets.append(t2)

        # Tweet 3: Affected Systems & IOCs
        entities = [e.name for e in brief.entities[:4]]
        entities_str = ", ".join(entities) if entities else "Enterprise perimeter nodes"
        t3 = (
            f"3/6 🎯 Affected Assets & Identifiers:\n\n"
            f"Key targets & IOCs: {entities_str}.\n"
            f"Ensure your network telemetry and IDS rules flag these endpoints immediately."
        )
        tweets.append(t3)

        # Tweet 4: Remediation Step 1 & 2
        act1 = brief.actions[0].description if len(brief.actions) > 0 else "Apply emergency security patches."
        act2 = brief.actions[1].description if len(brief.actions) > 1 else "Restrict external management access."
        t4 = (
            f"4/6 🛠️ Defensive Actions (Part 1):\n\n"
            f"1️⃣ {act1}\n\n"
            f"2️⃣ {act2}"
        )
        tweets.append(t4)

        # Tweet 5: Remediation Step 3 & 4
        act3 = brief.actions[2].description if len(brief.actions) > 2 else "Inspect authorization logs for anomalous sessions."
        act4 = brief.actions[3].description if len(brief.actions) > 3 else "Report compromise to national incident response teams."
        t5 = (
            f"5/6 🛡️ Defensive Actions (Part 2):\n\n"
            f"3️⃣ {act3}\n\n"
            f"4️⃣ {act4}"
        )
        tweets.append(t5)

        # Tweet 6: Conclusion / CTA
        t6 = (
            f"6/6 ⚠️ Summary:\n\n"
            f"Prompt mitigation is essential to avoid lateral movement. "
            f"All content verified by VeriMorph AI with blockchain provenance.\n\n"
            f"🔄 Retweet to alert your engineering & security network!"
        )
        tweets.append(t6)

        thread_markdown = "\n\n---\n\n".join(tweets)

        return {
            "format": "twitter_thread",
            "title": f"X Thread: {brief.source_title}",
            "tweets": tweets,
            "total_tweets": len(tweets),
            "content": thread_markdown,
            "claims": [f.statement for f in brief.facts[:2]] + [act.description for act in brief.actions[:4]]
        }
