from pathlib import Path
import logging

from unstructured.partition.auto import partition
from unstructured.partition.image import partition_image
from unstructured.partition.pdf import partition_pdf

from core.exceptions import PartitioningError

from domain.enums.element_type import ElementType
from domain.enums.parser_strategy import ParsingStrategy
from domain.enums.parser_type import ParserType

from domain.models.coordinates import Coordinates
from domain.models.document_element import DocumentElement
from domain.models.document_metadata import DocumentMetadata
from domain.models.document_profile import DocumentProfile
from domain.models.document_strategy import DocumentStrategy
from domain.models.parsed_document import ParsedDocument

logger = logging.getLogger(__name__)


ELEMENT_TYPE_MAPPING = {
    "Title": ElementType.TITLE,
    "NarrativeText": ElementType.NARRATIVE,
    "ListItem": ElementType.LIST,
    "Table": ElementType.TABLE,
    "Header": ElementType.HEADER,
    "Footer": ElementType.FOOTER,
    "Image": ElementType.IMAGE,
    "FigureCaption": ElementType.FIGURE_CAPTION,
    "Address": ElementType.ADDRESS,
    "PageBreak": ElementType.PAGE_BREAK,
    "Formula": ElementType.FORMULA,
    "UncategorizedText": ElementType.UNCATEGORIZED,
}


class UnstructuredProvider:

  def __init__(self):

    self._handlers = {
      ParserType.PDF: self._partition_pdf,
      ParserType.GENERIC: self._partition_generic,
      ParserType.IMAGE: self._partition_image,
    }

  def partition(self,file_path: Path, profile: DocumentProfile, strategy: DocumentStrategy) -> ParsedDocument:

    if not file_path.exists():
      raise PartitioningError(
            f"No partition Filepath provided for parser: {file_path}"
        )


    handler = self._handlers.get(strategy.parser)
  
    if handler is None:
        raise PartitioningError(
            f"No partition handler for parser: {strategy.parser}"
        )
    
    return handler(file_path=file_path, strategy=strategy, profile=profile)

  

  def _partition_with(
    self,
    partitioner,
    profile: DocumentProfile,
    file_path: Path,
    strategy: ParsingStrategy,
    **kwargs,
) -> ParsedDocument:

    try:

        elements = partitioner(
            filename=str(file_path),
            strategy=strategy.value,
            **kwargs,
        )

        page_count = self._get_page_count(
            elements
        )

        document_elements = [
            self._to_document_element(element)
            for element in elements
        ]

        return ParsedDocument(
            document_id=profile.document_id,
            company_id=profile.company_id,
            filename=profile.filename,
            page_count=page_count,
            elements=document_elements,
        )

    except Exception as e:

        logger.exception(
            "Partition failed "
            "document=%s "
            "company=%s "
            "file=%s "
            "strategy=%s",
            profile.document_id,
            profile.company_id,
            file_path,
            strategy,
        )

        raise PartitioningError(
            f"Failed to partition '{file_path.name}': {e}"
        ) from e




  def _partition_pdf(
      self,
      file_path: Path,
      profile:DocumentProfile,
      strategy: DocumentStrategy,
    ) -> ParsedDocument:

    return self._partition_with(
      partitioner=partition_pdf,
      file_path=file_path,
      strategy=strategy.parsing_strategy,
      profile=profile
    )

  

  def _partition_generic(self, file_path: Path, profile: DocumentProfile, strategy: DocumentStrategy) -> ParsedDocument:

    return self._partition_with(
      partitioner=partition,
      file_path=file_path,
      strategy=strategy.parsing_strategy,
      profile=profile
    )

  def _partition_image(
      self,
      file_path: Path,
      profile:DocumentProfile,
      strategy: DocumentStrategy,
    ) -> ParsedDocument:

    return self._partition_with(
      partitioner=partition_image,
      file_path=file_path,
      strategy=strategy.parsing_strategy,
      profile=profile
    )


  def _to_document_element(
    self,
    element,
) -> DocumentElement:

    return DocumentElement(
        element_id=getattr(
            element,
            "element_id",
            None,
        ),
        text=getattr(
            element,
            "text",
            "",
        ) or "",
        element_type=self._to_element_type(element),
        metadata=self._to_document_metadata(element),
        source_element=element,
    )


  def _to_document_metadata(
    self,
    element,
) -> DocumentMetadata:

    metadata = getattr(
        element,
        "metadata",
        None,
    )

    if metadata is None:

        return DocumentMetadata(
            page_number=None,
            languages=[],
            coordinates=None,
            section_title=None,
            parent_section=None,
            text_as_html=None,
        )

    return DocumentMetadata(
        page_number=getattr(
            metadata,
            "page_number",
            None,
        ),
        languages=getattr(
            metadata,
            "languages",
            [],
        ) or [],
        coordinates=self._to_coordinates(
            getattr(
                metadata,
                "coordinates",
                None,
            )
        ),
        section_title=None,
        parent_section=None,
        text_as_html=getattr(
            metadata,
            "text_as_html",
            None,
        ),
    )


  def _to_element_type(self, element) -> ElementType:

    category = getattr(
        element,
        "category",
        None,
    )

    return ELEMENT_TYPE_MAPPING.get(
        category,
        ElementType.NARRATIVE,
    )


  def _get_page_count(self, elements) -> int | None:

    page_numbers = [
        page_number
        for element in elements
        if (
            page_number := getattr(
                getattr(element, "metadata", None),
                "page_number",
                None,
            )
        ) is not None
    ]

    return max(page_numbers, default=None)



  def _to_coordinates(self, coordinates) -> Coordinates | None:

    if not coordinates or not getattr(coordinates, "points", None):
      return None

    return Coordinates(
      points= coordinates.points
    )

