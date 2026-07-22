from unstructured.documents.elements import (
NarrativeText,
Table,
Title,
)

from domain.enums.element_type import ElementType

from domain.models.chunk_metadata import ChunkMetadata
from domain.models.coordinates import Coordinates
from domain.models.document_element import DocumentElement
from domain.models.document_metadata import DocumentMetadata
from domain.models.document_chunking_strategy import (
DocumentChunkingStrategy,
)
from domain.models.parsed_document import ParsedDocument

from processing.chunking.unstructured_chunker import (
UnstructuredChunker,
)

def create_document_element(
    source_element,
    element_type: ElementType,
    page_number: int,
    languages: list[str],
    coordinates: Coordinates | None = None,
    text_as_html: str | None = None,
    ) -> DocumentElement:
    
    return DocumentElement(
        element_id=source_element.id,
        text=source_element.text,
        element_type=element_type,
        metadata=DocumentMetadata(
            page_number=page_number,
            languages=languages,
            coordinates=coordinates,
            section_title=None,
            parent_section=None,
            text_as_html=text_as_html,
        ),
        source_element=source_element,
    )


def create_chunker() -> UnstructuredChunker:


    strategy = DocumentChunkingStrategy(
        max_characters=1000,
        new_after_n_chars=800,
        combine_text_under_n_chars=200,
        multipage_sections=True,
        include_orig_elements=True,
    )
    
    return UnstructuredChunker(
        strategy=strategy,
    )


def test_empty_document_returns_no_chunks():


    document = ParsedDocument(
        document_id="doc-123",
        filename="company.pdf",
        company_id="company-456",
        page_count=0,
        elements=[],
    )
    
    chunker = create_chunker()
    
    result = chunker.chunk(document)
    
    assert result == []


def test_chunker_creates_document_chunk():


    title = Title(
        "Company Overview",
    )
    
    narrative = NarrativeText(
        "ACME builds software products.",
    )
    
    document = ParsedDocument(
        document_id="doc-123",
        filename="company.pdf",
        company_id="company-456",
        page_count=1,
        elements=[
            create_document_element(
                source_element=title,
                element_type=ElementType.TITLE,
                page_number=1,
                languages=["eng"],
            ),
            create_document_element(
                source_element=narrative,
                element_type=ElementType.NARRATIVE,
                page_number=1,
                languages=["eng"],
            ),
        ],
    )
    
    chunker = create_chunker()
    
    result = chunker.chunk(document)
    
    assert len(result) == 1
    
    chunk = result[0]
    
    assert chunk.document_id == "doc-123"
    
    assert chunk.filename == "company.pdf"
    
    assert chunk.company_id == "company-456"
    
    assert chunk.chunk_index == 0
    
    assert "Company Overview" in chunk.text
    
    assert "ACME builds software products." in chunk.text


def test_chunker_preserves_source_element_ids_and_metadata():


    title = Title(
        "Company Overview",
    )
    
    narrative = NarrativeText(
        "ACME builds software products.",
    )
    
    title_domain_element = create_document_element(
        source_element=title,
        element_type=ElementType.TITLE,
        page_number=1,
        languages=["eng"],
    )
    
    narrative_domain_element = create_document_element(
        source_element=narrative,
        element_type=ElementType.NARRATIVE,
        page_number=2,
        languages=["eng"],
    )
    
    document = ParsedDocument(
        document_id="doc-123",
        filename="company.pdf",
        company_id="company-456",
        page_count=2,
        elements=[
            title_domain_element,
            narrative_domain_element,
        ],
    )
    
    chunker = create_chunker()
    
    result = chunker.chunk(document)
    
    assert len(result) == 1
    
    chunk = result[0]
    
    assert set(
        chunk.metadata.source_element_ids
    ) == {
        title_domain_element.element_id,
        narrative_domain_element.element_id,
    }
    
    assert chunk.metadata.page_numbers == [
        1,
        2,
    ]
    
    assert chunk.metadata.languages == [
        "eng",
    ]


