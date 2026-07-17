from dataclasses import dataclass

@dataclass(slots=True)
class Coordinates:
  points: tuple[tuple[float, float], ...]