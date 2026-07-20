from dataclasses import dataclass

from domain.models.chunk_metadata import ChunkMetadata


@dataclass(slots=True)
class DocumentChunk:
    document_id: str

    filename: str

    company_id: str

    chunk_index: int

    text: str

    metadata: ChunkMetadata