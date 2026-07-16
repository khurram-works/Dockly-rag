from domain.models.document_element import DocumentElement
from domain.enums.parser_type import ParserType
from domain.models.document_strategy import DocumentStrategy

from pathlib import Path
from core.exceptions import PartitioningError

from unstructured.partition.pdf import partition_pdf
from unstructured.partition.auto import partition


class UnstructuredProvider:
  def partition(self,file_path: Path,strategy: DocumentStrategy) -> tuple[list[DocumentElement], int]:

    handlers = {
      ParserType.PDF: self._partition_pdf,
      ParserType.GENERIC: self._partition_generic,
      ParserType.IMAGE: self._partition_image,
    }

    handler = handlers.get(strategy.parser)
  
    if handler is None:
        raise PartitioningError(
            f"No partition handler for parser: {strategy.parser}"
        )
    
    return handler(file_path=file_path, strategy=strategy)









  def _partition_pdf():
    pass

  def _partition_generic():
    pass

  def _partition_image():
    pass