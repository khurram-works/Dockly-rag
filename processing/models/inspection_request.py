from dataclasses import dataclass

@dataclass(slots=True)
class InspectionRequest:
    document_id: str
    company_id: str
    filename: str
    file_size: int
    mime_type: str | None = None