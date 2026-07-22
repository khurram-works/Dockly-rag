from domain.enums.element_type import ElementType

from domain.models.document_element import DocumentElement
from domain.models.document_metadata import DocumentMetadata
from domain.models.parsed_document import ParsedDocument

from processing.filtering.filter_pipeline import FilterPipeline
from processing.filtering.filters.empty_text_filter import EmptyTextFilter
from processing.filtering.filters.header_footer_filter import HeaderFooterFilter
from processing.filtering.filters.repeated_element_filter import (
    RepeatedElementFilter,
)


def test_filter_pipeline_applies_filters_in_order():

    document = ParsedDocument(
        document_id="doc-123",
        filename="annual_report.pdf",
        company_id="company-456",
        page_count=2,
        elements=[
            DocumentElement(
                element_id="title-1",
                text="Annual Report",
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
                element_id="header-1",
                text="ACME Corporation — Confidential",
                element_type=ElementType.HEADER,
                metadata=DocumentMetadata(
                    page_number=1,
                    languages=[],
                    coordinates=None,
                    section_title=None,
                    parent_section=None,
                ),
            ),

            DocumentElement(
                element_id="empty-1",
                text="   ",
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
                element_id="revenue-1",
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
                element_id="header-2",
                text="ACME Corporation — Confidential",
                element_type=ElementType.HEADER,
                metadata=DocumentMetadata(
                    page_number=2,
                    languages=[],
                    coordinates=None,
                    section_title=None,
                    parent_section=None,
                ),
            ),

            DocumentElement(
                element_id="profit-1",
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

            DocumentElement(
                element_id="footer-2",
                text="Page 2",
                element_type=ElementType.FOOTER,
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

    pipeline = FilterPipeline(
        filters=[
            EmptyTextFilter(),
            HeaderFooterFilter(),
            RepeatedElementFilter(),
        ],
    )

    result = pipeline.apply(document)

    assert len(result.elements) == 3

    assert [
        element.element_id
        for element in result.elements
    ] == [
        "title-1",
        "revenue-1",
        "profit-1",
    ]

    assert [
        element.text
        for element in result.elements
    ] == [
        "Annual Report",
        "Revenue increased by 20%.",
        "Profit increased by 15%.",
    ]

    assert result.document_id == "doc-123"
    assert result.filename == "annual_report.pdf"
    assert result.company_id == "company-456"
    assert result.page_count == 2