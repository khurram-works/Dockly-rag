from abc import ABC, abstractmethod

from domain.models.document_chunk import DocumentChunk
from domain.models.parsed_document import ParsedDocument


class BaseChunker(ABC):

    @abstractmethod
    def chunk(
        self,
        document: ParsedDocument,
    ) -> list[DocumentChunk]:
        pass