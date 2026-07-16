from dataclasses import dataclass

@dataclass(slots=True)
class DocumentMetadata:
  page_number: int

  section_title: str | None = None

  parent_section: str | None = None

  language: str | None = None