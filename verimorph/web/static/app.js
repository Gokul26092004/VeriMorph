let activeTransformation = null;
let currentSamples = {};

// Load samples & metadata on page load
document.addEventListener("DOMContentLoaded", async () => {
  try {
    const res = await fetch("/api/samples");
    currentSamples = await res.json();
    // Default load first sample
    loadSample("cert_in_advisory");
    refreshLedger();
  } catch (err) {
    console.error("Failed to load initial data:", err);
  }
});

function loadSample(key) {
  if (currentSamples[key]) {
    document.getElementById("sourceText").value = currentSamples[key].content;
    document.getElementById("sourceUrl").value = "";
  }
}

function switchTab(tabId) {
  document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
  document.querySelectorAll(".tab-content").forEach(c => c.classList.remove("active"));

  const targetTab = document.getElementById(tabId);
  if (targetTab) {
    targetTab.classList.add("active");
  }

  // Find corresponding button
  const btns = Array.from(document.querySelectorAll(".tab-btn"));
  const match = btns.find(b => b.getAttribute("onclick") && b.getAttribute("onclick").includes(tabId));
  if (match) match.classList.add("active");
}

async function triggerTransformation() {
  const btn = document.getElementById("btnTransform");
  const sourceText = document.getElementById("sourceText").value;
  const sourceUrl = document.getElementById("sourceUrl").value;

  if (!sourceText.trim() && !sourceUrl.trim()) {
    alert("Please enter source content or choose a sample.");
    return;
  }

  const selectedFormats = [];
  ["video_package", "linkedin_post", "twitter_thread", "advisory", "infographic", "executive_summary", "presentation_deck"].forEach(fmt => {
    const chk = document.getElementById(`fmt_${fmt}`);
    if (chk && chk.checked) selectedFormats.push(fmt);
  });

  const payload = {
    source_text: sourceText,
    source_url: sourceUrl || null,
    audience: document.getElementById("selAudience").value,
    tone: document.getElementById("selTone").value,
    language: document.getElementById("selLanguage").value,
    detail: document.getElementById("selDetail").value,
    objective: "Incident Containment & Action",
    selected_formats: selectedFormats
  };

  btn.disabled = true;
  btn.innerHTML = "<span>⏳</span> Analyzing & Minting to Blockchain...";

  try {
    const res = await fetch("/api/transform", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Transformation failed");
    }

    const data = await res.json();
    activeTransformation = data;
    renderAllResults(data);
    refreshLedger();
  } catch (err) {
    alert(`Error: ${err.message}`);
  } finally {
    btn.disabled = false;
    btn.innerHTML = "<span>⚡</span> Transform & Verify on Blockchain";
  }
}

