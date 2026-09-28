from typing import Dict, Any, List
from verimorph.brief.models import ContentBrief
from .base import BaseGenerator

class VideoPackageGenerator(BaseGenerator):
    def __init__(self):
        super().__init__("video_package")

    def generate(self, brief: ContentBrief) -> Dict[str, Any]:
        settings = brief.operator_settings
        tone = settings.get("tone", "Professional & Authoritative")
        audience = settings.get("audience", "Technical Specialists")
        
        # Build scenes based on the facts and actions
        scenes = []
        srt_cues = []
        time_offset = 0

        # Scene 1: Hook
        hook_text = (
            f"Attention all {audience}. A critical security advisory has been released regarding {brief.source_title}. "
            f"Here is what you must know right now."
        )
        scenes.append({
            "scene_number": 1,
            "title": "The Operational Hook",
            "duration_sec": 6,
            "visual_description": "Dark cyber war-room graphic with pulsing red alert borders. Digital globe highlighting threat vectors.",
            "camera_angle": "Dynamic tracking shot zooming into server node status lights.",
            "audio_cues": "Low-frequency synth drone rising into a subtle alert tone.",
            "narration_script": hook_text
        })
        srt_cues.append((time_offset, time_offset + 6, hook_text))
        time_offset += 6

        # Scene 2: The Core Problem / Facts
        fact_texts = [f.statement for f in brief.facts[:2]]
        fact_narration = " ".join(fact_texts) if fact_texts else "Critical perimeter vulnerabilities are currently being actively exploited."
        scenes.append({
            "scene_number": 2,
            "title": "Threat Anatomy & Core Facts",
            "duration_sec": 10,
            "visual_description": "Split screen displaying network architecture diagram with packet inspection telemetry and affected components.",
            "camera_angle": "Medium close-up on diagnostic terminal displaying CVE identifiers and memory heap alerts.",
            "audio_cues": "Subtle mechanical keystrokes with pulsating bass rhythm.",
            "narration_script": fact_narration
        })
        srt_cues.append((time_offset, time_offset + 10, fact_narration))
        time_offset += 10

        # Scene 3: Impact & Assets
        affected_entities = [e.name for e in brief.entities if e.entity_type in ["APPLIANCE_ASSET", "GATEWAY_ASSET", "CVE_IDENTIFIER", "SYSTEM"]]
        entities_str = ", ".join(affected_entities) if affected_entities else "Enterprise gateways and cloud infrastructure"
        impact_narration = f"Impacted systems include {entities_str}. Adversaries can achieve privileged remote execution and lateral persistence."
        scenes.append({
            "scene_number": 3,
            "title": "Impact & Affected Perimeter",
            "duration_sec": 8,
            "visual_description": "Isometric 3D render of an enterprise cloud infrastructure showing lateral spread between subnets.",
            "camera_angle": "Wide bird's-eye view transitioning to red warning perimeter ring.",
            "audio_cues": "Tension-building string swell.",
            "narration_script": impact_narration
        })
        srt_cues.append((time_offset, time_offset + 8, impact_narration))
        time_offset += 8

        # Scene 4: Action / Remediation
        action_texts = [f"{i+1}: {act.title} - {act.description}" for i, act in enumerate(brief.actions[:3])]
        action_narration = "Immediate directives: " + " ".join([f"Step {i+1}, {act.title}." for i, act in enumerate(brief.actions[:3])])
        scenes.append({
            "scene_number": 4,
            "title": "Remediation & Action Plan",
            "duration_sec": 12,
            "visual_description": "Clean step-by-step checklist checklist overlay with green tick marks indicating defensive mitigations.",
            "camera_angle": "Static graphic layout with animated typography.",
            "audio_cues": "Confident, resolute electronic beat with rhythmic pulses.",
            "narration_script": action_narration
        })
        srt_cues.append((time_offset, time_offset + 12, action_narration))
        time_offset += 12

        # Scene 5: Outro / Governance
        outro_narration = "Verify all signatures, update firmware immediately, and report detections to your incident response team. Stay secure."
        scenes.append({
            "scene_number": 5,
            "title": "Summary & Official Directive",
            "duration_sec": 6,
            "visual_description": "Official CERT / Security Operations logo card with emergency reporting contact and QR code.",
            "camera_angle": "Center aligned lockup, fade to black.",
            "audio_cues": "Crisp closing chime resolving to silence.",
            "narration_script": outro_narration
        })
        srt_cues.append((time_offset, time_offset + 6, outro_narration))
        time_offset += 6

        # Generate SRT string
        srt_lines = []
        for idx, (start_s, end_s, text) in enumerate(srt_cues, 1):
            def fmt_time(seconds):
                h = int(seconds // 3600)
                m = int((seconds % 3600) // 60)
                s = int(seconds % 60)
                ms = int((seconds - int(seconds)) * 1000)
                return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
            
            srt_lines.append(f"{idx}")
            srt_lines.append(f"{fmt_time(start_s)} --> {fmt_time(end_s)}")
            srt_lines.append(text)
            srt_lines.append("")

        srt_content = "\n".join(srt_lines)

        full_script = "\n\n".join([
            f"[SCENE {s['scene_number']}: {s['title']} ({s['duration_sec']}s)]\n"
            f"VISUAL: {s['visual_description']}\n"
            f"AUDIO: {s['audio_cues']}\n"
            f"NARRATION: \"{s['narration_script']}\""
            for s in scenes
        ])

        return {
            "format": "video_package",
            "title": f"Video Package: {brief.source_title}",
            "total_duration_sec": time_offset,
            "scenes": scenes,
            "narration_script": full_script,
            "srt_subtitles": srt_content,
            "claims": [s["narration_script"] for s in scenes]
        }
