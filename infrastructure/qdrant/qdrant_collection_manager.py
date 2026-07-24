from qdrant_client import QdrantClient, models

from domain.interfaces.collection_manager import (
    CollectionManager,
)
from domain.models.vector_collection_config import (
    VectorCollectionConfig,
)


class QdrantCollectionManager(CollectionManager):

    def __init__(
        self,
        client: QdrantClient,
    ) -> None:

        self._client = client

    def ensure_collection(
        self,
        config: VectorCollectionConfig,
    ) -> None:

        exists = self._client.collection_exists(
            collection_name=config.collection_name,
        )

        if exists:
            return

        self._client.create_collection(
            collection_name=config.collection_name,
            vectors_config=models.VectorParams(
                size=config.vector_size,
                distance=config.distance,
            ),
        )