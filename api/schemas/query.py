

from typing import Any

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    question: str
    companyId: str
    conversationHistory: list[dict[str, Any]] = Field(
        default_factory=list
    )

class SourceReference(BaseModel):
    documentId: str
    filename: str
    pageNumbers: list[int]
    chunkIndex: int


class QueryResponse(BaseModel):
    answer: str
    sources: List[SourceReference] | None = None
    foundAnswer: bool
    success: bool