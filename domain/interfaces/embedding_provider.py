from abc import ABC, abstractmethod

from domain.models.embeddings import Embedding


class EmbeddingProvider(ABC):

    @abstractmethod
    def embed_documents(
        self,
        texts: list[str],
    ) -> list[Embedding]:
      ...

    @abstractmethod
    def embed_query(
      self,
      text: str,
    ) -> Embedding:
      ...