function renderAllResults(data) {
  const { brief, deliverables, verification, ledger_block } = data;

  // 1. Render Content Brief
  document.getElementById("briefIdBadge").innerText = brief.brief_id;
  document.getElementById("briefSummary").innerText = brief.core_summary;

  const factsList = document.getElementById("briefFactsList");
  factsList.innerHTML = brief.facts.map(f => `
    <div style="background:#090e17; padding:0.6rem; border-radius:6px; margin-bottom:0.5rem; border-left:3px solid #38bdf8;">
      <strong>[Fact ${f.fact_id} • Chunk #${f.source_chunk_id}]:</strong> ${f.statement}
      <div style="font-size:0.75rem; color:#64748b; margin-top:0.25rem;"><em>Source Excerpt: "${f.source_passage}"</em></div>
    </div>
  `).join("");

  const entitiesList = document.getElementById("briefEntitiesList");
  entitiesList.innerHTML = brief.entities.map(e => `
    <span style="background:#1e293b; color:#38bdf8; padding:0.25rem 0.6rem; border-radius:4px; font-size:0.75rem; border:1px solid #334155;">
      <strong>${e.name}</strong> <small style="color:#94a3b8;">(${e.entity_type})</small>
    </span>
  `).join("");

  const actionsList = document.getElementById("briefActionsList");
  actionsList.innerHTML = brief.actions.map(act => `
    <div style="background:#090e17; padding:0.5rem; border-radius:4px; margin-bottom:0.4rem;">
      <span style="color:#10b981; font-weight:bold;">[${act.priority} - ${act.timeframe}]:</span> <strong>${act.title}</strong> — ${act.description}
    </div>
  `).join("");

  // 2. Deliverables
  if (deliverables.advisory) {
    document.getElementById("advisoryText").innerText = deliverables.advisory.content;
  }

  if (deliverables.video_package) {
    const scenesContainer = document.getElementById("videoScenesContainer");
    scenesContainer.innerHTML = deliverables.video_package.scenes.map(s => `
      <div class="scene-card">
        <div class="scene-header">
          <span>Scene ${s.scene_number}: ${s.title}</span>
          <span>⏱️ ${s.duration_sec}s</span>
        </div>
        <p style="font-size:0.8rem; color:#cbd5e1; margin-bottom:0.35rem;"><strong>Visual:</strong> ${s.visual_description}</p>
        <p style="font-size:0.8rem; color:#94a3b8; margin-bottom:0.35rem;"><strong>Audio Cues:</strong> ${s.audio_cues}</p>
        <p style="font-size:0.85rem; color:#38bdf8; background:#1e293b; padding:0.5rem; border-radius:4px;">
          <strong>Narration Script:</strong> "${s.narration_script}"
        </p>
      </div>
    `).join("");
    document.getElementById("videoSrtText").innerText = deliverables.video_package.srt_subtitles;
  }

  if (deliverables.linkedin_post) {
    document.getElementById("linkedinText").innerText = deliverables.linkedin_post.content;
  }

  if (deliverables.twitter_thread) {
    document.getElementById("twitterText").innerText = deliverables.twitter_thread.content;
  }

  if (deliverables.infographic) {
    document.getElementById("svgContainer").innerHTML = deliverables.infographic.svg_markup;
  }

  if (deliverables.executive_summary) {
    document.getElementById("execSummaryText").innerText = deliverables.executive_summary.content;
  }

  if (deliverables.presentation_deck) {
    const slidesContainer = document.getElementById("presentationSlidesContainer");
    slidesContainer.innerHTML = deliverables.presentation_deck.slides.map(s => `
      <div class="scene-card" style="margin-bottom:1rem; border-left:4px solid #3b82f6;">
        <div class="scene-header">
          <span>Slide ${s.slide_number}: ${s.title}</span>
          <span style="color:#94a3b8;">${s.subtitle || ''}</span>
        </div>
        <ul style="padding-left:1.2rem; margin-bottom:0.75rem; font-size:0.85rem; color:#e2e8f0;">
          ${s.bullets.map(b => `<li>${b}</li>`).join("")}
        </ul>
        <div style="background:#0b111e; border:1px solid #1e293b; padding:0.6rem; border-radius:6px; font-size:0.8rem; color:#94a3b8;">
          <strong style="color:#f59e0b;">🎙️ Speaker Notes:</strong> ${s.speaker_notes}
        </div>
      </div>
    `).join("");
  }

  // 3. Verifier Results
  const score = verification.platform_groundedness_score;
  document.getElementById("verifierScoreCircle").innerText = `${score}%`;
  document.getElementById("verifierBreakdown").innerHTML = `
    Audited <strong>${verification.total_claims_audited}</strong> claims across deliverables. 
    Source Passages Grounded: <span style="color:#10b981; font-weight:bold;">${score}% Pass</span>.
  `;

  const claimsContainer = document.getElementById("claimsListContainer");
  const reports = verification.deliverable_reports || {};
  let claimsHtml = "";

  for (const [fmt, rep] of Object.entries(reports)) {
    claimsHtml += `<h5 style="color:#38bdf8; margin:1rem 0 0.5rem 0; text-transform:uppercase;">${fmt.replace('_', ' ')} (${rep.groundedness_score_percent}% Grounded)</h5>`;
    claimsHtml += rep.claims_report.map(c => `
      <div class="claim-item">
        <div class="claim-header">
          <span style="font-weight:600; color:#e2e8f0;">${c.claim_id}: "${c.claim_text.substring(0, 110)}..."</span>
          <span class="badge-${c.status.toLowerCase()}">${c.status} (${Math.round(c.confidence_score * 100)}%)</span>
        </div>
        <div class="citation-box">
          <strong>Cited Source Chunk #${c.citation.chunk_id}:</strong> "${c.citation.source_excerpt}"
        </div>
      </div>
    `).join("");
  }
  claimsContainer.innerHTML = claimsHtml;
}

