from domain.models.document_element import DocumentElement
from domain.enums.parser_type import ParserType
from domain.models.document_strategy import DocumentStrategy
from domain.enums.element_type import ElementType
from domain.models.document_metadata import DocumentMetadata
from domain.models.coordinates import Coordinates
from domain.enums.parser_strategy import ParsingStrategy
from domain.models.parsed_document import ParsedDocument


from pathlib import Path
from core.exceptions import PartitioningError
import logging

from unstructured.partition.pdf import partition_pdf
from unstructured.partition.auto import partition
from unstructured.partition.image import partition_image

from unstructured.documents.elements import (
  Title,
  NarrativeText,
  ListItem,
  Table,
  Header,
  Footer,
  Image,
  FigureCaption,
  UncategorizedText,
)

logger = logging.getLogger(__name__)


ELEMENT_TYPE_MAPPING = {
  Title: ElementType.TITLE,
  NarrativeText: ElementType.NARRATIVE,
  ListItem: ElementType.LIST,
  Table: ElementType.TABLE,
  Header: ElementType.HEADER,
  Footer: ElementType.FOOTER,
  Image: ElementType.IMAGE,
  FigureCaption: ElementType.NARRATIVE,
  UncategorizedText: ElementType.NARRATIVE,
}


class UnstructuredProvider:

  def __init__(self):

    self._handlers = {
      ParserType.PDF: self._partition_pdf,
      ParserType.GENERIC: self._partition_generic,
      ParserType.IMAGE: self._partition_image,
    }

  def partition(self,file_path: Path, strategy: DocumentStrategy) -> ParsedDocument:

    handler = self._handlers.get(strategy.parser)
  
    if handler is None:
        raise PartitioningError(
            f"No partition handler for parser: {strategy.parser}"
        )
    
    return handler(file_path=file_path, strategy=strategy)

  

  def _partition_with(
      self,
      partitioner,
      file_path: Path,
      strategy: ParsingStrategy,
      **kwargs,
    ) -> ParsedDocument:

    try:

      elements = partitioner(
        filename=str(file_path),
        strategy = strategy.value,
        **kwargs,
      )

      page_count = self._get_page_count(elements)

      document_elements = [
          self._to_document_element(element)
          for element in elements
        ]

      return ParsedDocument(
        page_count=page_count,
        elements=document_elements
      )

    except Exception as e:
        logger.exception(
          "Failed partitioning '%s' using parser '%s'",
          file_path,
          strategy,
        )

        raise PartitioningError(
          f"Failed to partition document '{file_path.name}'."
        ) from e





  def _partition_pdf(
      self,
      file_path: Path,
      strategy: DocumentStrategy,
    ) -> ParsedDocument:

    return self._partition_with(
      partitioner=partition_pdf,
      file_path=file_path,
      strategy=strategy.parsing_strategy,
    )

  

  def _partition_generic(self, file_path: Path, strategy: DocumentStrategy) -> ParsedDocument:

    return self._partition_with(
      partitioner=partition,
      file_path=file_path,
      strategy=strategy.parsing_strategy,
    )

  def _partition_image(
      self,
      file_path: Path,
      strategy: DocumentStrategy,
    ) -> ParsedDocument:

    return self._partition_with(
      partitioner=partition_image,
      file_path=file_path,
      strategy=strategy.parsing_strategy,
    )


  def _to_document_element(self, element) -> DocumentElement:
    
    return DocumentElement(
      text=getattr(element, "text", "") or "",
      element_type = self._to_element_type(element),
      metadata = self._to_document_metadata(element)
    )


  def _to_document_metadata(self, element) -> DocumentMetadata:
    metadata = getattr(element, "metadata", None)

    if metadata is None:
      return DocumentMetadata(
        page_number=None,
        languages=[],
        coordinates=None,
        section_title=None,
        parent_section=None
      )
    
    coordinates = self._to_coordinates(
      getattr(metadata, "coordinates", None)
    )

    languages = getattr(metadata, "languages", []) or []

    return DocumentMetadata(
      page_number=getattr(metadata, "page_number", None),
      languages=languages,
      section_title = None,
      parent_section= None,
      coordinates=coordinates
    )


  def _to_element_type(self, element) -> ElementType:
    for cls, element_type in ELEMENT_TYPE_MAPPING.items():
      if isinstance(element, cls):
          return element_type

    return ElementType.NARRATIVE


  def _get_page_count(self, elements) -> int:

    page_numbers = [
      page_number
      for element in elements
      if (page_number := getattr(getattr(element, "metadata", None), "page_number", None))
      is not None
    ]

    if not page_numbers:
        return 0

    return max(page_numbers)



  def _to_coordinates(self, coordinates) -> Coordinates | None:

    if not coordinates or not getattr(coordinates, "points", None):
      return None

    return Coordinates(
      points= coordinates.points
    )

