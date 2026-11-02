from __future__ import annotations

from pathlib import Path
from typing import Dict, List


def generate_form_payload(candidate: dict, resume_path: str, ats_score: float, job_title: str) -> dict:
    required_fields = {
        "full_name": candidate.get("full_name"),
        "email": candidate.get("email"),
        "phone": candidate.get("phone"),
        "location": candidate.get("location"),
        "gender": candidate.get("gender"),
        "education": candidate.get("education", [])[0] if candidate.get("education") else "",
        "experience_years": candidate.get("experience_years"),
        "skills": candidate.get("skills", []),
        "resume_path": resume_path,
        "job_title": job_title,
        "ats_score": ats_score,
    }

    return required_fields


def evaluate_missing_fields(candidate: dict, required_fields: List[str]) -> List[str]:
    missing = []
    for field in required_fields:
        value = candidate.get(field)
        if value in (None, "", [], {}):
            missing.append(field)
    return missing


def simulate_application(candidate: dict, resume_path: str, ats_score: float, job_title: str, company_name: str) -> dict:
    required_fields = [
        "full_name",
        "email",
        "phone",
        "location",
        "gender",
        "education",
        "experience_years",
        "skills",
    ]

    missing_fields = evaluate_missing_fields(candidate, required_fields)
    warnings = []

    if missing_fields:
        warnings.append(f"Missing values for: {', '.join(missing_fields)}")

    application_record = {
        "job_title": job_title,
        "company_name": company_name,
        "selected_resume": Path(resume_path).name,
        "ats_score": round(ats_score, 2),
        "status": "applied" if not missing_fields else "requires_user_input",
        "filled_fields": generate_form_payload(candidate, resume_path, ats_score, job_title),
        "warnings": warnings,
        "notes": [
            "Resume selected from best ATS match",
            "Application form prepared using candidate profile",
            "No CAPTCHA or blocking challenge detected in demo mode",
        ],
    }

    return application_record
