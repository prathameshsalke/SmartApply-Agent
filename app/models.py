from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class CandidateProfile:
    full_name: str
    email: str
    phone: str
    location: str
    gender: str
    education: List[str] = field(default_factory=list)
    experience_years: int = 0
    skills: List[str] = field(default_factory=list)
    preferred_roles: List[str] = field(default_factory=list)
    linkedin: Optional[str] = None
    portfolio: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "location": self.location,
            "gender": self.gender,
            "education": self.education,
            "experience_years": self.experience_years,
            "skills": self.skills,
            "preferred_roles": self.preferred_roles,
            "linkedin": self.linkedin,
            "portfolio": self.portfolio,
        }
