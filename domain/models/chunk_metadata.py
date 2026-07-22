from dataclasses import dataclass
from typing import Optional

from domain.models.coordinates import Coordinates


@dataclass
class ChunkMetadata:

    page_numbers: list[int]

    languages: list[str]

    coordinates: Optional[list[Coordinates]]

    source_element_ids: list[str]

    text_as_html: Optional[str] = None