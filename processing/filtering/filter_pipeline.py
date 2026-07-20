from collections.abc import Sequence

from domain.models.parsed_document import ParsedDocument

from processing.filtering.filters.base_filter import BaseFilter


class FilterPipeline:

    def __init__(
        self,
        filters: Sequence[BaseFilter],
    ) -> None:
        self._filters = filters

    def apply(
        self,
        document: ParsedDocument,
    ) -> ParsedDocument:

        current_document = document

        for document_filter in self._filters:
            current_document = document_filter.apply(current_document)

        return current_document