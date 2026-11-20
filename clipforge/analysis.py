from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Any

from .storage import DATA_DIR


class MediaError(RuntimeError):
    pass


def probe_duration(path: Path) -> float:
    """Return media duration in seconds using the system ffprobe binary."""
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(path)],
            capture_output=True,
            text=True,
            check=True,
            timeout=30,
        )
        duration = float(json.loads(result.stdout)["format"]["duration"])
    except (OSError, subprocess.SubprocessError, ValueError, KeyError, json.JSONDecodeError) as exc:
        raise MediaError("Could not read this video. Install FFmpeg and provide a valid video file.") from exc
    if duration <= 0:
        raise MediaError("The uploaded video has no valid duration.")
    return duration


def transcribe(path: Path) -> list[dict[str, Any]]:
    """Transcribe locally with Whisper; model weights are downloaded on first use."""
    try:
        import whisper
    except ImportError as exc:
        raise MediaError("Whisper is not installed. Install optional dependencies with: pip install -r requirements-clipforge.txt") from exc
    model = whisper.load_model("base")
    result = model.transcribe(str(path), verbose=False)
    return [
        {"start": float(s["start"]), "end": float(s["end"]), "text": str(s["text"]).strip()}
        for s in result.get("segments", []) if str(s.get("text", "")).strip()
    ]


_HOOK_WORDS = {"wow", "wait", "finally", "secret", "insane", "amazing", "never", "best", "worst", "why", "how", "can't", "can't", "look", "crazy", "important", "actually"}


def suggest_clips(segments: list[dict[str, Any]], duration: float, limit: int = 20) -> list[dict[str, Any]]:
    """Rank overlapping transcript windows with a transparent heuristic score."""
    if not segments:
        raise MediaError("No speech was detected. Try another source video or add clips manually in a future version.")
    windows: list[dict[str, Any]] = []
    # Group adjacent speech segments into windows of roughly 25–45 seconds.
    i = 0
    while i < len(segments):
        start = max(0.0, float(segments[i]["start"]) - 1.5)
        end_index = i
        while end_index + 1 < len(segments) and float(segments[end_index]["end"]) - start < 35:
            end_index += 1
            if float(segments[end_index]["end"]) - start >= 24:
                break
        end = min(duration, float(segments[end_index]["end"]) + 1.5)
        if end - start >= 8:
            text = " ".join(str(s["text"]).strip() for s in segments[i:end_index + 1]).strip()
            words = re.findall(r"[\w']+", text.lower())
            hook_count = sum(word in _HOOK_WORDS for word in words)
            punctuation = sum(text.count(ch) for ch in "?!")
            density = min(len(words) / max(end - start, 1), 2.5)
            score = min(97, max(35, round(48 + hook_count * 6 + punctuation * 2 + density * 8)))
            windows.append({"start": round(start, 2), "end": round(end, 2), "duration": round(end - start, 2), "transcript": text, "score": score})
        i = end_index + 1
    # Return highest-scoring suggestions with minimal overlap, then restore chronological order.
    selected: list[dict[str, Any]] = []
    for item in sorted(windows, key=lambda x: x["score"], reverse=True):
        if all(item["end"] <= other["start"] or item["start"] >= other["end"] for other in selected):
            selected.append(item)
        if len(selected) >= max(1, min(limit, 50)):
            break
    return sorted(selected, key=lambda x: x["start"])


def make_metadata(transcript: str) -> dict[str, Any]:
    words = re.findall(r"[A-Za-z][A-Za-z'-]{3,}", transcript)
    frequent: dict[str, int] = {}
    stop = {"that", "this", "with", "from", "have", "your", "about", "there", "what", "when", "they", "just", "like", "really", "because", "would", "could", "should", "were", "then", "them", "will", "into", "some", "make", "know", "think", "very", "been", "being", "also"}
    for word in words:
        key = word.lower()
        if key not in stop:
            frequent[key] = frequent.get(key, 0) + 1
    tags = [f"#{word}" for word, _ in sorted(frequent.items(), key=lambda pair: pair[1], reverse=True)[:5]]
    title = " ".join(words[:8]).strip() or "A moment worth sharing"
    return {"title": title[:90], "description": f"A highlight from the original video.\n\n{transcript[:350].strip()}", "tags": tags}
