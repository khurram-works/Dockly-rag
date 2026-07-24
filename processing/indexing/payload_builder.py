from typing import Any
from domain.models.document_chunk import DocumentChunk

class PayloadBuilder:

    def build(
        self,
        chunk: DocumentChunk,
    ) -> dict[str, Any]:

        metadata = chunk.metadata

        return {
            "document_id": chunk.document_id,
            "company_id": chunk.company_id,
            "filename": chunk.filename,
            "chunk_index": chunk.chunk_index,
            "text": chunk.text,

            "page_numbers": metadata.page_numbers,
            "languages": metadata.languages,
            # "coordinates": metadata.coordinates,
            "source_element_ids": metadata.source_element_ids,
            "text_as_html": metadata.text_as_html,

            # "section_title": metadata.section_title,
            # "parent_section": metadata.parent_section,
        }