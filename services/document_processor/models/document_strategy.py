from dataclasses import dataclass
from .enums import ParserType, ParsingStrategy


@dataclass(slots=True)
class DocumentStrategy:
    parser: ParserType
    strategy: ParsingStrategy
    use_ocr: bool
    extract_tables: bool
    extract_images: bool
    description: str


@dataclass(slots=True)
class ParsedDocument:
    profile: DocumentProfile
    parser: ParserType
    strategy: ParsingStrategy
    page_count: int
    elements: list[DocumentElement]


@dataclass(slots=True)
class ChunkDocument:
    parsed_document: ParsedDocument
    chunks: list[Chunk]


from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class DocumentElement:
    text: str

    element_type: str

    metadata: DocumentMetadata


@dataclass(slots=True)
class DocumentMetadata:
    page_number: int

    section_title: str | None = None

    parent_section: str | None = None

    language: str | None = None