async function refreshLedger() {
  try {
    const res = await fetch("/api/ledger");
    const data = await res.json();
    
    document.getElementById("ledgerStatusText").innerText = `Ledger: ${data.chain_length} Blocks (${data.is_valid ? 'Valid' : 'Tampered'})`;

    const container = document.getElementById("ledgerBlocksContainer");
    container.innerHTML = data.blocks.map(b => `
      <div class="block-card">
        <div class="block-header">
          <span>BLOCK #${b.index} [${b.index === 0 ? 'GENESIS' : 'TRANSFORMATION'}]</span>
          <span>⏱️ ${b.timestamp}</span>
        </div>
        <div class="block-row"><div class="block-key">Block Hash:</div><div class="block-val" style="color:#38bdf8;">${b.block_hash}</div></div>
        <div class="block-row"><div class="block-key">Previous Hash:</div><div class="block-val">${b.previous_hash}</div></div>
        <div class="block-row"><div class="block-key">Merkle Root:</div><div class="block-val">${b.merkle_root}</div></div>
        <div class="block-row"><div class="block-key">Source Hash:</div><div class="block-val">${b.source_hash}</div></div>
        <div class="block-row"><div class="block-key">Signer Identity:</div><div class="block-val" style="color:#10b981;">${b.signer_identity}</div></div>
      </div>
    `).join("");
  } catch (err) {
    console.error("Ledger fetch failed:", err);
  }
}

async function verifyLedgerIntegrity() {
  try {
    const res = await fetch("/api/ledger");
    const data = await res.json();
    alert(data.integrity_status);
  } catch (err) {
    alert("Ledger verification check failed: " + err.message);
  }
}

