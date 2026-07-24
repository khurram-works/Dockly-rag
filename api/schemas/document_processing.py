from pydantic import BaseModel, ConfigDict, Field


class ProcessDocumentRequest(BaseModel):

    model_config = ConfigDict(
        populate_by_name=True
    )

    document_id: str = Field(
        alias="documentId"
    )

    company_id: str = Field(
        alias="companyId"
    )

    file_url: str = Field(
        alias="fileUrl"
    )

    filename: str


from pydantic import BaseModel


class ProcessDocumentResponse(BaseModel):

    success: bool

    documentId: str

    chunksCreated: int

    pageCount: int | None

    message: str