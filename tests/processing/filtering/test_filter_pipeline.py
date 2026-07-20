from domain.enums.element_type import ElementType
from domain.models.document_element import DocumentElement
from domain.models.document_metadata import DocumentMetadata
from domain.models.parsed_document import ParsedDocument

from processing.filtering.filter_pipeline import FilterPipeline
from processing.filtering.filters.empty_text_filter import EmptyTextFilter
from processing.filtering.filters.header_footer_filter import HeaderFooterFilter


def test_filter_pipeline_removes_unwanted_elements():

    document = ParsedDocument(
        document_id="doc-123",
        filename="annual_report.pdf",
        company_id="company-456",
        page_count=1,
        elements=[
            DocumentElement(
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
                text="Company Confidential",
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
                text="Page 1",
                element_type=ElementType.FOOTER,
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

    pipeline = FilterPipeline(
        filters=[
            EmptyTextFilter(),
            HeaderFooterFilter(),
        ],
    )

    result = pipeline.apply(document)

    assert len(result.elements) == 2

    assert result.elements[0].text == "Annual Report"
    assert result.elements[1].text == "Revenue increased by 20%."
    assert result.document_id == "doc-123"
    assert result.filename == "annual_report.pdf"
    assert result.company_id == "company-456"