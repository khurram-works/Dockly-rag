from unstructured.chunking.title import chunk_by_title

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

        source_elements = [
            element.source_element
            for element in document.elements
            if element.source_element is not None
        ]

        source_element_map = {
            element.source_element.id: element
            for element in document.elements
            if element.source_element is not None
        }

        chunks = chunk_by_title(
            elements=source_elements,
            max_characters=self._strategy.max_characters,
            new_after_n_chars=self._strategy.new_after_n_chars,
            combine_text_under_n_chars=(
                self._strategy.combine_text_under_n_chars
            ),
            multipage_sections=self._strategy.multipage_sections,
            include_orig_elements=self._strategy.include_orig_elements,
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
        source_element_map: dict[str, DocumentElement]
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
        source_element_map: dict[str, DocumentElement]
    ) -> ChunkMetadata:

        page_numbers: list[int] = []
        languages: list[str] = []
        coordinates: list[Coordinates] = []
    
        original_elements = chunk.metadata.orig_elements or []
    
        for original_element in original_elements:
    
            domain_element = source_element_map.get(
                original_element.id
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
    
        return ChunkMetadata(
            page_numbers=list(dict.fromkeys(page_numbers)),
            languages=list(dict.fromkeys(languages)),
            coordinates=coordinates or None,
        )