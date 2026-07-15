from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=true)
class DocumentProfile:
  document_id:str
  company_id:str

  filename:str
  extension:str
  mime_type:str | None

  file_size:int
  file_url:str

  uploaded_at:datetime

  @property
  def is_pdf(self)->bool:
    return self.extension == ".pdf"
