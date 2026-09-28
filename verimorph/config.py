import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
DATA_DIR = BASE_DIR / "data"
EXPORTS_DIR = PROJECT_ROOT / "exports"

os.makedirs(EXPORTS_DIR, exist_ok=True)

# SIH Hackathon Metadata
SIH_METADATA = {
    "problem_statement_id": "26154",
    "problem_statement_title": "Gen AI Platform for Automated Content Transformation",
    "theme": "Blockchain & Cybersecurity",
    "category": "Software",
    "team_id": "171612",
    "team_name": "Tech stack",
    "project_name": "VeriMorph",
    "tagline": "Gen AI Platform for Automated, Auditable Content Transformation from a Single Source"
}

# Operator Controls Options
AUDIENCE_OPTIONS = [
    "Technical Specialists & Cyber Cells",
    "Executives & Decision Makers (C-Level)",
    "General Public & Citizens",
    "Incident Responders & Field Teams",
    "Media & Public Relations"
]

TONE_OPTIONS = [
    "Urgent & Alert",
    "Professional & Authoritative",
    "Accessible & Educational",
    "Neutral & Objective"
]

LANGUAGE_OPTIONS = [
    "English",
    "Hindi",
    "Tamil",
    "Telugu",
    "Marathi",
    "Bengali",
    "Gujarati"
]

DETAIL_OPTIONS = [
    "Executive (Concise)",
    "Standard",
    "Comprehensive (Deep-Dive)"
]

OBJECTIVE_OPTIONS = [
    "Incident Containment & Action",
    "Public Awareness & Advisory",
    "Strategic Decision-Making",
    "Compliance & Audit Readiness"
]

SUPPORTED_FORMATS = [
    "video_package",
    "linkedin_post",
    "twitter_thread",
    "advisory",
    "infographic",
    "executive_summary",
    "presentation_deck"
]

# AI Provider Configuration (Supports Offline Heuristic AI / vLLM / Gemini API)
AI_PROVIDER = os.getenv("VERIMORPH_AI_PROVIDER", "hybrid") # "hybrid", "gemini", "vllm", "offline"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
VLLM_ENDPOINT = os.getenv("VLLM_ENDPOINT", "http://localhost:8000/v1")
DEFAULT_LEDGER_SIGNER = "TechStack_Node_171612"
