from unstructured.chunking.title import chunk_by_title

from domain.enums.element_type import ElementType

from domain.models.document_chunk import DocumentChunk
from domain.models.document_chunking_strategy import (
    DocumentChunkingStrategy,
)
from domain.models.document_element import DocumentElement
from domain.models.chunk_metadata import ChunkMetadata
from domain.models.parsed_document import ParsedDocument
from domain.models.coordinates import Coordinates

from processing.chunking.base_chunker import BaseChunker


class UnstructuredChunker(BaseChunker):

    def __init__(
        self,
        strategy: DocumentChunkingStrategy,
    ) -> None:

        self._strategy = strategy

    def chunk(
        self,
        document: ParsedDocument,
    ) -> list[DocumentChunk]:

        if not document.elements:
            return []

        source_elements = [
            element.source_element
            for element in document.elements
            if element.source_element is not None
        ]

        if not source_elements:
            return []

        source_element_map = {}

        for domain_element in document.elements:
        
            source_element = domain_element.source_element
        
            if source_element is None:
                continue
        
            source_element_id = getattr(
                source_element,
                "id",
                None,
            )
        
            if source_element_id is None:
                continue
        
            source_element_map[source_element_id] = domain_element
        
        chunks = chunk_by_title(
            elements=source_elements,
            max_characters=self._strategy.max_characters,
            new_after_n_chars=self._strategy.new_after_n_chars,
            combine_text_under_n_chars=(
                self._strategy.combine_text_under_n_chars
            ),
            multipage_sections=self._strategy.multipage_sections,
            include_orig_elements=True,
        )

        return [
            self._to_document_chunk(
                document=document,
                chunk=chunk,
                chunk_index=index,
                source_element_map=source_element_map,
            )
            for index, chunk in enumerate(chunks)
        ]

    def _to_document_chunk(
        self,
        document: ParsedDocument,
        chunk,
        chunk_index: int,
        source_element_map: dict[str, DocumentElement],
    ) -> DocumentChunk:

        return DocumentChunk(
            document_id=document.document_id,
            filename=document.filename,
            company_id=document.company_id,
            chunk_index=chunk_index,
            text=chunk.text,
            metadata=self._to_chunk_metadata(
                chunk,
                source_element_map,
            ),
        )

    def _to_chunk_metadata(
        self,
        chunk,
        source_element_map: dict[str, DocumentElement],
    ) -> ChunkMetadata:

        page_numbers: list[int] = []
        languages: list[str] = []
        coordinates: list[Coordinates] = []
        source_element_ids: list[str] = []

        chunk_metadata = getattr(
            chunk,
            "metadata",
            None,
        )

        original_elements = getattr(
            chunk_metadata,
            "orig_elements",
            None,
        ) or []

        text_as_html = None

        for original_element in original_elements:

            original_element_id = getattr(
                original_element,
                "id",
                None,
            )
        
            if original_element_id is None:
                continue
        
            domain_element = source_element_map.get(
                original_element_id,
            )
        
            if domain_element is None:
                continue

            metadata = domain_element.metadata

            if metadata.page_number is not None:
                page_numbers.append(
                    metadata.page_number
                )

            if metadata.languages:
                languages.extend(
                    metadata.languages
                )

            if metadata.coordinates is not None:
                coordinates.append(
                    metadata.coordinates
                )

            if domain_element.element_id is not None:
                source_element_ids.append(
                    domain_element.element_id
                )

            if (
                domain_element.element_type
                == ElementType.TABLE
                and metadata.text_as_html is not None
            ):
                text_as_html = metadata.text_as_html

        return ChunkMetadata(
            page_numbers=list(
                dict.fromkeys(page_numbers)
            ),
            languages=list(
                dict.fromkeys(languages)
            ),
            coordinates=coordinates or None,
            source_element_ids=list(
                dict.fromkeys(source_element_ids)
            ),
            text_as_html=text_as_html,
        )