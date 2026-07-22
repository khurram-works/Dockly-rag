from qdrant_client import QdrantClient, models

from domain.models.indexable_point import IndexablePoint
from domain.interfaces.vector_store import VectorStore


class QdrantVectorStore(VectorStore):

    def __init__(
        self,
        client: QdrantClient,
        collection_name: str,
    ) -> None:

        self._client = client
        self._collection_name = collection_name

    def upsert(
        self,
        points: list[IndexablePoint],
    ) -> None:

        if not points:
            return

        qdrant_points = [
            models.PointStruct(
                id=point.point_id,
                vector=list(point.vector),
                payload=point.payload,
            )
            for point in points
        ]

        self._client.upsert(
            collection_name=self._collection_name,
            points=qdrant_points,
        )