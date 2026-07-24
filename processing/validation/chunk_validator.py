from domain.models.document_chunk import DocumentChunk

from core.exceptions import ChunkValidationError


class ChunkValidator:

    def validate(
        self,
        chunk: DocumentChunk,
    ) -> None:

        if not chunk.document_id.strip():

            raise ChunkValidationError(
                "Chunk document_id cannot be empty."
            )

        if not chunk.company_id.strip():

            raise ChunkValidationError(
                "Chunk company_id cannot be empty."
            )

        if not chunk.filename.strip():

            raise ChunkValidationError(
                "Chunk filename cannot be empty."
            )

        if not chunk.text.strip():

            raise ChunkValidationError(
                "Chunk text cannot be empty."
            )

        if chunk.chunk_index < 0:

            raise ChunkValidationError(
                "Chunk chunk_index cannot be negative."
            )