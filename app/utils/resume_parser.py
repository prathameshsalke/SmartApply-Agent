from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple

from app.config import DEFAULT_RESUME_DIR


def load_resume_text(path: str | Path) -> str:
    p = Path(path)
    return p.read_text(encoding="utf-8")


def extract_email(text: str) -> str:
    match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    return match.group(0) if match else ""


def extract_phone(text: str) -> str:
    match = re.search(r"\+?\d[\d\s().-]{7,}\d", text)
    return match.group(0).strip() if match else ""


def extract_name(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    for line in lines[:5]:
        if len(line.split()) >= 2 and not re.search(r"(resume|cv|profile)", line.lower()):
            return line
    return "Unknown"


def extract_experience_years(text: str) -> int:
    patterns = [
        r"(\d+)\s*\+?\s*years?\s*of\s*experience",
        r"(\d+)\s*years?\s*(?:in|of|experience)",
        r"(\d+)\s*\+?\s*yrs?\s*experience",
    ]
    matches = []
    for pattern in patterns:
        for match in re.finditer(pattern, text, flags=re.IGNORECASE):
            matches.append(int(match.group(1)))
    return max(matches) if matches else 0


def extract_skills(text: str) -> List[str]:
    common_skills = {
        "python",
        "fastapi",
        "flask",
        "django",
        "sql",
        "postgresql",
        "mysql",
        "mongodb",
        "javascript",
        "react",
        "node",
        "docker",
        "kubernetes",
        "aws",
        "gcp",
        "azure",
        "rest api",
        "apis",
        "html",
        "css",
        "git",
        "ci/cd",
        "machine learning",
        "data analysis",
        "excel",
        "power bi",
        "tableau",
        "linux",
        "typescript",
        "agile",
        "spark",
        "pandas",
        "numpy",
        "scikit-learn",
    }

    lower_text = text.lower()
    found = [skill for skill in sorted(common_skills) if skill in lower_text]
    return found


def extract_education(text: str) -> List[str]:
    education_patterns = [
        r"B\.Tech[^\n]*",
        r"B\.E\.[^\n]*",
        r"Bachelor[^\n]*",
        r"Master[^\n]*",
        r"M\.Tech[^\n]*",
        r"MBA[^\n]*",
        r"Diploma[^\n]*",
    ]
    found = []
    for pattern in education_patterns:
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        for item in matches:
            found.append(item.strip())
    return found[:5]


def parse_resume(path: str | Path) -> Dict[str, object]:
    text = load_resume_text(path)
    name = extract_name(text)
    email = extract_email(text)
    phone = extract_phone(text)
    skills = extract_skills(text)
    experience_years = extract_experience_years(text)
    education = extract_education(text)

    return {
        "path": str(path),
        "name": name,
        "email": email,
        "phone": phone,
        "skills": skills,
        "experience_years": experience_years,
        "education": education,
        "text": text,
    }


def load_demo_resumes(resume_dir: str | Path = DEFAULT_RESUME_DIR) -> List[Dict[str, object]]:
    resume_dir = Path(resume_dir)
    resumes = []
    for path in sorted(resume_dir.glob("*.txt")):
        resumes.append(parse_resume(path))
    return resumes


def load_demo_user(path: str | Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
