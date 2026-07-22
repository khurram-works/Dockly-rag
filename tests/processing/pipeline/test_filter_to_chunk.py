from unstructured.documents.elements import (
    NarrativeText,
    Title,
)

from domain.enums.element_type import ElementType

from domain.models.document_element import DocumentElement
from domain.models.document_metadata import DocumentMetadata
from domain.models.document_chunking_strategy import (
    DocumentChunkingStrategy,
)
from domain.models.parsed_document import ParsedDocument

from processing.chunking.unstructured_chunker import (
    UnstructuredChunker,
)

from processing.filtering.filter_pipeline import (
    FilterPipeline,
)

from processing.filtering.filters.empty_text_filter import (
    EmptyTextFilter,
)

from processing.filtering.filters.header_footer_filter import (
    HeaderFooterFilter,
)

from processing.filtering.filters.repeated_element_filter import (
    RepeatedElementFilter,
)


def create_document_element(
    source_element,
    element_type: ElementType,
    page_number: int,
    languages: list[str],
    element_id: str | None = None,
):

    return DocumentElement(
        element_id=(
            element_id
            or source_element.id
        ),
        text=source_element.text,
        element_type=element_type,
        metadata=DocumentMetadata(
            page_number=page_number,
            languages=languages,
            coordinates=None,
            section_title=None,
            parent_section=None,
            text_as_html=None,
        ),
        source_element=source_element,
    )


def test_filtering_before_chunking_removes_unwanted_content():

    title = Title(
        "Annual Report",
    )

    header = NarrativeText(
        "ACME Corporation — Confidential",
    )

    revenue = NarrativeText(
        "Revenue increased by 20 percent.",
    )

    repeated_header = NarrativeText(
        "ACME Corporation — Confidential",
    )

    profit = NarrativeText(
        "Profit increased by 15 percent.",
    )

    footer = NarrativeText(
        "Page 2",
    )

    document = ParsedDocument(
        document_id="doc-123",
        filename="annual-report.pdf",
        company_id="company-456",
        page_count=2,
        elements=[
            create_document_element(
                source_element=title,
                element_type=ElementType.TITLE,
                page_number=1,
                languages=["eng"],
            ),
            create_document_element(
                source_element=header,
                element_type=ElementType.HEADER,
                page_number=1,
                languages=["eng"],
            ),
            create_document_element(
                source_element=NarrativeText("   "),
                element_type=ElementType.NARRATIVE,
                page_number=1,
                languages=["eng"],
            ),
            create_document_element(
                source_element=revenue,
                element_type=ElementType.NARRATIVE,
                page_number=1,
                languages=["eng"],
            ),
            create_document_element(
                source_element=repeated_header,
                element_type=ElementType.HEADER,
                page_number=2,
                languages=["eng"],
            ),
            create_document_element(
                source_element=profit,
                element_type=ElementType.NARRATIVE,
                page_number=2,
                languages=["eng"],
            ),
            create_document_element(
                source_element=footer,
                element_type=ElementType.FOOTER,
                page_number=2,
                languages=["eng"],
            ),
        ],
    )

    filter_pipeline = FilterPipeline(
        filters=[
            EmptyTextFilter(),
            HeaderFooterFilter(),
            RepeatedElementFilter(),
        ],
    )

    filtered_document = filter_pipeline.apply(
        document
    )

    chunking_strategy = DocumentChunkingStrategy(
        max_characters=1000,
        new_after_n_chars=800,
        combine_text_under_n_chars=200,
        multipage_sections=True,
        include_orig_elements=True,
    )

    chunker = UnstructuredChunker(
        strategy=chunking_strategy,
    )

    chunks = chunker.chunk(
        filtered_document
    )

    assert len(chunks) >= 1

    combined_text = "\n".join(
        chunk.text
        for chunk in chunks
    )

    assert "Annual Report" in combined_text

    assert (
        "Revenue increased by 20 percent."
        in combined_text
    )

    assert (
        "Profit increased by 15 percent."
        in combined_text
    )

    assert (
        "ACME Corporation — Confidential"
        not in combined_text
    )

    assert "Page 2" not in combined_text

    assert "   " not in combined_text