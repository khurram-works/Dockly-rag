from dataclasses import dataclass

from domain.enums.element_type import ElementType
from domain.models.document_metadata import DocumentMetadata


@dataclass(slots=True)
class DocumentElement:
    text: str

    element_type: ElementType

    metadata: DocumentMetadata

    source_element: object | None = None