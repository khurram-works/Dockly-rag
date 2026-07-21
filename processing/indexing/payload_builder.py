from domain.models.document_chunk import DocumentChunk


class PayloadBuilder:

    def build(
        self,
        chunk: DocumentChunk,
    ) -> dict:

        metadata = chunk.metadata

        return {
            "document_id": chunk.document_id,
            "company_id": chunk.company_id,
            "filename": chunk.filename,
            "chunk_index": chunk.chunk_index,
            "text": chunk.text,
            "page_numbers": metadata.page_numbers,
            "languages": metadata.languages,
            "section_title": metadata.section_title,
            "parent_section": metadata.parent_section,
        }