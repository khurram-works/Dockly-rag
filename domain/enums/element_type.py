from enum import Enum


class ElementType(str, Enum):
    TITLE = "Title"
    NARRATIVE = "NarrativeText"
    LIST = "ListItem"
    TABLE = "Table"
    HEADER = "Header"
    FOOTER = "Footer"
    IMAGE = "Image"
    FIGURE_CAPTION = "FigureCaption"
    ADDRESS = "Address"
    PAGE_BREAK = "PageBreak"
    FORMULA = "Formula"
    UNCATEGORIZED = "UncategorizedText"