from domain.interfaces.vector_store import VectorStore
from domain.models.embedded_chunk import EmbeddedChunk
from processing.indexing.vector_indexer import VectorIndexer


class IndexingService:

    def __init__(
        self,
        indexer: VectorIndexer,
        vector_store: VectorStore,
    ) -> None:

        self._indexer = indexer
        self._vector_store = vector_store

    def index(
        self,
        chunks: list[EmbeddedChunk],
    ) -> None:

        if not chunks:
            return
    
        points = self._indexer.index(
            chunks
        )
    
        self._vector_store.upsert(
            points
        )