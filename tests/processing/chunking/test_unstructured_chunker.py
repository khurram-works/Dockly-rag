from unstructured.documents.elements import (
    Title,
    NarrativeText,
    ListItem,
    Table,
)

from domain.models.document_element import DocumentElement
from domain.enums.element_type import ElementType
from domain.models.document_metadata import DocumentMetadata
from domain.models.document_profile import DocumentProfile
from domain.models.parsed_document import ParsedDocument
from domain.models.document_chunking_strategy import (
    DocumentChunkingStrategy,
)
from domain.models.coordinates import Coordinates

from processing.chunking.unstructured_chunker import (
    UnstructuredChunker,
)

def test_unstructured_chunker_creates_document_chunks():

    title = Title(
        text="Company Overview"
    )

    paragraph_1 = NarrativeText(
        text=(
            "Our company builds software systems "
            "for business automation."
        )
    )

    paragraph_2 = NarrativeText(
        text=(
            "The platform helps companies automate "
            "repetitive operational workflows."
        )
    )

    document_elements = [
        DocumentElement(
            text=title.text,
            element_type=ElementType.TITLE,
            metadata=DocumentMetadata(
                page_number=1,
                languages=["eng"],
            ),
            source_element=title,
        ),

        DocumentElement(
            text=paragraph_1.text,
            element_type=ElementType.NARRATIVE,
            metadata=DocumentMetadata(
                page_number=1,
                languages=["eng"],
            ),
            source_element=paragraph_1,
        ),

        DocumentElement(
            text=paragraph_2.text,
            element_type=ElementType.NARRATIVE,
            metadata=DocumentMetadata(
                page_number=1,
                languages=["eng"],
            ),
            source_element=paragraph_2,
        ),
    ]


    document = ParsedDocument(
        document_id="doc-123",
        filename="company.pdf",
        company_id="company-456",
        page_count=1,
        elements=document_elements,
    )


    strategy = DocumentChunkingStrategy(
        max_characters=1500,
        new_after_n_chars=1000,
        combine_text_under_n_chars=1000,
        multipage_sections=True,
        include_orig_elements=True,
    )

    chunker = UnstructuredChunker(
        strategy=strategy,
    )



    chunks = chunker.chunk(document)

    assert len(chunks) > 0

    first_chunk = chunks[0]

    assert first_chunk.document_id == "doc-123"
    assert first_chunk.filename == "company.pdf"
    assert first_chunk.company_id == "company-456"

    assert first_chunk.text

    assert "Company Overview" in first_chunk.text

    assert first_chunk.metadata is not None

    assert 1 in first_chunk.metadata.page_numbers

    assert "eng" in first_chunk.metadata.languages



  
def test_unstructured_chunker_creates_multiple_chunks():

    title_1 = Title(
        text="Engineering"
    )

    paragraph_1 = NarrativeText(
        text=(
            "The engineering team builds backend systems "
            "and develops reliable software infrastructure."
        )
    )

    title_2 = Title(
        text="Operations"
    )

    paragraph_2 = NarrativeText(
        text=(
            "The operations team manages business workflows "
            "and ensures that internal processes run efficiently."
        )
    )



    document_elements = [
        DocumentElement(
            text=title_1.text,
            element_type=ElementType.TITLE,
            metadata=DocumentMetadata(
                page_number=1,
                languages=["eng"],
            ),
            source_element=title_1,
        ),

        DocumentElement(
            text=paragraph_1.text,
            element_type=ElementType.NARRATIVE,
            metadata=DocumentMetadata(
                page_number=1,
                languages=["eng"],
            ),
            source_element=paragraph_1,
        ),

        DocumentElement(
            text=title_2.text,
            element_type=ElementType.TITLE,
            metadata=DocumentMetadata(
                page_number=2,
                languages=["eng"],
            ),
            source_element=title_2,
        ),

        DocumentElement(
            text=paragraph_2.text,
            element_type=ElementType.NARRATIVE,
            metadata=DocumentMetadata(
                page_number=2,
                languages=["eng"],
            ),
            source_element=paragraph_2,
        ),
    ]


    document = ParsedDocument(
        document_id="doc-multi-123",
        filename="company.pdf",
        company_id="company-456",
        page_count=2,
        elements=document_elements,
    )


    strategy = DocumentChunkingStrategy(
        max_characters=150,
        new_after_n_chars=100,
        combine_text_under_n_chars=0,
        multipage_sections=True,
        include_orig_elements=True,
    )


    chunker = UnstructuredChunker(
        strategy=strategy,
    )

    chunks = chunker.chunk(document)

    assert len(chunks) == 2
    first_chunk = chunks[0]
    second_chunk = chunks[1]
    assert first_chunk.chunk_index == 0
    assert second_chunk.chunk_index == 1

    assert first_chunk.document_id == "doc-multi-123"
    assert second_chunk.document_id == "doc-multi-123"

    assert first_chunk.company_id == "company-456"
    assert second_chunk.company_id == "company-456"

    assert first_chunk.filename == "company.pdf"
    assert second_chunk.filename == "company.pdf"

    assert "Engineering" in first_chunk.text
    assert "backend systems" in first_chunk.text

    assert "Operations" in second_chunk.text
    assert "business workflows" in second_chunk.text

    assert "Operations" not in first_chunk.text
    assert "Engineering" not in second_chunk.text

    assert first_chunk.metadata.page_numbers == [1]
    assert second_chunk.metadata.page_numbers == [2]

    assert first_chunk.metadata.languages == ["eng"]
    assert second_chunk.metadata.languages == ["eng"]



