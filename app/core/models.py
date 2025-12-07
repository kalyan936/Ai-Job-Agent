from typing import Optional
from pydantic import BaseModel


class CandidateProfile(BaseModel):
    raw_text: str


class JobPosting(BaseModel):
    id: str
    title: str
    company: str
    location: str
    description: str
    url: Optional[str] = None
