from unittest.mock import Mock

from domain.models.chunk_metadata import ChunkMetadata
from domain.models.document_chunk import DocumentChunk
from domain.models.embeddings import Embedding
from domain.models.embedded_chunk import EmbeddedChunk
from processing.indexing.indexing_service import IndexingService


def create_embedded_chunk(
    index: int,
    text: str,
) -> EmbeddedChunk:

    chunk = DocumentChunk(
        document_id="doc-123",
        filename="company.pdf",
        company_id="company-456",
        chunk_index=index,
        text=text,
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

    return EmbeddedChunk(
        chunk=chunk,
        embedding=embedding,
    )


def test_indexing_service_does_nothing_for_empty_input():

    vector_store = Mock()

    service = IndexingService(
        vector_store=vector_store,
    )

    service.index([])

    vector_store.upsert.assert_not_called()


def test_indexing_service_passes_embedded_chunks_to_vector_store():

    vector_store = Mock()

    embedded_chunks = [
        create_embedded_chunk(
            index=0,
            text="First chunk",
        ),
        create_embedded_chunk(
            index=1,
            text="Second chunk",
        ),
    ]

    service = IndexingService(
        vector_store=vector_store,
    )

    service.index(embedded_chunks)

    vector_store.upsert.assert_called_once_with(
        embedded_chunks
    )