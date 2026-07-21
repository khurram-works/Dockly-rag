from dataclasses import dataclass
from typing import Any


@dataclass(slots=True, frozen=True)
class IndexablePoint:

    point_id: str

    vector: tuple[float, ...]

    payload: dict[str, Any]