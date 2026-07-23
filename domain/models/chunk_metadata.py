from dataclasses import dataclass

from domain.models.coordinates import Coordinates


@dataclass(slots=True)
class ChunkMetadata:

    page_numbers: list[int]

    languages: list[str]

    coordinates: list[Coordinates] | None

    source_element_ids: list[str]

    text_as_html: str | None = None