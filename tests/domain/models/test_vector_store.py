from domain.models.indexable_point import IndexablePoint
from domain.interfaces.vector_store import VectorStore


class FakeVectorStore(VectorStore):

    def __init__(self):

        self.points = []

    def upsert(
        self,
        points: list[IndexablePoint],
    ) -> None:

        self.points.extend(points)


def test_vector_store_accepts_indexable_points():

    store = FakeVectorStore()

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

    assert len(store.points) == 1

    assert store.points[0] == point