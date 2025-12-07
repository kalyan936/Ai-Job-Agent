import os
from langchain_groq import ChatGroq
from app.core.job_search import search_jobs_function as raw_search_jobs
from app.core.ranker import rank_jobs

# Fast lightweight model for ranking
llm = ChatGroq(
    groq_api_key=os.environ["GROQ_API_KEY"],
    model="llama-3.1-8b-instant",   # fast model, NOT 70B
    temperature=0
)

def run_agent(query: str, resume_text: str, num_results: int = 10):
    """
    FAST pipeline:
    1. Fetch jobs
    2. Rank jobs using LLM
    """
    # ---- 1. Fetch jobs ----
    jobs = raw_search_jobs(
        query=query,
        location="",
        num_results=num_results
    )

    if not jobs:
        return []

    # ---- 2. Rank Jobs ----
    # rank_jobs is a StructuredTool. It expects: jobs, resume_text
    ranked_jobs = rank_jobs.invoke({
        "jobs": jobs,
        "resume_text": resume_text,
        "query": query
    })

    return ranked_jobs
