from qdrant_client import QdrantClient, models

from domain.models.indexable_point import IndexablePoint
from domain.interfaces.vector_store import VectorStore

from tenacity import retry, stop_after_attempt, wait_exponential
from qdrant_client import QdrantClient, models
from qdrant_client.http.exceptions import UnexpectedResponse
from tenacity import retry_if_exception_type


class QdrantVectorStore(VectorStore):
    def __init__(
        self,
        client: QdrantClient,
        collection_name: str,
    ) -> None:
        self._client = client
        self._collection_name = collection_name

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((UnexpectedResponse, ConnectionError)),
    )
    
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

    def delete_points_by_document_id(self, document_id: str) -> None:
        self._client.delete(
            collection_name=self._collection_name,
            points_selector=models.Filter(
                must=[
                    models.FieldCondition(
                        key="document_id",
                        match=models.MatchValue(value=document_id),
                    )
                ]
            ),
        )