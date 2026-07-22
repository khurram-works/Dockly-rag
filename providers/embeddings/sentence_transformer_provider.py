from sentence_transformers import SentenceTransformer

from domain.interfaces.embedding_provider import (
    EmbeddingProvider,
)
from domain.models.embeddings import Embedding
from domain.models.embedding_config import EmbeddingConfig


class SentenceTransformerEmbeddingProvider(
    EmbeddingProvider
):

    def __init__(
        self,
        config: EmbeddingConfig,
    ) -> None:

        self._config = config

        self._model = SentenceTransformer(
            config.model_name
        )

    def embed_documents(
        self,
        texts: list[str],
    ) -> list[Embedding]:

        if not texts:
            return []

        vectors = self._model.encode_document(
            texts,
            batch_size=self._config.batch_size,
            normalize_embeddings=(
                self._config.normalize_embeddings
            ),
            convert_to_numpy=True,
        )

        return [
            self._to_embedding(vector)
            for vector in vectors
        ]

    def embed_query(
        self,
        text: str,
    ) -> Embedding:
        
        if not text:
            raise ValueError("Query text cannot be empty.")

        vector = self._model.encode_query(
            text,
            normalize_embeddings=(
                self._config.normalize_embeddings
            ),
            convert_to_numpy=True,
        )

        return self._to_embedding(vector)

    def _to_embedding(
        self,
        vector,
    ) -> Embedding:

        return Embedding(values=tuple(vector.tolist()))


