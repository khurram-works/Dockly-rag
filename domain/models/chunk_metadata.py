from dataclasses import dataclass
from typing import Optional

@dataclass(slots=True)
class ChunkMetadata:
    page_numbers: list[int]
    languages: list[str]
    coordinates: Optional[list] = None
    source_element_ids: list[str] = None
    text_as_html: Optional[str] = None
    section_title: Optional[str] = None
    parent_section: Optional[str] = None