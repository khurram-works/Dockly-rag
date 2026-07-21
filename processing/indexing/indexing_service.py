from domain.interfaces.vector_store import VectorStore
from domain.models.embedded_chunk import EmbeddedChunk


class IndexingService:

    def __init__(
        self,
        vector_store: VectorStore,
    ) -> None:
        self._vector_store = vector_store

    def index(
        self,
        chunks: list[EmbeddedChunk],
    ) -> None:

        if not chunks:
            return

        self._vector_store.upsert(chunks)