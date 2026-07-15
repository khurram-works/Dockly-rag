from enum import Enum

class ParserType(str, Enum):
  AUTO = "auto"
  PDF = "pdf"
  GENERIC = "generic"


class ParsingStrategy(str, Enum):
  FAST = "fast"
  HI_RES = "hi_res"
  OCR_ONLY = "ocr_only"


class ElementType(str, Enum):
  TITLE = "Title"
  NARRATIVE = "NarrativeText"
  TABLE = "Table"
  LIST = "ListItem"
  HEADER = "Header"
  FOOTER = "Footer"
  IMAGE = "Image"