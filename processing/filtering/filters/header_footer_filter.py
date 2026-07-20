from domain.enums.element_type import ElementType
from domain.models.parsed_document import ParsedDocument

from processing.filtering.filters.base_filter import BaseFilter


class HeaderFooterFilter(BaseFilter):

    def apply(
        self,
        document: ParsedDocument,
    ) -> ParsedDocument:

        filtered_elements = [
            element
            for element in document.elements
            if element.element_type not in {
                ElementType.HEADER,
                ElementType.FOOTER,
            }
        ]

        return ParsedDocument(
            document_id=document.document_id,
            filename=document.filename,
            company_id=document.company_id,
            page_count=document.page_count,
            elements=filtered_elements,
        )