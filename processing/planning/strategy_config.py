from domain.enums.parser_strategy import ParsingStrategy
from domain.enums.parser_type import ParserType
from domain.models.document_strategy import DocumentStrategy


STRATEGY_CONFIG: dict[str, DocumentStrategy] = {

    ".pdf": DocumentStrategy(
        parser=ParserType.PDF,
        parsing_strategy=ParsingStrategy.HI_RES,
    ),

    ".docx": DocumentStrategy(
        parser=ParserType.GENERIC,
        parsing_strategy=ParsingStrategy.FAST,
    ),

    ".pptx": DocumentStrategy(
        parser=ParserType.GENERIC,
        parsing_strategy=ParsingStrategy.FAST,
    ),

    ".html": DocumentStrategy(
        parser=ParserType.GENERIC,
        parsing_strategy=ParsingStrategy.FAST,
    ),

    ".txt": DocumentStrategy(
        parser=ParserType.GENERIC,
        parsing_strategy=ParsingStrategy.FAST,
    ),

    ".md": DocumentStrategy(
        parser=ParserType.GENERIC,
        parsing_strategy=ParsingStrategy.FAST,
    ),

    ".csv": DocumentStrategy(
        parser=ParserType.GENERIC,
        parsing_strategy=ParsingStrategy.FAST,
    ),

    ".epub": DocumentStrategy(
        parser=ParserType.GENERIC,
        parsing_strategy=ParsingStrategy.FAST,
    ),

    ".jpg": DocumentStrategy(
        parser=ParserType.IMAGE,
        parsing_strategy=ParsingStrategy.OCR_ONLY,
    ),

    ".jpeg": DocumentStrategy(
        parser=ParserType.IMAGE,
        parsing_strategy=ParsingStrategy.OCR_ONLY,
    ),

    ".png": DocumentStrategy(
        parser=ParserType.IMAGE,
        parsing_strategy=ParsingStrategy.OCR_ONLY,
    ),
}