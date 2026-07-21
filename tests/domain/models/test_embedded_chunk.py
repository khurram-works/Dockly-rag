from domain.models.chunk_metadata import ChunkMetadata
from domain.models.document_chunk import DocumentChunk
from domain.models.embeddings import Embedding
from domain.models.embedded_chunk import EmbeddedChunk


def test_embedded_chunk_preserves_chunk_and_embedding():

    chunk = DocumentChunk(
        document_id="doc-123",
        filename="company.pdf",
        company_id="company-456",
        chunk_index=0,
        text="Company overview",
        metadata=ChunkMetadata(
            page_numbers=[1],
            languages=["eng"],
        ),
    )

    embedding = Embedding(
        values=(
            0.1,
            0.2,
            0.3,
        )
    )

    embedded_chunk = EmbeddedChunk(
        chunk=chunk,
        embedding=embedding,
    )

    assert embedded_chunk.chunk is chunk
    assert embedded_chunk.embedding is embedding

    assert embedded_chunk.chunk.document_id == "doc-123"
    assert embedded_chunk.chunk.chunk_index == 0

    assert embedded_chunk.embedding.dimension == 3