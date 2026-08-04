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
    documentId: str | None = None
    filename: str | None = None
    pageNumbers: list[int] = []
    chunkIndex: int | None = None

class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceReference] | None = None
    foundAnswer: bool
    success: bool