from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class DocumentProcessingResult:

    document_id: str

    page_count: int | None

    chunks_created: int