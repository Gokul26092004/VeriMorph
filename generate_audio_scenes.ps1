Add-Type -AssemblyName System.Speech

$voice = New-Object System.Speech.Synthesis.SpeechSynthesizer
$voice.SelectVoiceByHints([System.Speech.Synthesis.VoiceGender]::Neutral)
$voice.Rate = 0

$scenes = @(
    "Welcome to VeriMorph A I, an enterprise platform for automated, auditable content transformation. In this demonstration, we will show how VeriMorph transforms raw threat intelligence and complex technical reports into seven synchronized deliverables with zero hallucination and complete cryptographic trust.",
    "Step one: Source Ingestion and Operator Controls. In the Operator Control Panel on the left, we input a technical advisory regarding an active perimeter gateway exploit. Operators can dynamically select the target audience, tone, language, and choose from seven distribution channels.",
    "Step two: The Unified Content Brief. Instead of separate uncoordinated prompts that cause fact drift, VeriMorph analyzes the source once, synthesizing a structured Content Brief. Every ground-truth fact is anchored with citations to exact source chunks, alongside extracted threat entities and mitigation action directives.",
    "Step three: Parallel Multi-Channel Generation. In less than thirty milliseconds, the platform generates seven synchronized formats: a video package with scene storyboard and millisecond-accurate S R T subtitles, an official advisory, a LinkedIn briefing, an X thread, an S V G infographic, an executive summary, and a six-slide presentation with speaker notes.",
    "Step four: Grounded Claim Verifier. To protect operational communications against L L M confabulation, our verifier audits every generated statement against original source passages. On this advisory, the system achieved a 94.2 percent Factual Groundedness Index with zero ungrounded hallucinations.",
    "Step five: Blockchain Provenance and Instant Export. Every transformation hashes the source, settings, outputs, and verifier report into a Merkle tree and mints an immutable block on the S H A 256 ledger. Operators can download verifiable audit certificates and export directly to P P T X, D O C X, P D F, and S R T files."
)

for ($i = 0; $i -lt $scenes.Length; $i++) {
    $outPath = "scene_$($i + 1).wav"
    $voice.SetOutputToWaveFile($outPath)
    $voice.Speak($scenes[$i])
    Write-Host "Generated $outPath"
}

$voice.Dispose()
Write-Host "ALL_SCENES_SYNTHESIZED_SUCCESS"
