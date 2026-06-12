from fastapi import HTTPException, APIRouter
from models.schemas import (
    ProcessDocumentRequest,
    ProcessDocumentResponse,
    QueryRequest,
    QueryResponse
)
from services.pdf import download_and_extract_text, split_text_into_chunks
from services.embeddings import generate_embeddings_batch, generate_embedding
from services.qdrant import ensure_collection_exists, store_chunks, search_similar_chunks, delete_document_chunks
from services.chat import generate_answer


router = APIRouter()

@router.post("/process-document", response_model=ProcessDocumentResponse)
async def process_document(request: ProcessDocumentRequest):
    try:
        ensure_collection_exists()
        print(f"Downloading PDF: {request.filename}")
        pages, page_count = download_and_extract_text(request.fileUrl)
        if not pages:
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from PDF. The file may be a scanned image."
            )
        print(f"Splitting text into chunks...")
        chunks = split_text_into_chunks(pages)
        print(f"Created {len(chunks)} chunks")

        if len(chunks) == 0:
            raise HTTPException(
                status_code=400,
                detail="No content could be extracted from this document"
            )

        print(f"Generating embeddings for {len(chunks)} chunks...")
        chunk_texts = [chunk["text"] for chunk in chunks]
        embeddings = generate_embeddings_batch(chunk_texts)

        print(f"Storing chunks in Qdrant...")
        chunks_stored = store_chunks(
            chunks=chunks,
            embeddings=embeddings,
            company_id=request.companyId,
            document_id=request.documentId,
            filename=request.filename
        )

        print(f"Successfully processed {request.filename}: {chunks_stored} chunks stored")
        return ProcessDocumentResponse(
            success=True,
            chunksCreated=chunks_stored,
            pageCount=page_count,
            message=f"Successfully processed {request.filename}"
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error processing document: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process document: {str(e)}"
        )

@router.delete("/delete-document/{document_id}")
async def delete_document_vectors(document_id: str):
    try:
        delete_document_chunks(document_id)
        return {
            "success": True,
            "message": f"Vectors deleted for document {document_id}"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete vectors: {str(e)}"
        )

@router.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):

    try:
        print(f"Processing query: {request.question}")
        query_embedding = generate_embedding(request.question)

        relevant_chunks = search_similar_chunks(
            query_embedding=query_embedding,
            company_id=request.companyId,
            limit=5
        )

        if len(relevant_chunks) == 0:
            return QueryResponse(
                answer="I don't have any documents in my knowledge base yet. Please ask the company to upload their documents.",
                sources=[],
                success=True
            )

        answer, sources = generate_answer(
            question=request.question,
            relevant_chunks=relevant_chunks,
            conversation_history=request.conversationHistory
        )

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




    
