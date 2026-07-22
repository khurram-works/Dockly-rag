from unittest.mock import Mock

from domain.models.indexable_point import IndexablePoint
from infrastructure.qdrant.qdrant_vector_store import (
    QdrantVectorStore,
)


def test_qdrant_vector_store_upserts_points():

    fake_client = Mock()

    store = QdrantVectorStore(
        client=fake_client,
        collection_name="documents",
    )

    point = IndexablePoint(
        point_id="point-123",
        vector=(
            0.1,
            0.2,
            0.3,
        ),
        payload={
            "document_id": "doc-123",
        },
    )

    store.upsert(
        points=[point],
    )

    fake_client.upsert.assert_called_once()

    call_kwargs = fake_client.upsert.call_args.kwargs

    assert call_kwargs["collection_name"] == "documents"

    qdrant_points = call_kwargs["points"]

    assert len(qdrant_points) == 1

    assert qdrant_points[0].id == "point-123"

    assert list(qdrant_points[0].vector) == [
        0.1,
        0.2,
        0.3,
    ]

    assert qdrant_points[0].payload == {
        "document_id": "doc-123",
    }


def test_qdrant_vector_store_does_not_upsert_empty_points():

    fake_client = Mock()

    store = QdrantVectorStore(
        client=fake_client,
        collection_name="documents",
    )

    store.upsert(
        points=[],
    )

    fake_client.upsert.assert_not_called()