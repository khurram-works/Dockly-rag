from dataclasses import dataclass
from domain.models.document_element import DocumentElement

@dataclass(slots=True)
class ParsedDocument:
    document_id: str
    filename: str
    company_id: str
    page_count: int | None
    elements: list[DocumentElement]