def test_chunker_deduplicates_metadata():


    title = Title(
        "Company Overview",
    )
    
    paragraph_1 = NarrativeText(
        "First paragraph.",
    )
    
    paragraph_2 = NarrativeText(
        "Second paragraph.",
    )
    
    document = ParsedDocument(
        document_id="doc-123",
        filename="company.pdf",
        company_id="company-456",
        page_count=1,
        elements=[
            create_document_element(
                source_element=title,
                element_type=ElementType.TITLE,
                page_number=1,
                languages=["eng"],
            ),
            create_document_element(
                source_element=paragraph_1,
                element_type=ElementType.NARRATIVE,
                page_number=1,
                languages=["eng"],
            ),
            create_document_element(
                source_element=paragraph_2,
                element_type=ElementType.NARRATIVE,
                page_number=1,
                languages=["eng"],
            ),
        ],
    )
    
    chunker = create_chunker()
    
    result = chunker.chunk(document)
    
    assert len(result) == 1
    
    chunk = result[0]
    
    assert chunk.metadata.page_numbers == [
        1,
    ]
    
    assert chunk.metadata.languages == [
        "eng",
    ]


def test_chunker_preserves_table_html():

    
    html = (
        "<table>"
        "<tr>"
        "<td>Product</td>"
        "<td>Revenue</td>"
        "</tr>"
        "</table>"
    )
    
    table = Table(
        "Product | Revenue\n"
        "Platform | $1M",
    )
    
    document = ParsedDocument(
        document_id="doc-123",
        filename="financial-report.pdf",
        company_id="company-456",
        page_count=1,
        elements=[
            create_document_element(
                source_element=table,
                element_type=ElementType.TABLE,
                page_number=1,
                languages=["eng"],
                text_as_html=html,
            ),
        ],
    )
    
    chunker = create_chunker()
    
    result = chunker.chunk(document)
    
    assert len(result) == 1
    
    chunk = result[0]
    
    assert chunk.metadata.text_as_html == html


def test_chunker_preserves_coordinates():

    
    coordinates_1 = Coordinates(
        points=(
            (0.0, 0.0),
            (100.0, 0.0),
            (100.0, 50.0),
            (0.0, 50.0),
        )
    )
    
    coordinates_2 = Coordinates(
        points=(
            (0.0, 60.0),
            (100.0, 60.0),
            (100.0, 110.0),
            (0.0, 110.0),
        )
    )
    
    paragraph_1 = NarrativeText(
        "The company builds software systems.",
    )
    
    paragraph_2 = NarrativeText(
        "The platform automates business workflows.",
    )
    
    document = ParsedDocument(
        document_id="doc-123",
        filename="company.pdf",
        company_id="company-456",
        page_count=1,
        elements=[
            create_document_element(
                source_element=paragraph_1,
                element_type=ElementType.NARRATIVE,
                page_number=1,
                languages=["eng"],
                coordinates=coordinates_1,
            ),
            create_document_element(
                source_element=paragraph_2,
                element_type=ElementType.NARRATIVE,
                page_number=1,
                languages=["eng"],
                coordinates=coordinates_2,
            ),
        ],
    )
    
    chunker = create_chunker()
    
    result = chunker.chunk(document)
    
    assert len(result) == 1
    
    chunk = result[0]
    
    assert chunk.metadata.coordinates == [
        coordinates_1,
        coordinates_2,
    ]


def test_chunker_ignores_domain_elements_without_source_elements():

    
    title = Title(
        "Company Overview",
    )
    
    domain_element_with_source = create_document_element(
        source_element=title,
        element_type=ElementType.TITLE,
        page_number=1,
        languages=["eng"],
    )
    
    domain_element_without_source = DocumentElement(
        element_id="domain-only-element",
        text="This element has no source element.",
        element_type=ElementType.NARRATIVE,
        metadata=DocumentMetadata(
            page_number=1,
            languages=["eng"],
            coordinates=None,
            section_title=None,
            parent_section=None,
            text_as_html=None,
        ),
        source_element=None,
    )
    
    document = ParsedDocument(
        document_id="doc-123",
        filename="company.pdf",
        company_id="company-456",
        page_count=1,
        elements=[
            domain_element_with_source,
            domain_element_without_source,
        ],
    )
    
    chunker = create_chunker()
    
    result = chunker.chunk(document)
    
    assert len(result) == 1
    
    chunk = result[0]
    
    assert (
        "Company Overview"
        in chunk.text
    )
    
    assert (
        "This element has no source element."
        not in chunk.text
    )
    
    assert (
        domain_element_without_source.element_id
        not in chunk.metadata.source_element_ids
    )
    