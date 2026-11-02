from __future__ import annotations

import csv
import json
from pathlib import Path

from app.config import DEFAULT_RESULTS_PATH


def ensure_parent_dir(path: str | Path) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def load_json(path: str | Path, default=None):
    p = Path(path)
    if not p.exists():
        return default
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def save_json(data, path: str | Path):
    p = ensure_parent_dir(path)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return str(p)


def save_result(result: dict, path: str | Path = DEFAULT_RESULTS_PATH):
    p = ensure_parent_dir(path)
    existing = load_json(p, [])
    if not isinstance(existing, list):
        existing = [existing]
    existing.append(result)
    save_json(existing, p)
    return str(p)


def append_result(result: dict, path: str | Path):
    p = Path(path)
    existing = load_json(p, [])
    if not isinstance(existing, list):
        existing = [existing]
    existing.append(result)
    save_json(existing, p)
    return str(p)


def save_csv_summary(rows: list[dict], path: str | Path):
    p = ensure_parent_dir(path)
    fieldnames = [
        "job_title",
        "company_name",
        "selected_resume",
        "ats_score",
        "status",
        "matched_keywords",
        "warnings",
    ]

    with open(p, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({
                "job_title": row.get("job_title", ""),
                "company_name": row.get("company_name", ""),
                "selected_resume": row.get("selected_resume", ""),
                "ats_score": row.get("ats_score", 0),
                "status": row.get("status", ""),
                "matched_keywords": ", ".join(row.get("matched_keywords", [])),
                "warnings": "; ".join(row.get("warnings", [])),
            })

    return str(p)


def export_summary_csv(rows: list[dict], path: str | Path):
    return save_csv_summary(rows, path)