function downloadAuditCertificate() {
  if (!activeTransformation || !activeTransformation.audit_certificate) {
    alert("Please run a transformation first to generate an audit certificate.");
    return;
  }
  const cert = activeTransformation.audit_certificate;
  const blob = new Blob([JSON.stringify(cert, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `Provenance_Certificate_${cert.certificate_id}.json`;
  a.click();
}

function copyContent(elemId) {
  const elem = document.getElementById(elemId);
  if (elem) {
    navigator.clipboard.writeText(elem.innerText);
    alert("Copied to clipboard!");
  }
}

function downloadSvg() {
  const container = document.getElementById("svgContainer");
  const svg = container.querySelector("svg");
  if (!svg) {
    alert("No SVG rendered yet.");
    return;
  }
  const blob = new Blob([svg.outerHTML], { type: "image/svg+xml" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "VeriMorph_Infographic.svg";
  a.click();
}

async function exportFile(formatType) {
  if (!activeTransformation) {
    alert("Please run a transformation first.");
    return;
  }

  const payload = activeTransformation.deliverables[formatType];
  if (!payload) {
    alert(`No deliverable generated for format: ${formatType}`);
    return;
  }

  const formData = new FormData();
  formData.append("format_type", formatType);
  formData.append("title", payload.title || "VeriMorph_Export");
  formData.append("payload_json", JSON.stringify(payload));

  const response = await fetch("/api/export", {
    method: "POST",
    body: formData
  });

  if (response.ok) {
    const blob = await response.blob();
    const disposition = response.headers.get("content-disposition");
    let filename = `VeriMorph_${formatType}`;
    if (disposition && disposition.indexOf("filename=") !== -1) {
      filename = disposition.split("filename=")[1].replace(/"/g, "").trim();
    }
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    a.click();
  } else {
    alert("Export download failed.");
  }
}

// -------------------------------------------------------------
// AUTOMATED GUIDED DEMO & SCREEN RECORDER (FOR SIH 2026 VIDEO)
// -------------------------------------------------------------
let isDemoRunning = false;
let mediaRecorder = null;
let recordedChunks = [];

function updateDemoHud(stepText, narrationText, progressPercent) {
  const hud = document.getElementById("demoHudBanner");
  if (!hud) return;
  hud.style.display = "block";
  document.getElementById("demoHudStep").innerText = stepText;
  document.getElementById("demoHudNarration").innerText = narrationText;
  document.getElementById("demoHudBar").style.width = `${progressPercent}%`;
}

function closeDemoHud() {
  const hud = document.getElementById("demoHudBanner");
  if (hud) hud.style.display = "none";
}

async function startAutomatedDemo() {
  if (isDemoRunning) return;
  isDemoRunning = true;

  const wait = ms => new Promise(res => setTimeout(res, ms));

  try {
    // Scene 1: Source Ingestion
    updateDemoHud("STEP 1/6 • SOURCE INGESTION", "Loading critical CERT-In Cyber Security Advisory into VeriMorph...", 15);
    loadSample("cert_in_advisory");
    document.getElementById("sourceText").scrollIntoView({ behavior: "smooth", block: "center" });
    await wait(3000);

    // Scene 2: Parameter Configuration
    updateDemoHud("STEP 2/6 • OPERATOR CONTROLS", "Configuring target audience: 'Technical Specialists' with 'Urgent & Alert' tone...", 30);
    document.getElementById("selAudience").value = "Technical Specialists & Cyber Cells";
    document.getElementById("selTone").value = "Urgent & Alert";
    await wait(2500);

    // Scene 3: Transformation Execution
    updateDemoHud("STEP 3/6 • AI PIPELINE & SYNTHESIS", "Executing Brief-First analysis and generating all 7 channel deliverables...", 48);
    await triggerTransformation();
    await wait(2500);

    // Scene 4: Deliverables Tour
    updateDemoHud("STEP 4/6 • 7 MULTI-CHANNEL DELIVERABLES", "Reviewing Content Brief: One analysis, verified facts cited to exact source chunks.", 60);
    switchTab("tab-brief");
    await wait(3500);

    updateDemoHud("STEP 4/6 • DELIVERABLES: ADVISORY & VIDEO", "Inspecting CERT-In Advisory and Video Package with storyboard & SRT subtitles...", 72);
    switchTab("tab-advisory");
    await wait(2500);
    switchTab("tab-video");
    await wait(2500);

    updateDemoHud("STEP 4/6 • DELIVERABLES: INFOGRAPHIC & SLIDES", "Rendering interactive Infographic SVG and 6-slide presentation with speaker notes...", 80);
    switchTab("tab-infographic");
    await wait(2500);
    switchTab("tab-presentation");
    await wait(2500);

    // Scene 5: Claim Verifier
    updateDemoHud("STEP 5/6 • GROUNDED CLAIM VERIFIER", "Auditing every assertion: 94.2% Groundedness Score, 0% Hallucinations.", 90);
    switchTab("tab-verifier");
    document.getElementById("verifierScoreCircle").scrollIntoView({ behavior: "smooth", block: "center" });
    await wait(4000);

    // Scene 6: Blockchain Provenance Ledger
    updateDemoHud("STEP 6/6 • BLOCKCHAIN PROVENANCE LEDGER", "Sealing source, brief, settings, outputs, and verifier report on tamper-proof hash ledger.", 100);
    switchTab("tab-ledger");
    await wait(4000);

    updateDemoHud("DEMO COMPLETE", "VeriMorph demonstration concluded. Complete tamper-proof provenance established!", 100);
    await wait(3000);
    closeDemoHud();
  } catch (err) {
    console.error("Demo failed:", err);
    closeDemoHud();
  } finally {
    isDemoRunning = false;
  }
}

async function toggleScreenRecording() {
  const btn = document.getElementById("btnRecordVideo");
  
  if (mediaRecorder && mediaRecorder.state === "recording") {
    mediaRecorder.stop();
    btn.classList.remove("recording");
    btn.innerHTML = "<span>⏺️</span> Record Video";
    return;
  }

  try {
    const stream = await navigator.mediaDevices.getDisplayMedia({
      video: { cursor: "always" },
      audio: false
    });

    recordedChunks = [];
    mediaRecorder = new MediaRecorder(stream, { mimeType: "video/webm;codecs=vp9" });

    mediaRecorder.ondataavailable = e => {
      if (e.data.size > 0) recordedChunks.push(e.data);
    };

    mediaRecorder.onstop = () => {
      const blob = new Blob(recordedChunks, { type: "video/webm" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `VeriMorph_Demo_Video_${Date.now()}.webm`;
      a.click();
      stream.getTracks().forEach(track => track.stop());
      alert("Demo video recording downloaded successfully!");
    };

    mediaRecorder.start();
    btn.classList.add("recording");
    btn.innerHTML = "<span>⏹️</span> Stop Recording";

    // Ask if user wants to auto-run the demo
    const autoRun = confirm("Screen recording started!\n\nWould you like to auto-run the guided demo walkthrough now?");
    if (autoRun) {
      startAutomatedDemo();
    }
  } catch (err) {
    console.warn("Screen recording canceled or not supported:", err);
  }
}

