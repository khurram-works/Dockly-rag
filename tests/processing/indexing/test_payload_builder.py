from domain.models.chunk_metadata import ChunkMetadata
from domain.models.document_chunk import DocumentChunk
from processing.indexing.payload_builder import PayloadBuilder


def test_payload_builder_preserves_chunk_identity_and_content():

    chunk = DocumentChunk(
        document_id="doc-123",
        company_id="company-456",
        filename="company.pdf",
        chunk_index=3,
        text="The company builds software.",
        metadata=ChunkMetadata(
            page_numbers=[1, 2],
            languages=["eng"],
            section_title="Company Overview",
            parent_section="About the Company",
        ),
    )

    builder = PayloadBuilder()

    payload = builder.build(chunk)

    assert payload == {
        "document_id": "doc-123",
        "company_id": "company-456",
        "filename": "company.pdf",
        "chunk_index": 3,
        "text": "The company builds software.",
        "page_numbers": [1, 2],
        "languages": ["eng"],
        "section_title": "Company Overview",
        "parent_section": "About the Company",
    }