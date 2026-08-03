from typing import Any
from domain.models.document_chunk import DocumentChunk

# processing/indexing/payload_builder.py
from typing import Any
from domain.models.document_chunk import DocumentChunk

class PayloadBuilder:
    def build(
        self,
        chunk: DocumentChunk,
    ) -> dict[str, Any]:
        metadata = chunk.metadata

        payload = {
            "document_id": chunk.document_id,
            "company_id": chunk.company_id,
            "filename": chunk.filename,
            "chunk_index": chunk.chunk_index,
            "text": chunk.text,
            "page_numbers": metadata.page_numbers,
            "languages": metadata.languages,
            "source_element_ids": metadata.source_element_ids,
            "text_as_html": metadata.text_as_html,
        }

        # Add coordinates if available
        if metadata.coordinates:
            payload["coordinates"] = [
                {"points": coord.points} for coord in metadata.coordinates
            ]

        # Add section information if available
        if hasattr(metadata, 'section_title') and metadata.section_title:
            payload["section_title"] = metadata.section_title
        
        if hasattr(metadata, 'parent_section') and metadata.parent_section:
            payload["parent_section"] = metadata.parent_section

        return payload