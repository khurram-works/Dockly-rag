from dataclasses import dataclass

from domain.models.coordinates import Coordinates


@dataclass(slots=True)
class DocumentMetadata:
    page_number: int | None

    languages: list[str] | None = None

    section_title: str | None = None

    parent_section: str | None = None

    coordinates: Coordinates | None = None

    text_as_html: str | None = None