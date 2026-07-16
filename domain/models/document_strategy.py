from dataclasses import dataclass
from domain.enums.parser_type import ParserType
from domain.enums.parser_strategy import ParsingStrategy


@dataclass(slots=True)
class DocumentStrategy:

  parser: ParserType
  strategy: ParsingStrategy
  use_ocr: bool
  extract_tables: bool
  extract_images: bool
  description: str