import os
import requests
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from typing import List


class JobSearchInput(BaseModel):
    query: str = Field(..., description="Job title or keywords")
    location: str = Field(..., description="Location")
    num_results: int = Field(10, description="Number of results to return")


def search_jobs_function(query: str, location: str, num_results: int = 10):
    url = "https://jsearch.p.rapidapi.com/search"

    headers = {
        "X-RapidAPI-Key": os.environ.get("JSEARCH_API_KEY", ""),
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    if not headers["X-RapidAPI-Key"]:
        return []

    params = {
        "query": f"{query} in {location}",
        "page": "1",
        "num_pages": "1",
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception:
        return []

    jobs = []
    for item in data.get("data", [])[:num_results]:
        jobs.append({
            "id": item.get("job_id", ""),
            "title": item.get("job_title", ""),
            "company": item.get("employer_name", ""),
            "location": item.get("job_city") or item.get("job_country", ""),
            "description": item.get("job_description", ""),
            "link": item.get("job_apply_link") or item.get("job_apply_link_original") or "#"
        })

    return jobs
