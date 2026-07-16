from pathlib import Path
import mimetypes
from domain.models.document_profile import DocumentProfile

class DocumentInspector:

  def _extract_extension(self, filename: str) -> str:
    return Path(filename).suffix.lower()

  def _determine_mime_type(self, filename: str, mime_type: str | None = None) -> str | None:
    if mime_type is None:
      mime_type, _ = mimetypes.guess_type(filename)
    return mime_type

  def inspect(
        self,document_id: str,
        company_id: str,
        filename: str,
        file_size: int,
        mime_type: str | None=None,
    ) -> DocumentProfile:

    extension = self._extract_extension(filename)
    mime_type = self._determine_mime_type(filename, mime_type)

    return DocumentProfile(
      document_id=document_id,
      company_id=company_id,
      filename=filename,
      extension=extension,
      mime_type=mime_type,
      file_size=file_size,
    )


  
  
