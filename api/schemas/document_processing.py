# api/schemas/document_processing.py
from pydantic import BaseModel, ConfigDict, Field

class ProcessDocumentRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    document_id: str = Field(alias="documentId")
    company_id: str = Field(alias="companyId")
    file_url: str = Field(alias="fileUrl")
    filename: str
    file_size: int = Field(default=0, alias="fileSize")  # NEW FIELD
    mime_type: str | None = Field(default=None, alias="mimeType")  # NEW FIELD



class ProcessDocumentResponse(BaseModel):

    success: bool

    documentId: str

    chunksCreated: int

    pageCount: int | None

    message: str