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

        if not exists:

            self._client.create_collection(
                collection_name=config.collection_name,
                vectors_config=models.VectorParams(
                    size=config.vector_size,
                    distance=config.distance,
                ),
            )

        self._ensure_payload_indexes(
            collection_name=config.collection_name,
        )

    def _ensure_payload_indexes(
        self,
        collection_name: str,
    ) -> None:

        self._client.create_payload_index(
            collection_name=collection_name,
            field_name="company_id",
            field_schema=models.PayloadSchemaType.KEYWORD,
        )

        self._client.create_payload_index(
            collection_name=collection_name,
            field_name="document_id",
            field_schema=models.PayloadSchemaType.KEYWORD,
        )