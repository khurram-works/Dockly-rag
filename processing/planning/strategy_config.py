# from domain.models.document_strategy import DocumentStrategy
# from domain.enums.parser_strategy import ParsingStrategy
# from domain.enums.parser_type import ParserType


# STRATEGY_CONFIG = {

#     ".pdf": DocumentStrategy(
#         parser=ParserType.PDF,
#         strategy=ParsingStrategy.HI_RES,
#         # use_ocr=False,
#         # extract_tables=True,
#         # extract_images=True,
#         # description="High-resolution layout parsing for PDFs."
#     ),

#     ".png": DocumentStrategy(
#         parser=ParserType.IMAGE,
#         strategy=ParsingStrategy.OCR_ONLY,
#         # use_ocr=True,
#         # extract_tables=False,
#         # extract_images=False,
#         # description="OCR strategy for image documents."
#     ),

#     ".jpg": DocumentStrategy(
#         parser=ParserType.IMAGE,
#         strategy=ParsingStrategy.OCR_ONLY,
#         # use_ocr=True,
#         # extract_tables=False,
#         # extract_images=False,
#         # description="OCR strategy for image documents."
#     ),

#     ".jpeg": DocumentStrategy(
#         parser=ParserType.IMAGE,
#         strategy=ParsingStrategy.OCR_ONLY,
#         # use_ocr=True,
#         # extract_tables=False,
#         # extract_images=False,
#         # description="OCR strategy for image documents."
#     ),

#     ".docx": DocumentStrategy(
#         parser=ParserType.GENERIC,
#         strategy=ParsingStrategy.FAST,
#         # use_ocr=False,
#         # extract_tables=False,
#         # extract_images=False,
#         # description="Fast parsing for structured Office documents."
#     ),

#     ".txt": DocumentStrategy(
#         parser=ParserType.GENERIC,
#         strategy=ParsingStrategy.FAST,
#         # use_ocr=False,
#         # extract_tables=False,
#         # extract_images=False,
#         # description="Fast parsing for plain text."
#     ),

#     ".md": DocumentStrategy(
#         parser=ParserType.GENERIC,
#         strategy=ParsingStrategy.FAST,
#         # use_ocr=False,
#         # extract_tables=False,
#         # extract_images=False,
#         # description="Fast parsing for Markdown."
#     ),

#     ".html": DocumentStrategy(
#         parser=ParserType.GENERIC,
#         strategy=ParsingStrategy.FAST,
#         # use_ocr=False,
#         # extract_tables=False,
#         # extract_images=False,
#         # description="Fast parsing for HTML."
#     ),

#     ".csv": DocumentStrategy(
#         parser=ParserType.GENERIC,
#         strategy=ParsingStrategy.FAST,
#         # use_ocr=False,
#         # extract_tables=False,
#         # extract_images=False,
#         # description="Fast parsing for CSV."
#     ),

#     ".epub": DocumentStrategy(
#         parser=ParserType.GENERIC,
#         strategy=ParsingStrategy.FAST,
#         # use_ocr=False,
#         # extract_tables=False,
#         # extract_images=False,
#         # description="Fast parsing for EPUB."
#     ),

#     ".pptx": DocumentStrategy(
#         parser=ParserType.GENERIC,
#         strategy=ParsingStrategy.FAST,
#         # use_ocr=False,
#         # extract_tables=False,
#         # extract_images=False,
#         # description="Fast parsing for PowerPoint."
#     ),
# }


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