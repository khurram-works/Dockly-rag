from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Embedding:
    values: tuple[float, ...]

    @property
    def dimension(self) -> int:
      return len(self.values)