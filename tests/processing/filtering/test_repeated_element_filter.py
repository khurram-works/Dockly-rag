from domain.enums.element_type import ElementType

from domain.models.document_element import DocumentElement
from domain.models.document_metadata import DocumentMetadata
from domain.models.parsed_document import ParsedDocument

from processing.filtering.filters.repeated_element_filter import (
    RepeatedElementFilter,
)


def test_repeated_element_filter_removes_repeated_text_across_pages():

    document = ParsedDocument(
        document_id="doc-123",
        filename="annual_report.pdf",
        company_id="company-456",
        page_count=3,
        elements=[
            DocumentElement(
                element_id="element-header",
                text="ACME Corporation — Confidential",
                element_type=ElementType.NARRATIVE,
                metadata=DocumentMetadata(
                    page_number=1,
                    languages=[],
                    coordinates=None,
                    section_title=None,
                    parent_section=None,
                ),
            ),
            DocumentElement(
                element_id="element-revenue",
                text="Revenue increased by 20%.",
                element_type=ElementType.NARRATIVE,
                metadata=DocumentMetadata(
                    page_number=1,
                    languages=[],
                    coordinates=None,
                    section_title=None,
                    parent_section=None,
                ),
            ),
            DocumentElement(
                element_id="element-header-page-2",
                text="ACME Corporation — Confidential",
                element_type=ElementType.NARRATIVE,
                metadata=DocumentMetadata(
                    page_number=2,
                    languages=[],
                    coordinates=None,
                    section_title=None,
                    parent_section=None,
                ),
            ),
            DocumentElement(
                element_id="element-profit",
                text="Profit increased by 15%.",
                element_type=ElementType.NARRATIVE,
                metadata=DocumentMetadata(
                    page_number=2,
                    languages=[],
                    coordinates=None,
                    section_title=None,
                    parent_section=None,
                ),
            ),
        ],
    )

    document_filter = RepeatedElementFilter()

    result = document_filter.apply(
        document
    )

    assert len(result.elements) == 2

    assert result.elements[0].text == (
        "Revenue increased by 20%."
    )

    assert result.elements[1].text == (
        "Profit increased by 15%."
    )

    assert result.elements[0].element_id == "element-revenue"
    assert result.elements[1].element_id == (
    "element-profit"
)

def test_repeated_text_on_same_page_is_preserved():

    document = ParsedDocument(
        document_id="doc-123",
        filename="document.pdf",
        company_id="company-456",
        page_count=1,
        elements=[
            DocumentElement(
                element_id="title-introduction",
                text="Introduction",
                element_type=ElementType.TITLE,
                metadata=DocumentMetadata(
                    page_number=1,
                    languages=[],
                    coordinates=None,
                    section_title=None,
                    parent_section=None,
                ),
            ),
            DocumentElement(
                element_id="narrative-introduction",
                text="Introduction",
                element_type=ElementType.NARRATIVE,
                metadata=DocumentMetadata(
                    page_number=1,
                    languages=[],
                    coordinates=None,
                    section_title=None,
                    parent_section=None,
                ),
            ),
        ],
    )

    document_filter = RepeatedElementFilter()

    result = document_filter.apply(document)

    assert len(result.elements) == 2

    assert result.elements[0].element_id == (
        "title-introduction"
    )

    assert result.elements[1].element_id == (
        "narrative-introduction"
    )

def test_repeated_text_across_three_pages_is_removed():

    document = ParsedDocument(
        document_id="doc-123",
        filename="annual_report.pdf",
        company_id="company-456",
        page_count=3,
        elements=[
            DocumentElement(
                element_id="header-page-1",
                text="ACME Corporation — Confidential",
                element_type=ElementType.NARRATIVE,
                metadata=DocumentMetadata(
                    page_number=1,
                    languages=[],
                    coordinates=None,
                    section_title=None,
                    parent_section=None,
                ),
            ),
            DocumentElement(
                element_id="header-page-2",
                text="ACME Corporation — Confidential",
                element_type=ElementType.NARRATIVE,
                metadata=DocumentMetadata(
                    page_number=2,
                    languages=[],
                    coordinates=None,
                    section_title=None,
                    parent_section=None,
                ),
            ),
            DocumentElement(
                element_id="header-page-3",
                text="ACME Corporation — Confidential",
                element_type=ElementType.NARRATIVE,
                metadata=DocumentMetadata(
                    page_number=3,
                    languages=[],
                    coordinates=None,
                    section_title=None,
                    parent_section=None,
                ),
            ),
            DocumentElement(
                element_id="important-information",
                text="Important business information.",
                element_type=ElementType.NARRATIVE,
                metadata=DocumentMetadata(
                    page_number=3,
                    languages=[],
                    coordinates=None,
                    section_title=None,
                    parent_section=None,
                ),
            ),
        ],
    )

    document_filter = RepeatedElementFilter()

    result = document_filter.apply(document)

    assert len(result.elements) == 1

    assert result.elements[0].text == (
        "Important business information."
    )

    assert result.elements[0].element_id == (
        "important-information"
    )