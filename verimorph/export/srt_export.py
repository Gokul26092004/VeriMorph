import os
from pathlib import Path

def export_srt(srt_content: str, output_path: str) -> str:
    """
    Writes SRT subtitle content to disk.
    """
    path = Path(output_path)
    os.makedirs(path.parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(srt_content)
    return str(path)
