from dataclasses import dataclass
from dataclasses import field
from domain.enums.parser_type import ParserType
from domain.enums.parser_strategy import ParsingStrategy


@dataclass(slots=True)
class DocumentStrategy:
    parser: ParserType
    parsing_strategy: ParsingStrategy

    # infer_table_structure: bool = False

    # languages: list[str] = field(default_factory=list)

    # extract_image_block_types: list[str] = field(default_factory=list)