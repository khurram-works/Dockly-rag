# processing/generation/citation_builder.py
from typing import List

class CitationBuilder:
    def build_citations(self, retrieved_results: List[dict]) -> List[dict]:
        citations = []

        for result in retrieved_results:
            payload = result.get("payload", {})

            page_numbers = payload.get("page_numbers", []) or []
            if not isinstance(page_numbers, list):
                page_numbers = [page_numbers]

            citations.append({
                "documentId": payload.get("document_id"),
                "filename": payload.get("filename"),
                "pageNumbers": page_numbers,
                "chunkIndex": payload.get("chunk_index"),
            })

        return citations