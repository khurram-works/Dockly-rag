from fastapi import APIRouter, Depends
import logging

from api.controllers.document_controller import (
    DocumentController,
)

from api.dependencies.document_dependencies import (
    get_document_controller,
)

from api.schemas.document_processing import (
    ProcessDocumentRequest,
    ProcessDocumentResponse,
)

from infrastructure.qdrant.qdrant_vector_store import QdrantVectorStore
from fastapi import APIRouter, Depends, HTTPException
from api.schemas.query import QueryRequest, QueryResponse
from processing.retrieval.retriever import VectorRetriever
from processing.retrieval.query_rewriter import QueryRewriter
from processing.retrieval.reranker import Reranker
from processing.generation.answer_generator import AnswerGenerator
from processing.generation.citation_builder import CitationBuilder
from api.dependencies.document_dependencies import (
    get_vector_store,
    get_embedding_provider,
    get_qdrant_client,
)
from core.config.settings import settings

router = APIRouter(
    prefix="/api",
    tags=["documents"],
)


@router.post(
    "/process-document",
    response_model=ProcessDocumentResponse,
)
def process_document(
    request: ProcessDocumentRequest,
    controller: DocumentController = Depends(
        get_document_controller
    ),
) -> ProcessDocumentResponse:

    return controller.process_document(
        request
    )


@router.post("/query", response_model=QueryResponse)
def query_documents(
    request: QueryRequest,
    vector_store = Depends(get_vector_store),
    embedding_provider = Depends(get_embedding_provider),
    qdrant_client = Depends(get_qdrant_client),
) -> QueryResponse:
    """Query documents and generate an answer."""
    
    try:
        
        retriever = VectorRetriever(
            embedding_provider=embedding_provider,
            qdrant_client=qdrant_client,
            collection_name=settings.qdrant_collection_name,
        )

        query_rewriter = QueryRewriter()
        reranker = Reranker()
        answer_generator = AnswerGenerator()
        citation_builder = CitationBuilder()

        rewritten_query = query_rewriter.rewrite(
            query=request.question,
            conversation_history=request.conversationHistory,
        )

        retrieved_results = retriever.retrieve(
            query=rewritten_query,
            company_id=request.companyId,
            limit=5,
        )
        
        if not retrieved_results:
            return QueryResponse(
                answer="I don't have enough information to answer this question.",
                sources=None,
                foundAnswer=False,
                success=True,
            )

        reranked_results = reranker.rerank(
            query=rewritten_query,
            results=retrieved_results,
            top_k=3,
        )
        
        context_chunks = []
        for result in reranked_results:
            payload = result.get("payload", {})
            
            pages = payload.get("page_numbers", "Unknown Page")
            if isinstance(pages, list):
                pages = ", ".join(map(str, pages))
        
            context_chunks.append({
                "text": payload.get("text", ""),
                "source": payload.get("filename", "Unknown Document"),  # <-- Fixed key
                "page": pages                                           # <-- Fixed key
            })
        

        answer = answer_generator.generate(
            question=request.question,
            context_chunks=context_chunks,
            conversation_history=request.conversationHistory,
        )
        
        raw_sources = citation_builder.build_citations(reranked_results)
        sources = []
        if raw_sources:
            for source in raw_sources:
                filename = source.get("filename", "")
                if filename and filename in answer:
                    sources.append(source)
        
        return QueryResponse(
            answer=answer,
            sources=sources if sources else raw_sources,
            foundAnswer=True,
            success=True,
        )
        
    except Exception as e:
        logging.error("An unexpected error occurred", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Query failed: {str(e)}"
        )


@router.delete("/delete-document/{document_id}")
def delete_document(
    document_id: str,
    vector_store: QdrantVectorStore = Depends(get_vector_store),
):
    try:
        vector_store.delete_points_by_document_id(document_id=document_id)
        return {"success": True, "documentId": document_id}
    except Exception as e:
        logging.error(f"Failed to delete document {document_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete document {document_id}: {str(e)}"
        )



    
