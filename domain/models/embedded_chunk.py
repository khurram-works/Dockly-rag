from dataclasses import dataclass

from domain.models.document_chunk import DocumentChunk
from domain.models.embeddings import Embedding


@dataclass(slots=True, frozen=True)
class EmbeddedChunk:
    chunk: DocumentChunk
    embedding: Embedding