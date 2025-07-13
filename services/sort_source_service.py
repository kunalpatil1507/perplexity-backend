from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List

class SortSourceService:
    def __init__(self):
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    def sort_sources(self, query: str, search_results: List[dict]):
        relevant_docs = []
        query_embedding = self.embedding_model.encode(query, normalize_embeddings=True)

        for res in search_results:
            if not res["content"]:
                continue
            res_embedding = self.embedding_model.encode(res["content"], normalize_embeddings=True)
            similarity = np.dot(query_embedding, res_embedding)
            res["relevance_score"] = similarity
            if similarity > 0.3:
                relevant_docs.append(res)

        return sorted(relevant_docs, key=lambda x: x["relevance_score"], reverse=True)
