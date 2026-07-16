from dataclasses import dataclass


@dataclass(slots=True)
class DocumentProfile:
  document_id:str
  company_id:str

  filename:str
  extension:str
  mime_type:str | None

  file_size:int