def test_unstructured_chunker_aggregates_metadata_from_multiple_pages():

    title = Title(
        text="Company History"
    )

    paragraph_1 = NarrativeText(
        text=(
            "The company was founded to build reliable "
            "software systems for growing businesses."
        )
    )

    paragraph_2 = NarrativeText(
        text=(
            "The company expanded its platform and began "
            "serving customers across multiple industries."
        )
    )

    paragraph_3 = NarrativeText(
        text=(
            "Today, the platform automates complex business "
            "operations and improves organizational efficiency."
        )
    )

    document_elements = [
        DocumentElement(
            text=title.text,
            element_type=ElementType.TITLE,
            metadata=DocumentMetadata(
                page_number=1,
                languages=["eng"],
            ),
            source_element=title,
        ),

        DocumentElement(
            text=paragraph_1.text,
            element_type=ElementType.NARRATIVE,
            metadata=DocumentMetadata(
                page_number=1,
                languages=["eng"],
            ),
            source_element=paragraph_1,
        ),

        DocumentElement(
            text=paragraph_2.text,
            element_type=ElementType.NARRATIVE,
            metadata=DocumentMetadata(
                page_number=2,
                languages=["eng"],
            ),
            source_element=paragraph_2,
        ),

        DocumentElement(
            text=paragraph_3.text,
            element_type=ElementType.NARRATIVE,
            metadata=DocumentMetadata(
                page_number=3,
                languages=["eng"],
            ),
            source_element=paragraph_3,
        ),
    ]

    document = ParsedDocument(
        document_id="doc-pages-123",
        filename="history.pdf",
        company_id="company-456",
        page_count=3,
        elements=document_elements,
    )

    strategy = DocumentChunkingStrategy(
        max_characters=1500,
        new_after_n_chars=1200,
        combine_text_under_n_chars=1500,
        multipage_sections=True,
        include_orig_elements=True,
    )


    chunker = UnstructuredChunker(
        strategy=strategy
    )

    chunks = chunker.chunk(document)

    assert len(chunks) == 1

    chunk = chunks[0]
    assert chunk.metadata.page_numbers == [1, 2, 3]
    assert chunk.metadata.languages == ["eng"]

    assert "Company History" in chunk.text
    assert "founded" in chunk.text
    assert "expanded" in chunk.text
    assert "Today" in chunk.text

    assert chunk.chunk_index == 0
    assert chunk.document_id == "doc-pages-123"


def test_unstructured_chunker_deduplicates_chunk_metadata():

    title = Title(
        text="Company Overview"
    )

    paragraph_1 = NarrativeText(
        text="The company builds software systems."
    )

    paragraph_2 = NarrativeText(
        text="The platform automates business workflows."
    )


    document_elements = [
        DocumentElement(
            text=title.text,
            element_type=ElementType.TITLE,
            metadata=DocumentMetadata(
                page_number=1,
                languages=["eng"],
            ),
            source_element=title
        ),

        DocumentElement(
            text=paragraph_1.text,
            element_type=ElementType.NARRATIVE,
            metadata=DocumentMetadata(
                page_number=1,
                languages=["eng","urd"],
            ),
            source_element=paragraph_1
        ),

        DocumentElement(
            text=paragraph_2.text,
            element_type=ElementType.NARRATIVE,
            metadata=DocumentMetadata(
                page_number=2,
                languages=["eng"],
            ),
            source_element=paragraph_2
        )
    ]


    document = ParsedDocument(
        document_id="urdu-123",
        company_id="google-123",
        filename="google.pdf",
        page_count=2,
        elements=document_elements
    )

    strategy = DocumentChunkingStrategy(
        max_characters=1500,
        new_after_n_chars=1200,
        combine_text_under_n_chars=1500,
        multipage_sections=True,
        include_orig_elements=True,
    )

    chunker = UnstructuredChunker(
        strategy=strategy
    )

    chunks = chunker.chunk(document)

    assert len(chunks) == 1
    
    chunk = chunks[0]

    assert chunk.metadata.page_numbers == [1, 2]
    assert chunk.metadata.languages == ["eng", "urd"]


