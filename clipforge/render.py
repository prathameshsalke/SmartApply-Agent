from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

from .storage import EXPORT_DIR


def render_clip(job_id: str, clip_id: int, source: Path, start: float, end: float, layout: str = "vertical") -> Path:
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("FFmpeg is required. Install it and ensure ffmpeg is on PATH.")
    output = EXPORT_DIR / f"{job_id}-{clip_id}.mp4"
    duration = end - start
    if duration <= 0:
        raise ValueError("Clip end must be after its start.")
    filters = {
        "vertical": "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
        "square": "scale=1080:1080:force_original_aspect_ratio=increase,crop=1080:1080",
        "original": "scale=1920:-2:force_original_aspect_ratio=decrease",
    }
    if layout not in filters:
        raise ValueError("Unsupported layout. Choose vertical, square, or original.")
    command = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", str(start), "-i", str(source), "-t", str(duration), "-vf", filters[layout], "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-c:a", "aac", "-movflags", "+faststart", str(output)]
    subprocess.run(command, check=True, capture_output=True, timeout=1800)
    return output
