from abc import ABC, abstractmethod

from domain.models.parsed_document import ParsedDocument

class BaseFilter(ABC):
  
  @abstractmethod
  def apply(self, document: ParsedDocument) -> ParsedDocument:
    pass