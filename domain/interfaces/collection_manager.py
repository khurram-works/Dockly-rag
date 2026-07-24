from abc import ABC, abstractmethod

from domain.models.vector_collection_config import (
    VectorCollectionConfig,
)


class CollectionManager(ABC):

    @abstractmethod
    def ensure_collection(
        self,
        config: VectorCollectionConfig,
    ) -> None:
        ...