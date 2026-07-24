from unittest.mock import Mock

from domain.models.embedded_chunk import EmbeddedChunk
from domain.models.embeddings import Embedding
from domain.models.indexable_point import IndexablePoint

from processing.indexing.indexing_service import IndexingService


def create_embedded_chunk() -> EmbeddedChunk:
    """
    Minimal test object.

    Replace the construction here with your actual EmbeddedChunk
    structure if its fields differ.
    """

    return Mock(spec=EmbeddedChunk)


def test_indexing_service_does_nothing_for_empty_chunks():

    indexer = Mock()
    vector_store = Mock()

    service = IndexingService(
        indexer=indexer,
        vector_store=vector_store,
    )

    service.index([])

    indexer.index.assert_not_called()
    vector_store.upsert.assert_not_called()


def test_indexing_service_indexes_embedded_chunks():

    indexer = Mock()
    vector_store = Mock()

    embedded_chunks = [
        create_embedded_chunk(),
        create_embedded_chunk(),
    ]

    indexable_points = [
        IndexablePoint(
            point_id="point-1",
            vector=(0.1, 0.2, 0.3),
            payload={
                "document_id": "doc-123",
            },
        ),
        IndexablePoint(
            point_id="point-2",
            vector=(0.4, 0.5, 0.6),
            payload={
                "document_id": "doc-123",
            },
        ),
    ]

    indexer.index.return_value = indexable_points

    service = IndexingService(
        indexer=indexer,
        vector_store=vector_store,
    )

    service.index(embedded_chunks)

    indexer.index.assert_called_once_with(
        embedded_chunks
    )

    vector_store.upsert.assert_called_once_with(
        indexable_points
    )


def test_indexing_service_passes_indexer_output_to_vector_store():

    indexer = Mock()
    vector_store = Mock()

    embedded_chunks = [
        create_embedded_chunk(),
    ]

    expected_points = [
        IndexablePoint(
            point_id="point-123",
            vector=(0.1, 0.2, 0.3),
            payload={
                "document_id": "doc-123",
            },
        ),
    ]

    indexer.index.return_value = expected_points

    service = IndexingService(
        indexer=indexer,
        vector_store=vector_store,
    )

    service.index(embedded_chunks)

    actual_points = (
        vector_store.upsert.call_args.args[0]
    )

    assert actual_points is expected_points