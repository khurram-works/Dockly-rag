# api/schemas/query.py
from typing import Any  # Remove List import
from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    question: str
    companyId: str = Field(alias="companyId")
    conversationHistory: list[dict[str, Any]] = Field(  # Use lowercase list
        default_factory=list,
        alias="conversationHistory"
    )

class SourceReference(BaseModel):
    documentId: str = Field(alias="documentId")
    filename: str
    pageNumbers: list[int] = Field(alias="pageNumbers")  # Use lowercase list
    chunkIndex: int = Field(alias="chunkIndex")

class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceReference] | None = None  # Use lowercase list
    foundAnswer: bool
    success: bool