from unstructured.chunking.title import chunk_by_title

from domain.models.document_chunk import DocumentChunk
from domain.models.document_chunking_strategy import (
    DocumentChunkingStrategy,
)
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
            )
            for index, chunk in enumerate(chunks)
        ]

    def _to_document_chunk(
    self,
    document: ParsedDocument,
    chunk,
    chunk_index: int,
) -> DocumentChunk:

        print("\nRAW UNSTRUCTURED CHUNK METADATA:")
        print(chunk.metadata)
    
        print("\nRAW ORIG ELEMENTS:")
        print(chunk.metadata.orig_elements)
    
        return DocumentChunk(
        document_id=document.document_id,
        filename=document.filename,
        company_id=document.company_id,
        chunk_index=chunk_index,
        text=chunk.text,
        metadata=self._to_chunk_metadata(chunk),
    )

    def _to_chunk_metadata(
        self,
        chunk,
    ) -> ChunkMetadata:

        metadata = chunk.metadata

        if metadata is None:
            return ChunkMetadata(
                page_numbers=[],
                languages=[],
                coordinates=None,
            )

        original_elements = metadata.orig_elements or []

        page_numbers = []
        languages = []
        coordinates = []

        for element in original_elements:

            element_metadata = element.metadata

            if element_metadata is None:
                continue

            if element_metadata.page_number is not None:
                page_numbers.append(
                    element_metadata.page_number
                )

            if element_metadata.languages:
                languages.extend(
                    element_metadata.languages
                )

            if element_metadata.coordinates is not None:

                converted_coordinates = self._to_coordinates(
                    element_metadata.coordinates
                )

                if converted_coordinates is not None:
                    coordinates.append(
                        converted_coordinates
                    )

        return ChunkMetadata(
            page_numbers=list(dict.fromkeys(page_numbers)),
            languages=list(dict.fromkeys(languages)),
            coordinates=coordinates or None,
        )