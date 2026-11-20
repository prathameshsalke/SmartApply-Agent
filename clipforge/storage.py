from __future__ import annotations

import json
import re
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "clipforge"
UPLOAD_DIR = DATA_DIR / "uploads"
EXPORT_DIR = DATA_DIR / "exports"
JOBS_FILE = DATA_DIR / "jobs.json"
MAX_UPLOAD_BYTES = 2 * 1024 * 1024 * 1024
ALLOWED_SUFFIXES = {".mp4", ".mov", ".mkv", ".webm", ".m4v"}

for directory in (UPLOAD_DIR, EXPORT_DIR):
    directory.mkdir(parents=True, exist_ok=True)


def read_jobs() -> dict:
    if not JOBS_FILE.exists():
        return {}
    try:
        return json.loads(JOBS_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def write_jobs(jobs: dict) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    temp = JOBS_FILE.with_suffix(".tmp")
    temp.write_text(json.dumps(jobs, indent=2), encoding="utf-8")
    temp.replace(JOBS_FILE)


def safe_name(filename: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", Path(filename).name).strip("._")
    return cleaned[:100] or f"video{Path(filename).suffix.lower()}"


def new_id() -> str:
    return uuid.uuid4().hex
