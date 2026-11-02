import re
from collections import Counter


def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s+/.-]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_keywords(text: str, min_length: int = 2) -> list[str]:
    words = re.findall(r"[a-z0-9+/.-]+", normalize_text(text))
    filtered = [w for w in words if len(w) >= min_length]
    return filtered


def score_keyword_overlap(job_description: str, resume_text: str) -> dict:
    jd_words = Counter(extract_keywords(job_description))
    resume_words = Counter(extract_keywords(resume_text))

    common_words = set(jd_words.keys()) & set(resume_words.keys())
    overlap_count = sum(min(jd_words[word], resume_words[word]) for word in common_words)
    total_possible = sum(jd_words.values())

    score = 0.0
    if total_possible:
        score = (overlap_count / total_possible) * 100.0

    matched_keywords = sorted(word for word in common_words if word in jd_words)
    missing_keywords = sorted(word for word in jd_words if word not in resume_words)

    return {
        "score": round(score, 2),
        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords,
        "overlap_count": overlap_count,
        "total_possible": total_possible,
    }
