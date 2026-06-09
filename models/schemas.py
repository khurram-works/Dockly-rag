# models/schemas.py

from pydantic import BaseModel
from typing import List, Optional

# BaseModel is Pydantic's base class
# When you inherit from it, your class gets automatic validation for free
# If a required field is missing or wrong type, FastAPI rejects the request
# before your code even runs — exactly like Zod on the frontend

# ─────────────────────────────────────────────
# REQUEST MODELS
# These define what Node.js sends TO Python
# ─────────────────────────────────────────────

class ProcessDocumentRequest(BaseModel):
    # This is what Node.js sends when a document needs processing
    documentId: str    # The PostgreSQL document ID
    companyId: str     # Which company owns this document
    fileUrl: str       # The Supabase URL to download the PDF from
    filename: str      # The original filename e.g. "ReturnPolicy.pdf"

class QueryRequest(BaseModel):
    # This is what Node.js sends when a customer asks a question
    question: str      # The customer's actual question
    companyId: str     # Which company's documents to search in
    conversationHistory: Optional[List[dict]] = []
    # conversationHistory = previous messages in this conversation
    # Optional means it can be missing — defaults to empty list
    # List[dict] means a list of dictionaries

# ─────────────────────────────────────────────
# RESPONSE MODELS
# These define what Python sends BACK to Node.js
# ─────────────────────────────────────────────

class ProcessDocumentResponse(BaseModel):
    # Sent back after a document is successfully processed
    success: bool          # True or False
    chunksCreated: int     # How many chunks were stored in Qdrant
    pageCount: int         # How many pages the PDF had
    message: str           # Human readable message

class QueryResponse(BaseModel):
    # Sent back after answering a customer question
    answer: str                # The AI generated answer
    sources: List[str]         # Which filenames were used as sources
    success: bool