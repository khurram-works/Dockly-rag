from collections import defaultdict

from domain.models.parsed_document import ParsedDocument

from processing.filtering.filters.base_filter import BaseFilter


class RepeatedElementFilter(BaseFilter):

    def __init__(
        self,
        minimum_occurrences: int = 2,
        maximum_text_length: int = 200,
    ) -> None:

        self._minimum_occurrences = minimum_occurrences
        self._maximum_text_length = maximum_text_length

    def apply(
        self,
        document: ParsedDocument,
    ) -> ParsedDocument:

        occurrences = defaultdict(list)

        for element in document.elements:

            normalized_text = self._normalize(
                element.text
            )

            if not normalized_text:
                continue

            if len(normalized_text) > self._maximum_text_length:
                continue

            page_number = (
                element.metadata.page_number
            )

            occurrences[
                normalized_text
            ].append(
                page_number
            )

        repeated_texts = {
            text
            for text, page_numbers
            in occurrences.items()
            if (
                len(page_numbers)
                >= self._minimum_occurrences
                and len(set(page_numbers))
                >= 2
            )
        }

        filtered_elements = [
            element
            for element in document.elements
            if self._normalize(
                element.text
            ) not in repeated_texts
        ]

        return ParsedDocument(
            document_id=document.document_id,
            filename=document.filename,
            company_id=document.company_id,
            page_count=document.page_count,
            elements=filtered_elements,
        )

    def _normalize(
        self,
        text: str,
    ) -> str:

        return " ".join(
            text.split()
        ).casefold()