from domain.models.chunk_metadata import ChunkMetadata
from domain.models.document_chunk import DocumentChunk

from processing.indexing.payload_builder import PayloadBuilder


def create_chunk() -> DocumentChunk:

    return DocumentChunk(
        document_id="doc-123",
        filename="annual-report.pdf",
        company_id="company-456",
        chunk_index=7,
        text="Revenue increased significantly during the year.",
        metadata=ChunkMetadata(
            page_numbers=[2, 3],
            languages=["eng"],
            coordinates=None,
            source_element_ids=[
                "element-101",
                "element-102",
            ],
            text_as_html=None,
        ),
    )


def test_payload_builder_preserves_chunk_identity():

    chunk = create_chunk()

    builder = PayloadBuilder()

    payload = builder.build(chunk)

    assert payload["document_id"] == "doc-123"

    assert payload["company_id"] == "company-456"

    assert payload["filename"] == (
        "annual-report.pdf"
    )

    assert payload["chunk_index"] == 7


def test_payload_builder_preserves_chunk_text():

    chunk = create_chunk()

    builder = PayloadBuilder()

    payload = builder.build(chunk)

    assert payload["text"] == (
        "Revenue increased significantly "
        "during the year."
    )


def test_payload_builder_preserves_chunk_metadata():

    chunk = create_chunk()

    builder = PayloadBuilder()

    payload = builder.build(chunk)

    assert payload["page_numbers"] == [2, 3]

    assert payload["languages"] == ["eng"]

    assert payload["source_element_ids"] == [
        "element-101",
        "element-102",
    ]

    assert payload["text_as_html"] is None


def test_payload_builder_preserves_table_html():

    chunk = DocumentChunk(
        document_id="doc-123",
        filename="financial-report.pdf",
        company_id="company-456",
        chunk_index=0,
        text="Product Revenue",
        metadata=ChunkMetadata(
            page_numbers=[4],
            languages=["eng"],
            coordinates=None,
            source_element_ids=["table-123"],
            text_as_html=(
                "<table>"
                "<tr>"
                "<td>Product</td>"
                "<td>Revenue</td>"
                "</tr>"
                "</table>"
            ),
        ),
    )

    builder = PayloadBuilder()

    payload = builder.build(chunk)

    assert payload["text_as_html"] == (
        "<table>"
        "<tr>"
        "<td>Product</td>"
        "<td>Revenue</td>"
        "</tr>"
        "</table>"
    )


def test_payload_builder_returns_expected_payload_keys():

    chunk = create_chunk()

    builder = PayloadBuilder()

    payload = builder.build(chunk)

    assert set(payload.keys()) == {
        "document_id",
        "company_id",
        "filename",
        "chunk_index",
        "text",
        "page_numbers",
        "languages",
        "source_element_ids",
        "text_as_html",
    }