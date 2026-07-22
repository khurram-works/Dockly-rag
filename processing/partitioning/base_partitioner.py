from abc import ABC, abstractmethod
from pathlib import Path

from domain.models.document_profile import DocumentProfile
from domain.models.document_strategy import DocumentStrategy
from domain.models.parsed_document import ParsedDocument


class BasePartitioner(ABC):

    @abstractmethod
    def partition(
        self,
        file_path: Path,
        profile: DocumentProfile,
        strategy: DocumentStrategy,
    ) -> ParsedDocument:
        pass