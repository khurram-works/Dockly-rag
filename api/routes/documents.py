from fastapi import APIRouter, Depends

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
import logging

from fastapi import APIRouter, Depends, HTTPException
from api.schemas.query import QueryRequest, QueryResponse
from processing.retrieval.retriever import VectorRetriever
from processing.retrieval.query_rewriter import QueryRewriter
from processing.retrieval.reranker import Reranker
from processing.generation.answer_generator import AnswerGenerator
from processing.generation.citation_builder import CitationBuilder
from api.dependencies.document_dependencies import (
    get_vector_store,
    get_embedding_service,
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
    embedding_service = Depends(get_embedding_service),
    qdrant_client = Depends(get_qdrant_client),
) -> QueryResponse:
    """Query documents and generate an answer."""
    
    try:
        
        retriever = VectorRetriever(
            # vector_store=vector_store,
            embedding_provider=embedding_service._provider,
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
        

        context_chunks = [
            result["payload"]["text"]
            for result in reranked_results
        ]
        

        answer = answer_generator.generate(
            question=request.question,
            context_chunks=context_chunks,
            conversation_history=request.conversationHistory,
        )
        
        sources = citation_builder.build_citations(reranked_results)
        
        return QueryResponse(
            answer=answer,
            sources=sources,
            foundAnswer=True,
            success=True,
        )
        
    except Exception as e:
        logging.error("An unexpected error occurred", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Query failed: {str(e)}"
        )



    
