from fastapi import APIRouter, HTTPException
from models.schemas import (
    ProcessDocumentRequest,
    ProcessDocumentResponse,
    QueryRequest,
    QueryResponse
)
from services.pdf import download_and_extract_text, split_text_into_chunks
from services.embeddings import generate_embeddings_batch, generate_embedding
from services.qdrant import ensure_collection_exists, store_chunks, search_similar_chunks
from services.chat import generate_answer

# APIRouter is like Express Router
# You define routes on it, then register it in main.py
router = APIRouter()


# ─────────────────────────────────────────────
# POST /process-document
# Called by Node.js after a PDF is uploaded
# ─────────────────────────────────────────────
@router.post("/process-document", response_model=ProcessDocumentResponse)
async def process_document(request: ProcessDocumentRequest):
    # @router.post = this function handles POST requests
    # response_model = FastAPI validates our response matches this shape
    # async def = this is an async function (like async function in JS)
    # request: ProcessDocumentRequest = FastAPI automatically parses
    # the request body and validates it matches our Pydantic model

    try:
        # Step 1: Make sure our Qdrant collection exists
        ensure_collection_exists()

        # Step 2: Download the PDF and extract text
        print(f"Downloading PDF: {request.filename}")
        full_text, page_count = download_and_extract_text(request.fileUrl)
        # full_text = all text from the PDF as one big string
        # page_count = number of pages

        if not full_text.strip():
            # strip() removes whitespace
            # If after stripping there's nothing, the PDF had no text
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from PDF. The file may be a scanned image."
            )
            # HTTPException is like res.status(400).json({error: "..."}) in Express

        # Step 3: Split text into chunks
        print(f"Splitting text into chunks...")
        chunks = split_text_into_chunks(full_text)
        print(f"Created {len(chunks)} chunks")

        if len(chunks) == 0:
            raise HTTPException(
                status_code=400,
                detail="No content could be extracted from this document"
            )

        # Step 4: Generate embeddings for all chunks at once
        print(f"Generating embeddings for {len(chunks)} chunks...")
        embeddings = generate_embeddings_batch(chunks)
        # embeddings is now a list of 384-number lists
        # One embedding per chunk

        # Step 5: Store everything in Qdrant
        print(f"Storing chunks in Qdrant...")
        chunks_stored = store_chunks(
            chunks=chunks,
            embeddings=embeddings,
            company_id=request.companyId,
            document_id=request.documentId,
            filename=request.filename
        )

        print(f"Successfully processed {request.filename}: {chunks_stored} chunks stored")

        # Step 6: Return success response to Node.js
        return ProcessDocumentResponse(
            success=True,
            chunksCreated=chunks_stored,
            pageCount=page_count,
            message=f"Successfully processed {request.filename}"
        )

    except HTTPException:
        raise
        # Re-raise HTTP exceptions as-is
        # We don't want to wrap them in another exception

    except Exception as e:
        # Catch any unexpected error
        print(f"Error processing document: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process document: {str(e)}"
        )


# ─────────────────────────────────────────────
# POST /query
# Called by Node.js when a customer asks a question
# ─────────────────────────────────────────────
@router.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):

    try:
        # Step 1: Convert the question to a vector
        print(f"Processing query: {request.question}")
        query_embedding = generate_embedding(request.question)
        # Single embedding for the question
        # Same model, same 384 numbers

        # Step 2: Search Qdrant for relevant chunks
        relevant_chunks = search_similar_chunks(
            query_embedding=query_embedding,
            company_id=request.companyId,
            limit=5
            # Get top 5 most relevant chunks
        )

        if len(relevant_chunks) == 0:
            # No relevant chunks found — no documents uploaded yet
            return QueryResponse(
                answer="I don't have any documents in my knowledge base yet. Please ask the company to upload their documents.",
                sources=[],
                success=True
            )

        # Step 3: Generate answer using Groq
        answer, sources = generate_answer(
            question=request.question,
            relevant_chunks=relevant_chunks,
            conversation_history=request.conversationHistory
        )

        # Step 4: Return answer to Node.js
        return QueryResponse(
            answer=answer,
            sources=sources,
            success=True
        )

    except Exception as e:
        print(f"Error processing query: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process query: {str(e)}"
        )