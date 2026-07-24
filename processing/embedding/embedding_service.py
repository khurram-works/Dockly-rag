from domain.models.embedded_chunk import EmbeddedChunk
from domain.models.document_chunk import DocumentChunk
from domain.interfaces.embedding_provider import EmbeddingProvider


class EmbeddingService:

    def __init__(
        self,
        provider: EmbeddingProvider,
    ) -> None:
        self._provider = provider

    def embed_chunks(
        self,
        chunks: list[DocumentChunk],
    ) -> list[EmbeddedChunk]:

        if not chunks:
            return []

        texts = [
            chunk.text
            for chunk in chunks
        ]

        embeddings = self._provider.embed_documents(
            texts
        )

        if len(embeddings) != len(chunks):
            raise ValueError(
                "Embedding provider returned a different "
                "number of embeddings than input chunks."
            )

        return [
            EmbeddedChunk(
                chunk=chunk,
                embedding=embedding,
            )
            for chunk, embedding in zip(
                chunks,
                embeddings,
            )
        ]