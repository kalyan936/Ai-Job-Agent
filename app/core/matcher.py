from sentence_transformers import SentenceTransformer, util

class JobMatcher:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def _encode(self, texts):
        return self.model.encode(texts, convert_to_tensor=True)

    def rank_jobs(self, profile: str, jobs: list):
        # Encode profile text
        profile_emb = self._encode([profile])

        # Encode each job description
        job_texts = [job["description"] for job in jobs]
        job_embs = self._encode(job_texts)

        # Compute similarity
        scores = util.cos_sim(profile_emb, job_embs)[0].cpu().tolist()

        # Attach scores
        ranked = []
        for job, score in zip(jobs, scores):
            ranked.append({
                "job_id": job["id"],
                "title": job["title"],
                "company": job["company"],
                "score": score
            })

        # Sort descending
        ranked = sorted(ranked, key=lambda x: x["score"], reverse=True)
        return ranked
