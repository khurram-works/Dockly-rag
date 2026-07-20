from unstructured.documents.elements import NarrativeText, Title

from domain.models.document_element import DocumentElement
from domain.enums.element_type import ElementType
from domain.models.document_metadata import DocumentMetadata
from domain.models.document_profile import DocumentProfile
from domain.models.parsed_document import ParsedDocument
from domain.models.document_chunking_strategy import (
    DocumentChunkingStrategy,
)

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
