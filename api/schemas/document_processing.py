from pydantic import BaseModel, ConfigDict, Field, field_validator
from core.constants import MAX_FILE_SIZE_BYTES, SUPPORTED_FILE_EXTENSIONS
from pathlib import Path

class ProcessDocumentRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    document_id: str = Field(alias="documentId")
    company_id: str = Field(alias="companyId")
    file_url: str = Field(alias="fileUrl")
    filename: str
    file_size: int = Field(default=0, alias="fileSize")
    mime_type: str | None = Field(default=None, alias="mimeType")

    @field_validator('filename')
    @classmethod
    def validate_file_extension(cls, v: str) -> str:
        extension = Path(v).suffix.lower()
        if extension not in SUPPORTED_FILE_EXTENSIONS:
            raise ValueError(
                f"Unsupported file extension: {extension}. "
                f"Supported: {', '.join(SUPPORTED_FILE_EXTENSIONS)}"
            )
        return v

    @field_validator('file_size')
    @classmethod
    def validate_file_size(cls, v: int) -> int:
        if v > MAX_FILE_SIZE_BYTES:
            raise ValueError(
                f"File size exceeds maximum of {MAX_FILE_SIZE_BYTES / (1024*1024)}MB"
            )
        return v


class ProcessDocumentResponse(BaseModel):
    documentId: str
    success: bool         
    chunksCreated: int     
    pageCount: int | None = None       
    message: str 