def test_unstructured_chunker_preserves_coordinates():
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

    title = Title(
        text="Company Overview"
    )

    paragraph_1 = NarrativeText(
        text="The company builds software systems."
    )

    paragraph_2 = NarrativeText(
        text="The platform automates business workflows."
    )


    document_elements = [
        DocumentElement(
            text=title.text,
            element_type=ElementType.TITLE,
            metadata=DocumentMetadata(
                page_number=1,
                languages=["eng"],
            ),
            source_element=title
        ),

        DocumentElement(
            text=paragraph_1.text,
            element_type=ElementType.NARRATIVE,
            metadata=DocumentMetadata(
                page_number=1,
                languages=["eng"],
                coordinates=coordinates_1,
            ),
            source_element=paragraph_1
        ),

        DocumentElement(
            text=paragraph_2.text,
            element_type=ElementType.NARRATIVE,
            metadata=DocumentMetadata(
                page_number=1,
                languages=["eng"],
                coordinates=coordinates_2,
            ),
            source_element=paragraph_2
        )
    ]



    document = ParsedDocument(
        document_id="urdu-123",
        company_id="google-123",
        filename="google.pdf",
        page_count=1,
        elements=document_elements
    )

    strategy = DocumentChunkingStrategy(
        max_characters=1500,
        new_after_n_chars=1200,
        combine_text_under_n_chars=1500,
        multipage_sections=True,
        include_orig_elements=True,
    )

    chunker = UnstructuredChunker(
        strategy=strategy
    )

    chunks = chunker.chunk(document)

    assert len(chunks) == 1
    
    chunk = chunks[0]

    assert chunk.metadata.coordinates is not None
    assert len(chunk.metadata.coordinates) == 2
    assert chunk.metadata.coordinates[0] == coordinates_1
    assert chunk.metadata.coordinates[1] == coordinates_2



def test_unstructured_chunker_handles_mixed_element_types():

    title = Title(
        text="Company Overview"
    )

    paragraph = NarrativeText(
        text=(
            "Our company builds software systems "
            "for business automation."
        )
    )

    list_item_1 = ListItem(
        text="Automated business workflows"
    )

    list_item_2 = ListItem(
        text="AI-powered operational tools"
    )

    table = Table(
        text=(
            "Product | Revenue\n"
            "Platform | $1M"
        )
    )

    document_elements = [
        DocumentElement(
            text=title.text,
            element_type=ElementType.TITLE,
            metadata=DocumentMetadata(
                page_number=1,
                languages=["eng"],
            ),
            source_element=title,
        ),

        DocumentElement(
            text=paragraph.text,
            element_type=ElementType.NARRATIVE,
            metadata=DocumentMetadata(
                page_number=1,
                languages=["eng"],
            ),
            source_element=paragraph,
        ),

        DocumentElement(
            text=list_item_1.text,
            element_type=ElementType.LIST,
            metadata=DocumentMetadata(
                page_number=1,
                languages=["eng"],
            ),
            source_element=list_item_1,
        ),

        DocumentElement(
            text=list_item_2.text,
            element_type=ElementType.LIST,
            metadata=DocumentMetadata(
                page_number=1,
                languages=["eng"],
            ),
            source_element=list_item_2,
        ),

        DocumentElement(
            text=table.text,
            element_type=ElementType.TABLE,
            metadata=DocumentMetadata(
                page_number=1,
                languages=["eng"],
            ),
            source_element=table,
        ),
    ]

    document = ParsedDocument(
        document_id="doc-mixed-123",
        company_id="company-456",
        filename="company-report.pdf",
        page_count=1,
        elements=document_elements,
    )

    strategy = DocumentChunkingStrategy(
        max_characters=1500,
        new_after_n_chars=1200,
        combine_text_under_n_chars=1500,
        multipage_sections=True,
        include_orig_elements=True,
    )

    chunker = UnstructuredChunker(
        strategy=strategy,
    )

    chunks = chunker.chunk(document)

    assert len(chunks) == 2

    text_chunk = chunks[0]
    table_chunk = chunks[1]

    assert text_chunk.document_id == "doc-mixed-123"
    assert text_chunk.company_id == "company-456"
    assert text_chunk.filename == "company-report.pdf"
    
    assert "Company Overview" in text_chunk.text
    assert "Our company builds software systems" in text_chunk.text
    assert "Automated business workflows" in text_chunk.text
    assert "AI-powered operational tools" in text_chunk.text
    
    assert text_chunk.metadata.page_numbers == [1]
    assert text_chunk.metadata.languages == ["eng"]

    assert table_chunk.document_id == "doc-mixed-123"
    assert table_chunk.company_id == "company-456"
    assert table_chunk.filename == "company-report.pdf"
    
    assert "Product | Revenue" in table_chunk.text
    assert "Platform | $1M" in table_chunk.text
    
    assert table_chunk.metadata.page_numbers == [1]
    assert table_chunk.metadata.languages == ["eng"]










