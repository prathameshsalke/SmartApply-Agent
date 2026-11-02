from __future__ import annotations

import json
from pathlib import Path

from app.config import DEFAULT_JOB_DESCRIPTION_PATH, DEFAULT_RESULTS_PATH, DEFAULT_RESUME_DIR, DEFAULT_USER_PROFILE_PATH
from app.utils.form_filler import run_demo_application


def main():
    user_profile_path = DEFAULT_USER_PROFILE_PATH
    job_description_path = DEFAULT_JOB_DESCRIPTION_PATH
    resume_dir = DEFAULT_RESUME_DIR
    results_path = DEFAULT_RESULTS_PATH

    result = run_demo_application(
        user_profile_path=user_profile_path,
        job_description_path=job_description_path,
        resume_dir=resume_dir,
        results_path=results_path,
    )

    print("SmartApply-Agent Demo Run")
    print("=" * 50)
    print(f"Selected Resume: {result['selected_resume']}")
    print(f"ATS Score: {result['ats_score']}")
    print(f"Status: {result['status']}")
    print(f"Matched Keywords: {', '.join(result.get('matched_keywords', [])) or 'None'}")
    print(f"Warnings: {result.get('warnings', [])}")
    print(f"Result saved to: {results_path}")
    print("=" * 50)

    return result


if __name__ == "__main__":
    main()
