import csv
import json
from pathlib import Path

from app.config import DEFAULT_RESULTS_PATH


def ensure_parent_dir(path: str | Path):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def save_result(result: dict, path: str | Path = DEFAULT_RESULTS_PATH):
    p = ensure_parent_dir(path)
    existing = []
    if p.exists():
        try:
            existing = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            existing = []

    if isinstance(existing, dict):
        existing = [existing]

    existing.append(result)
    p.write_text(json.dumps(existing, indent=2), encoding="utf-8")
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
