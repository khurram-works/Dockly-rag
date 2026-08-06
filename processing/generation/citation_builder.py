from typing import List

class CitationBuilder:
    def build_citations(self, retrieved_results: List[dict]) -> List[dict]:
        citations_by_key: dict[tuple[str, str], dict] = {}

        for result in retrieved_results:
            payload = result.get("payload", {})
            document_id = payload.get("document_id")
            filename = payload.get("filename")
            page_numbers = payload.get("page_numbers", []) or []

            if not isinstance(page_numbers, list):
                page_numbers = [page_numbers]

            key = (document_id or "", filename or "")

            if key not in citations_by_key:
                citations_by_key[key] = {
                    "documentId": document_id,
                    "filename": filename,
                    "pageNumbers": [],
                }

            existing_pages = citations_by_key[key]["pageNumbers"]
            for page in page_numbers:
                if page not in existing_pages:
                    existing_pages.append(page)

        for citation in citations_by_key.values():
            citation["pageNumbers"].sort()

        return list(citations_by_key.values())