from pydantic import BaseModel
from typing import List, Optional

class ProcessDocumentRequest(BaseModel):
    documentId: str    
    companyId: str     
    fileUrl: str       
    filename: str      

class QueryRequest(BaseModel):
    question: str     
    companyId: str     
    conversationHistory: Optional[List[dict]] = []


class ProcessDocumentResponse(BaseModel):
    success: bool         
    chunksCreated: int     
    pageCount: int         
    message: str           


class SourceReference(BaseModel):
    documentId: str
    filename: str
    pageNumber: int

class QueryResponse(BaseModel):
    answer: str                
    sources: List[SourceReference] 
    success: bool