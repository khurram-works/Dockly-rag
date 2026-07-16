from enum import Enum


class ElementType(str, Enum):
  TITLE = "Title"
  NARRATIVE = "NarrativeText"
  TABLE = "Table"
  LIST = "ListItem"
  HEADER = "Header"
  FOOTER = "Footer"
  IMAGE = "Image"