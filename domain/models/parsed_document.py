from dataclasses import dataclass
from domain.models.document_profile import DocumentProfile
from domain.models.document_strategy import DocumentStrategy
from domain.models.document_element import DocumentElement

@dataclass(slots=True)
class ParsedDocument:
    profile: DocumentProfile
    strategy: DocumentStrategy

    page_count: int

    elements: list[DocumentElement]