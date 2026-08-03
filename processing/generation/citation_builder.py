# processing/generation/citation_builder.py
from typing import List, Optional

class CitationBuilder:
    """Build citation information from retrieved chunks."""
    
    def build_citations(
        self,
        retrieved_results: List[dict],
    ) -> List[dict]:
        """Build citation information from results."""
        
        citations = []
        for result in retrieved_results:
            payload = result.get("payload", {})
            citations.append({
                "documentId": payload.get("document_id"),
                "filename": payload.get("filename"),
                "pageNumbers": payload.get("page_numbers", []),
                "chunkIndex": payload.get("chunk_index"),
            })
        
        return citations