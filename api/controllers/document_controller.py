from api.schemas.document_processing import (
    ProcessDocumentRequest,
    ProcessDocumentResponse,
)

from api.services.document_processing_service import (
    DocumentProcessingService,
)


from core.exceptions import (
    RAGPipelineError,
    UnsupportedDocumentError,  
    DocumentDownloadError,
    PartitioningError,
    EmbeddingError,
    StorageError
)
from fastapi import HTTPException, status
import logging

class DocumentController:
    def __init__(
        self,
        processing_service: DocumentProcessingService,
    ) -> None:
        self._processing_service = processing_service

    def process_document(
        self,
        request: ProcessDocumentRequest,
    ) -> ProcessDocumentResponse:
        try:
            chunks_created, page_count = self._processing_service.process(request)
            
            return ProcessDocumentResponse(
                success=True,
                documentId=request.document_id,
                chunksCreated=chunks_created,
                pageCount=page_count,
                message="Document processed successfully.",
            )
            
        except UnsupportedDocumentError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported document type: {str(e)}"
            )
        except DocumentDownloadError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to download document: {str(e)}"
            )
        except PartitioningError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Failed to parse document: {str(e)}"
            )
        except EmbeddingError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to generate embeddings: {str(e)}"
            )
        except StorageError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to store in vector database: {str(e)}"
            )
        except RAGPipelineError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Processing failed: {str(e)}"
            )
        except Exception as e:
            logging.error("An unexpected error occurred", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error: {str(e)}"
            )