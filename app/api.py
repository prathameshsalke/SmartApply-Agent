from __future__ import annotations

import json
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel

from app.config import DEFAULT_JOB_DESCRIPTION_PATH
from app.utils.form_filler import run_demo_application


class CandidateInput(BaseModel):
    full_name: str
    email: str
    phone: str
    location: str
    gender: str
    education: list[str] = []
    experience_years: int = 0
    skills: list[str] = []
    preferred_roles: list[str] = []
    linkedin: str | None = None
    portfolio: str | None = None


class ApplyRequest(BaseModel):
    job_url: str
    company_name: str
    job_title: str
    job_description: str
    candidate: CandidateInput


app = FastAPI(title="SmartApply-Agent API", version="1.0.0")


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "SmartApply-Agent API is running"}


@app.post("/apply")
def apply_for_job(payload: ApplyRequest):
    job_description = payload.job_description
    candidate = payload.candidate.model_dump()

    # Use the demo job description if the caller passes a blank string.
    if not job_description.strip():
        job_description = DEFAULT_JOB_DESCRIPTION_PATH.read_text(encoding="utf-8")

    result = {
        "job_url": payload.job_url,
        "company_name": payload.company_name,
        "job_title": payload.job_title,
        "status": "demo_simulation",
        "candidate": candidate,
        "job_description": job_description,
        "message": "This is a demo simulation. Connect real browser automation for live job portals.",
    }

    return result
