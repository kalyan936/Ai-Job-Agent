from langchain_core.tools import tool
from sentence_transformers import SentenceTransformer, util
import numpy as np

# Load small, fast embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

def cosine(a, b):
    return float(util.cos_sim(a, b)[0][0])

@tool
def rank_jobs(jobs: list, resume_text: str, query: str = ""):
    """
    Ultra-fast ranking engine using embeddings + keyword scoring.
    Returns jobs sorted by total_score.
    """
    if not jobs:
        return []

    resume_emb = model.encode(resume_text, convert_to_tensor=True)
    query_emb = model.encode(query, convert_to_tensor=True)

    ranked = []
    for job in jobs:
        title = job.get("title", "")
        summary = job.get("summary", "")
        combined = f"{title}. {summary}"

        job_emb = model.encode(combined, convert_to_tensor=True)

        # ---- semantic similarity ----
        resume_score = cosine(resume_emb, job_emb)
        query_score = cosine(query_emb, job_emb)

        # ---- keyword score ----
        resume_text_lower = resume_text.lower()
        combined_lower = combined.lower()

        keyword_hits = sum(word in combined_lower for word in query.lower().split())
        keyword_score = min(keyword_hits / 5, 1.0)  # cap at 1

        # ---- weighted score ----
        total_score = (
            resume_score * 0.5 +
            query_score * 0.3 +
            keyword_score * 0.2
        )

        job["score"] = round(total_score, 4)
        ranked.append(job)

    # Sort by score descending
    ranked.sort(key=lambda x: x["score"], reverse=True)
    return ranked
