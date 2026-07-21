from domain.models.embedded_chunk import EmbeddedChunk
from domain.models.indexable_point import IndexablePoint

from processing.indexing.point_id import build_point_id


class VectorIndexer:

    def index(
        self,
        embedded_chunks: list[EmbeddedChunk],
    ) -> list[IndexablePoint]:

        return [
            self._to_indexable_point(
                embedded_chunk=embedded_chunk,
            )
            for embedded_chunk in embedded_chunks
        ]

    def _to_indexable_point(
        self,
        embedded_chunk: EmbeddedChunk,
    ) -> IndexablePoint:

        chunk = embedded_chunk.chunk

        point_id = build_point_id(
            document_id=chunk.document_id,
            chunk_index=chunk.chunk_index,
        )

        payload = {
            "document_id": chunk.document_id,
            "filename": chunk.filename,
            "company_id": chunk.company_id,
            "chunk_index": chunk.chunk_index,
            "text": chunk.text,
        }

        return IndexablePoint(
            point_id=point_id,
            vector=embedded_chunk.embedding.values,
            payload=payload,
        )