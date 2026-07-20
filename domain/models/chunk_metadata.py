from dataclasses import dataclass

from domain.models.coordinates import Coordinates


@dataclass(slots=True)
class ChunkMetadata:
    page_numbers: list[int]

    languages: list[str]

    section_title: str | None = None

    parent_section: str | None = None

    coordinates: list[Coordinates] | None = None