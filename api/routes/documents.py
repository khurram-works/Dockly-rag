# from fastapi import HTTPException, APIRouter
# from api.schemas.document_processing import ProcessDocumentResponse
# from api.schemas.document_processing import ProcessDocumentRequest
# from api.services.document_processing_service import DocumentProcessingService


# router = APIRouter()

# @router.post(
#     "/process-document",
#     response_model=ProcessDocumentResponse,
# )
# def process_document(
#     request: ProcessDocumentRequest,
#     service: DocumentProcessingService = Depends(
#         get_document_processing_service
#     ),
# ):

#     chunks_created = service.process(
#         request
#     )

#     return ProcessDocumentResponse(
#         success=True,
#         documentId=request.documentId,
#         chunksCreated=chunks_created,
#         pageCount=None,
#         message="Document processed successfully.",
#     )

# @router.delete("/delete-document/{document_id}")
# async def delete_document_vectors(document_id: str):
#     try:
#         delete_document_chunks(document_id)
#         return {
#             "success": True,
#             "message": f"Vectors deleted for document {document_id}"
#         }
#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail=f"Failed to delete vectors: {str(e)}"
#         )

# @router.post("/query", response_model=QueryResponse)
# async def query_documents(request: QueryRequest):

#     try:
#         print(f"Processing query: {request.question}")
#         query_embedding = generate_embedding(request.question)

#         relevant_chunks = search_similar_chunks(
#             query_embedding=query_embedding,
#             company_id=request.companyId,
#             limit=5
#         )

#         answer, sources, foundAnswer = generate_answer(
#             question=request.question,
#             relevant_chunks=relevant_chunks,
#             conversation_history=request.conversationHistory
#         )

#         return QueryResponse(
#             answer=answer,
#             sources=sources,
#             foundAnswer = foundAnswer,
#             success=True
#         )

#     except Exception as e:
#         print(f"Error processing query: {str(e)}")
#         raise HTTPException(
#             status_code=500,
#             detail=f"Failed to process query: {str(e)}"
#         )




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



    
