from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from typing import List


class Job(BaseModel):
    id: str
    title: str
    company: str
    location: str
    description: str


class RankJobsInput(BaseModel):
    profile: str = Field(..., description="User resume or skills")
    jobs: List[Job] = Field(..., description="List of job postings")


def rank_jobs_function(profile: str, jobs: List[Job]):
    from app.core.matcher import JobMatcher

    matcher = JobMatcher()
    job_dicts = [job.dict() for job in jobs]
    ranked = matcher.rank_jobs(profile, job_dicts)
    return ranked


rank_jobs = StructuredTool(
    name="rank_jobs",
    description="Rank job postings based on similarity to user profile.",
    func=rank_jobs_function,
    args_schema=RankJobsInput,
)
