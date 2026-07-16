from enum import Enum

class ParsingStrategy(str, Enum):
  FAST = "fast"
  HI_RES = "hi_res"
  OCR_ONLY = "ocr_only"