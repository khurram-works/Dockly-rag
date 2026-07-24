from qdrant_client import QdrantClient, models
from unittest.mock import Mock

from domain.models.indexable_point import IndexablePoint
from infrastructure.qdrant.qdrant_vector_store import (
    QdrantVectorStore,
)


def test_qdrant_vector_store_does_nothing_for_empty_points():

    client = Mock()

    store = QdrantVectorStore(
        client=client,
        collection_name="dockly_documents",
    )

    store.upsert([])

    client.upsert.assert_not_called()


def test_qdrant_vector_store_upserts_into_configured_collection():

    client = Mock()

    points = [
        IndexablePoint(
            point_id="point-1",
            vector=(0.1, 0.2, 0.3),
            payload={
                "document_id": "doc-123",
                "text": "Revenue increased.",
            },
        ),
    ]

    store = QdrantVectorStore(
        client=client,
        collection_name="dockly_documents",
    )

    store.upsert(points)

    client.upsert.assert_called_once()

    call_kwargs = client.upsert.call_args.kwargs

    assert (
        call_kwargs["collection_name"]
        == "dockly_documents"
    )


def test_qdrant_vector_store_converts_indexable_point():

    client = Mock()

    point = IndexablePoint(
        point_id="point-1",
        vector=(0.1, 0.2, 0.3),
        payload={
            "document_id": "doc-123",
            "text": "Revenue increased.",
        },
    )

    store = QdrantVectorStore(
        client=client,
        collection_name="dockly_documents",
    )

    store.upsert([point])

    call_kwargs = client.upsert.call_args.kwargs

    qdrant_points = call_kwargs["points"]

    assert len(qdrant_points) == 1

    qdrant_point = qdrant_points[0]

    assert isinstance(
        qdrant_point,
        models.PointStruct,
    )

    assert qdrant_point.id == "point-1"

    assert qdrant_point.vector == [
        0.1,
        0.2,
        0.3,
    ]

    assert qdrant_point.payload == {
        "document_id": "doc-123",
        "text": "Revenue increased.",
    }


def test_qdrant_vector_store_converts_multiple_points():

    client = Mock()

    points = [
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

    store = QdrantVectorStore(
        client=client,
        collection_name="dockly_documents",
    )

    store.upsert(points)

    call_kwargs = client.upsert.call_args.kwargs

    qdrant_points = call_kwargs["points"]

    assert len(qdrant_points) == 2

    assert qdrant_points[0].id == "point-1"

    assert qdrant_points[1].id == "point-2"

    assert qdrant_points[0].vector == [
        0.1,
        0.2,
        0.3,
    ]

    assert qdrant_points[1].vector == [
        0.4,
        0.5,
        0.6,
    ]


def test_qdrant_vector_store_preserves_point_order():

    client = Mock()

    first_point = IndexablePoint(
        point_id="first",
        vector=(0.1, 0.2),
        payload={},
    )

    second_point = IndexablePoint(
        point_id="second",
        vector=(0.3, 0.4),
        payload={},
    )

    store = QdrantVectorStore(
        client=client,
        collection_name="dockly_documents",
    )

    store.upsert(
        [
            first_point,
            second_point,
        ]
    )

    qdrant_points = (
        client.upsert.call_args.kwargs["points"]
    )

    assert qdrant_points[0].id == "first"

    assert qdrant_points[1].id == "second"

