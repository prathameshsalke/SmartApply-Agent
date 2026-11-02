from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

from app.config import DEFAULT_JOB_DESCRIPTION_PATH, DEFAULT_RESULTS_PATH, DEFAULT_RESUME_DIR, DEFAULT_USER_PROFILE_PATH
from app.models import CandidateProfile
from app.utils.application_tracker import simulate_application
from app.utils.ats_matcher import score_keyword_overlap
from app.utils.resume_parser import load_demo_resumes, load_demo_user


def load_demo_user_profile(path: str | Path = DEFAULT_USER_PROFILE_PATH) -> CandidateProfile:
    data = load_demo_user(path)
    return CandidateProfile(
        full_name=data["full_name"],
        email=data["email"],
        phone=data["phone"],
        location=data["location"],
        gender=data["gender"],
        education=data.get("education", []),
        experience_years=data.get("experience_years", 0),
        skills=data.get("skills", []),
        preferred_roles=data.get("preferred_roles", []),
        linkedin=data.get("linkedin"),
        portfolio=data.get("portfolio"),
    )


def choose_best_resume(job_description: str, resume_dir: str | Path = DEFAULT_RESUME_DIR) -> dict:
    resumes = load_demo_resumes(resume_dir)
    results = []

    for resume in resumes:
        score_data = score_keyword_overlap(job_description, resume["text"])
        results.append({
            "resume": resume,
            "score": score_data["score"],
            "matched_keywords": score_data["matched_keywords"],
            "missing_keywords": score_data["missing_keywords"],
            "overlap_count": score_data["overlap_count"],
            "total_possible": score_data["total_possible"],
        })

    best = max(results, key=lambda item: item["score"])
    best["resume"]["ats_score"] = best["score"]
    return best


def run_demo_application(
    user_profile_path: str | Path = DEFAULT_USER_PROFILE_PATH,
    job_description_path: str | Path = DEFAULT_JOB_DESCRIPTION_PATH,
    resume_dir: str | Path = DEFAULT_RESUME_DIR,
    results_path: str | Path = DEFAULT_RESULTS_PATH,
):
    user = load_demo_user(user_profile_path)
    with open(job_description_path, "r", encoding="utf-8") as f:
        job_description = f.read()

    best = choose_best_resume(job_description, resume_dir)
    resume_path = best["resume"]["path"]
    ats_score = best["score"]
    company_name = "Nova Systems"
    job_title = "Python Backend Engineer"

    result = simulate_application(user, resume_path, ats_score, job_title, company_name)
    result["matched_keywords"] = best["matched_keywords"]
    result["missing_keywords"] = best["missing_keywords"]
    result["job_description"] = job_description
    result["best_resume_name"] = best["resume"]["name"]

    results_dir = Path(results_path).parent
    results_dir.mkdir(parents=True, exist_ok=True)
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump([result], f, indent=2)

    return result
