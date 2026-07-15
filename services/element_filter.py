import re
from typing import Set


SKIP_ELEMENT_TYPES: Set[str] = {
    "Header",
    "Footer", 
    "PageBreak",
    "Bibliography",
    "Footnote",
    "Endnote"
}

MIN_TEXT_LENGTH = 10

def is_empty(element: dict) -> bool:
  return not element["text"].strip()

def is_too_short(element: dict) -> bool:
  return len(element["text"]) < MIN_TEXT_LENGTH

def is_separator(element: dict) -> bool:
  return bool(
    re.fullmatch(
      r"[-=*]{3,}",
      element["text"]
    )
  )

def is_page_number(element: dict) -> bool:
  text = element["text"]
  return (
    re.fullmatch(r"\d+", text)
    or
    re.fullmatch(r"Page\s+\d+", text, re.IGNORECASE)
  )

def is_skipped_element_type(element: dict) -> bool:
  return (
    element["elementType"]
    in
    SKIP_ELEMENT_TYPES
  )

def filter_elements(elements: list[dict])-> list[dict]:
  filtered = []
  for element in elements:
    if is_empty(element):
      continue
    if is_too_short(element):
      continue
    if is_separator(element):
      continue
    if is_page_number(element):
      continue
    if is_skipped_element_type(element):
      continue
    filtered.append(element)

  return filtered
  

