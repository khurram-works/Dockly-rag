from domain.models.document_chunk import DocumentChunk
from domain.models.chunk_metadata import ChunkMetadata
from domain.models.embeddings import Embedding
from domain.models.embedded_chunk import EmbeddedChunk

from processing.indexing.vector_indexer import VectorIndexer
from processing.indexing.point_id import build_point_id


def test_vector_indexer_creates_indexable_point():

    chunk = DocumentChunk(
        document_id="doc-123",
        filename="company.pdf",
        company_id="company-456",
        chunk_index=0,
        text="The company builds software.",
        metadata=ChunkMetadata(
            page_numbers=[1],
            languages=["eng"],
        ),
    )

    embedded_chunk = EmbeddedChunk(
        chunk=chunk,
        embedding=Embedding(
            values=(
                0.1,
                0.2,
                0.3,
            ),
        ),
    )

    indexer = VectorIndexer()

    points = indexer.index(
        embedded_chunks=[embedded_chunk],
    )

    assert len(points) == 1

    point = points[0]

    assert point.point_id == build_point_id(
        document_id="doc-123",
        chunk_index=0,
    )

    assert point.vector == (
        0.1,
        0.2,
        0.3,
    )

    assert point.payload["document_id"] == "doc-123"
    assert point.payload["filename"] == "company.pdf"
    assert point.payload["company_id"] == "company-456"
    assert point.payload["chunk_index"] == 0
    assert point.payload["text"] == (
        "The company builds software."
    )