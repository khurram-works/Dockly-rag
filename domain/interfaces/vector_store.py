from abc import ABC, abstractmethod

from domain.models.indexable_point import IndexablePoint


class VectorStore(ABC):

    @abstractmethod
    def upsert(
        self,
        points: list[IndexablePoint],
    ) -> None:
        pass