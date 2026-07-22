from pathlib import Path

from domain.models.document_profile import DocumentProfile
from domain.models.document_strategy import DocumentStrategy
from domain.models.parsed_document import ParsedDocument

from providers.unstructured.provider import (
    UnstructuredProvider,
)

from processing.partitioning.base_partitioner import BasePartitioner


class DocumentPartitioner(BasePartitioner):

    def __init__(
        self,
        provider: UnstructuredProvider,
    ) -> None:

        self._provider = provider

    def partition(
        self,
        file_path: Path,
        profile: DocumentProfile,
        strategy: DocumentStrategy,
    ) -> ParsedDocument:

        return self._provider.partition(
            file_path=file_path,
            profile=profile,
            strategy=strategy,
        )