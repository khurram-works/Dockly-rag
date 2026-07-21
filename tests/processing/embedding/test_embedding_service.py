from unittest.mock import Mock

import pytest

from domain.models.chunk_metadata import ChunkMetadata
from domain.models.document_chunk import DocumentChunk
from domain.models.embeddings import Embedding
from domain.models.embedded_chunk import EmbeddedChunk
from processing.embedding.embedding_service import EmbeddingService


def create_chunk(
    index: int,
    text: str,
) -> DocumentChunk:

    return DocumentChunk(
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


def test_embedding_service_returns_empty_list_for_empty_chunks():

    provider = Mock()

    service = EmbeddingService(
        provider=provider,
    )

    result = service.embed_chunks([])

    assert result == []

    provider.embed_documents.assert_not_called()


def test_embedding_service_embeds_all_chunks():

    provider = Mock()

    provider.embed_documents.return_value = [
        Embedding(
            values=(0.1, 0.2, 0.3),
        ),
        Embedding(
            values=(0.4, 0.5, 0.6),
        ),
    ]

    chunks = [
        create_chunk(
            index=0,
            text="First chunk",
        ),
        create_chunk(
            index=1,
            text="Second chunk",
        ),
    ]

    service = EmbeddingService(
        provider=provider,
    )

    result = service.embed_chunks(chunks)

    assert len(result) == 2

    provider.embed_documents.assert_called_once_with(
        [
            "First chunk",
            "Second chunk",
        ]
    )


def test_embedding_service_preserves_chunk_embedding_alignment():

    provider = Mock()

    first_embedding = Embedding(
        values=(0.1, 0.2, 0.3),
    )

    second_embedding = Embedding(
        values=(0.4, 0.5, 0.6),
    )

    provider.embed_documents.return_value = [
        first_embedding,
        second_embedding,
    ]

    first_chunk = create_chunk(
        index=0,
        text="First chunk",
    )

    second_chunk = create_chunk(
        index=1,
        text="Second chunk",
    )

    service = EmbeddingService(
        provider=provider,
    )

    result = service.embed_chunks(
        [
            first_chunk,
            second_chunk,
        ]
    )

    assert result[0].chunk is first_chunk
    assert result[0].embedding is first_embedding

    assert result[1].chunk is second_chunk
    assert result[1].embedding is second_embedding


def test_embedding_service_rejects_mismatched_embedding_count():

    provider = Mock()

    provider.embed_documents.return_value = [
        Embedding(
            values=(0.1, 0.2, 0.3),
        ),
    ]

    chunks = [
        create_chunk(
            index=0,
            text="First chunk",
        ),
        create_chunk(
            index=1,
            text="Second chunk",
        ),
    ]

    service = EmbeddingService(
        provider=provider,
    )

    with pytest.raises(
        ValueError,
        match="different number of embeddings",
    ):

        service.embed_chunks(chunks)