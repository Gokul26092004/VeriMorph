import os
import sys
import json
from pathlib import Path
from typing import Dict, Any, List, Optional

# Ensure project root is in sys.path
CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT_DIR = CURRENT_FILE.parent.parent.parent
if str(PROJECT_ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT_DIR))

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from pydantic import BaseModel

from verimorph.config import (
    BASE_DIR, PROJECT_ROOT, DATA_DIR, EXPORTS_DIR,
    PLATFORM_METADATA, SIH_METADATA, AUDIENCE_OPTIONS, TONE_OPTIONS, LANGUAGE_OPTIONS,
    DETAIL_OPTIONS, OBJECTIVE_OPTIONS, SUPPORTED_FORMATS
)
from verimorph.ingestion import parse_text, parse_document, scrape_url
from verimorph.brief import generate_content_brief
from verimorph.generators import generate_all_formats
from verimorph.verifier import verify_all_deliverables, verify_claims
from verimorph.ledger import ProvenanceLedger, generate_audit_certificate
from verimorph.export import export_srt, export_docx, export_pptx, export_pdf

app = FastAPI(
    title="VeriMorph AI Platform",
    description="Gen AI Platform for Automated, Auditable Content Transformation from a Single Source",
    version="1.0.0"
)

# Initialize persistence for blockchain ledger
LEDGER_PATH = PROJECT_ROOT / "verimorph_ledger.json"
ledger = ProvenanceLedger(persistence_path=str(LEDGER_PATH))

# Mount static files
STATIC_DIR = BASE_DIR / "web" / "static"
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

class TransformRequest(BaseModel):
    source_text: str
    source_url: Optional[str] = None
    audience: str = "Technical Specialists & Cyber Cells"
    tone: str = "Urgent & Alert"
    language: str = "English"
    detail: str = "Standard"
    objective: str = "Incident Containment & Action"
    selected_formats: Optional[List[str]] = None

@app.get("/", response_class=HTMLResponse)
async def serve_dashboard():
    index_file = STATIC_DIR / "index.html"
    if not index_file.exists():
        raise HTTPException(status_code=404, detail="Dashboard UI not found")
    with open(index_file, "r", encoding="utf-8") as f:
        return f.read()

@app.get("/api/metadata")
async def get_metadata():
    return {
        "sih_metadata": SIH_METADATA,
        "options": {
            "audiences": AUDIENCE_OPTIONS,
            "tones": TONE_OPTIONS,
            "languages": LANGUAGE_OPTIONS,
            "details": DETAIL_OPTIONS,
            "objectives": OBJECTIVE_OPTIONS,
            "formats": SUPPORTED_FORMATS
        }
    }

@app.get("/api/samples")
async def get_samples():
    samples = {}
    for filename in ["cert_in_advisory_sample.txt", "disaster_management_sample.txt", "ai_security_briefing_sample.txt"]:
        file_path = DATA_DIR / filename
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                key = filename.replace("_sample.txt", "")
                samples[key] = {
                    "filename": filename,
                    "content": f.read()
                }
    return samples

@app.post("/api/transform")
async def transform_content(req: TransformRequest):
    content_to_parse = req.source_text
    
    # URL ingestion support
    if req.source_url and not content_to_parse.strip():
        parsed = scrape_url(req.source_url)
    else:
        parsed = parse_text(content_to_parse)

    if not parsed.get("content"):
        raise HTTPException(status_code=400, detail="Source content is empty.")

    # 1. Build Content Brief ("Analyze once, reused by every output")
    operator_settings = {
        "audience": req.audience,
        "tone": req.tone,
        "language": req.language,
        "detail": req.detail,
        "objective": req.objective
    }
    brief = generate_content_brief(parsed, operator_settings)

    # 2. Run Parallel Format Generators
    formats = req.selected_formats or SUPPORTED_FORMATS
    generated_outputs = generate_all_formats(brief, formats)

    # 3. Run Grounded Claim Verifier against source chunks
    verification_report = verify_all_deliverables(generated_outputs, parsed["chunks"])

    # 4. Mint Cryptographic Block on Blockchain Provenance Ledger
    block = ledger.record_transformation(
        source_content=parsed["content"],
        brief_data=brief.model_dump(),
        settings_data=operator_settings,
        outputs_data=generated_outputs,
        verifier_report=verification_report,
        signer="TechStack_Operator_171612"
    )

    certificate = generate_audit_certificate(block, SIH_METADATA)

    return {
        "status": "success",
        "brief": brief.model_dump(),
        "deliverables": generated_outputs,
        "verification": verification_report,
        "ledger_block": block.model_dump(),
        "audit_certificate": certificate
    }

