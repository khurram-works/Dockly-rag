from dataclasses import dataclass

from qdrant_client.models import Distance


@dataclass(slots=True, frozen=True)
class VectorCollectionConfig:

    collection_name: str

    vector_size: int

    distance: Distance