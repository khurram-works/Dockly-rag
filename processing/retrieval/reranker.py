# processing/retrieval/reranker.py
from typing import List

class Reranker:
    """Rerank retrieved results for better relevance."""
    
    def rerank(
        self,
        query: str,
        results: List[dict],
        top_k: int = 5,
    ) -> List[dict]:
        """Rerank results based on query relevance."""
        
        # Simple implementation: return as-is
        # Advanced: Use cross-encoder for reranking
        return results[:top_k]