@app.get("/api/ledger")
async def get_ledger():
    is_valid, msg = ledger.verify_integrity()
    return {
        "chain_length": len(ledger.chain),
        "is_valid": is_valid,
        "integrity_status": msg,
        "blocks": ledger.get_chain_dict()
    }

@app.get("/api/certificate/{block_index}")
async def get_certificate(block_index: int):
    if block_index < 0 or block_index >= len(ledger.chain):
        raise HTTPException(status_code=404, detail="Block index not found")
    block = ledger.chain[block_index]
    return generate_audit_certificate(block, SIH_METADATA)

@app.post("/api/export")
async def export_deliverable(
    format_type: str = Form(...),
    title: str = Form(...),
    payload_json: str = Form(...)
):
    try:
        data = json.loads(payload_json)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    clean_title = "".join(c for c in title if c.isalnum() or c in (" ", "_", "-")).strip().replace(" ", "_")[:30]
    out_dir = EXPORTS_DIR

    if format_type == "video_package":
        srt_content = data.get("srt_subtitles", "")
        file_path = export_srt(srt_content, str(out_dir / f"{clean_title}.srt"))
        return FileResponse(file_path, filename=f"{clean_title}.srt", media_type="text/plain")

    elif format_type == "presentation_deck":
        file_path = export_pptx(data, str(out_dir / f"{clean_title}.pptx"))
        media_type = "application/vnd.openxmlformats-officedocument.presentationml.presentation" if file_path.endswith(".pptx") else "text/markdown"
        return FileResponse(file_path, filename=os.path.basename(file_path), media_type=media_type)

    elif format_type in ["advisory", "executive_summary"]:
        content = data.get("content", "")
        file_path = export_docx(title, content, str(out_dir / f"{clean_title}.docx"))
        media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document" if file_path.endswith(".docx") else "text/plain"
        return FileResponse(file_path, filename=os.path.basename(file_path), media_type=media_type)

    elif format_type == "pdf_report":
        content = data.get("content", "")
        file_path = export_pdf(title, content, str(out_dir / f"{clean_title}.pdf"))
        media_type = "application/pdf" if file_path.endswith(".pdf") else "text/html"
        return FileResponse(file_path, filename=os.path.basename(file_path), media_type=media_type)

    else:
        # Default JSON export
        file_path = out_dir / f"{clean_title}_{format_type}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return FileResponse(str(file_path), filename=f"{clean_title}_{format_type}.json", media_type="application/json")


if __name__ == "__main__":
    import uvicorn
    import socket

    def find_free_port(start_port=8000):
        for p in range(start_port, start_port + 20):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                if s.connect_ex(('127.0.0.1', p)) != 0:
                    return p
        return start_port

    target_port = find_free_port(8000)
    print("\n" + "=" * 65)
    print(" [VeriMorph] Starting Enterprise Web Server...")
    print(f" Access the Live Dashboard at: http://127.0.0.1:{target_port}")
    print(f" (Or http://localhost:{target_port})")
    print("=" * 65 + "\n")
    uvicorn.run(app, host="127.0.0.1", port=target_port)


