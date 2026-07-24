from unittest.mock import Mock

from domain.models.chunk_metadata import ChunkMetadata
from domain.models.document_chunk import DocumentChunk
from domain.models.embeddings import Embedding
from domain.models.embedded_chunk import EmbeddedChunk
from domain.models.indexable_point import IndexablePoint

from processing.indexing.vector_indexer import VectorIndexer


def create_chunk(
    chunk_index: int = 0,
    text: str = "Revenue increased by 20%.",
) -> DocumentChunk:

    return DocumentChunk(
        document_id="doc-123",
        filename="annual-report.pdf",
        company_id="company-456",
        chunk_index=chunk_index,
        text=text,
        metadata=ChunkMetadata(
            page_numbers=[1],
            languages=["eng"],
            coordinates=None,
            source_element_ids=["element-123"],
            text_as_html=None,
        ),
    )


def test_vector_indexer_returns_empty_list_for_empty_input():

    payload_builder = Mock()

    indexer = VectorIndexer(
        payload_builder=payload_builder,
    )

    result = indexer.index([])

    assert result == []

    payload_builder.build.assert_not_called()


def test_vector_indexer_creates_indexable_point():

    chunk = create_chunk()

    embedding = Embedding(
        values=(0.1, 0.2, 0.3),
    )

    embedded_chunk = EmbeddedChunk(
        chunk=chunk,
        embedding=embedding,
    )

    payload = {
        "document_id": "doc-123",
        "company_id": "company-456",
        "filename": "annual-report.pdf",
        "chunk_index": 0,
        "text": "Revenue increased by 20%.",
    }

    payload_builder = Mock()

    payload_builder.build.return_value = payload

    indexer = VectorIndexer(
        payload_builder=payload_builder,
    )

    result = indexer.index(
        [embedded_chunk]
    )

    assert len(result) == 1

    assert isinstance(
        result[0],
        IndexablePoint,
    )

def test_vector_indexer_preserves_embedding_vector():

    chunk = create_chunk()

    embedding = Embedding(
        values=(0.1, 0.2, 0.3),
    )

    embedded_chunk = EmbeddedChunk(
        chunk=chunk,
        embedding=embedding,
    )

    payload_builder = Mock()

    payload_builder.build.return_value = {}

    indexer = VectorIndexer(
        payload_builder=payload_builder,
    )

    result = indexer.index(
        [embedded_chunk]
    )

    assert result[0].vector == (
        0.1,
        0.2,
        0.3,
    )


def test_vector_indexer_generates_deterministic_point_id():

    chunk = create_chunk(
        chunk_index=7,
    )

    embedding = Embedding(
        values=(0.1, 0.2, 0.3),
    )

    embedded_chunk = EmbeddedChunk(
        chunk=chunk,
        embedding=embedding,
    )

    payload_builder = Mock()

    payload_builder.build.return_value = {}

    indexer = VectorIndexer(
        payload_builder=payload_builder,
    )

    first_result = indexer.index(
        [embedded_chunk]
    )

    second_result = indexer.index(
        [embedded_chunk]
    )

    assert (
        first_result[0].point_id
        == second_result[0].point_id
    )



def test_vector_indexer_delegates_payload_creation():

    chunk = create_chunk()

    embedding = Embedding(
        values=(0.1, 0.2, 0.3),
    )

    embedded_chunk = EmbeddedChunk(
        chunk=chunk,
        embedding=embedding,
    )

    payload = {
        "document_id": "doc-123",
        "text": "Revenue increased by 20%.",
    }

    payload_builder = Mock()

    payload_builder.build.return_value = payload

    indexer = VectorIndexer(
        payload_builder=payload_builder,
    )

    result = indexer.index(
        [embedded_chunk]
    )

    payload_builder.build.assert_called_once_with(
        chunk
    )

    assert result[0].payload == payload

def test_vector_indexer_preserves_chunk_order():

    first_chunk = create_chunk(
        chunk_index=0,
        text="First chunk",
    )

    second_chunk = create_chunk(
        chunk_index=1,
        text="Second chunk",
    )

    first_embedded_chunk = EmbeddedChunk(
        chunk=first_chunk,
        embedding=Embedding(
            values=(0.1, 0.2, 0.3),
        ),
    )

    second_embedded_chunk = EmbeddedChunk(
        chunk=second_chunk,
        embedding=Embedding(
            values=(0.4, 0.5, 0.6),
        ),
    )

    payload_builder = Mock()

    payload_builder.build.return_value = {}

    indexer = VectorIndexer(
        payload_builder=payload_builder,
    )

    result = indexer.index(
        [
            first_embedded_chunk,
            second_embedded_chunk,
        ]
    )

    assert result[0].vector == (
        0.1,
        0.2,
        0.3,
    )

    assert result[1].vector == (
        0.4,
        0.5,
        0.6,
    )



