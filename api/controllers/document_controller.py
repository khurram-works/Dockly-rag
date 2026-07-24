from api.schemas.document_processing import (
    ProcessDocumentRequest,
    ProcessDocumentResponse,
)

from api.services.document_processing_service import (
    DocumentProcessingService,
)


class DocumentController:

    def __init__(
        self,
        processing_service: DocumentProcessingService,
    ) -> None:

        self._processing_service = (
            processing_service
        )

    def process_document(
        self,
        request: ProcessDocumentRequest,
    ) -> ProcessDocumentResponse:

        chunks_created = (
            self._processing_service.process(
                request
            )
        )

        return ProcessDocumentResponse(
            success=True,
            documentId=request.documentId,
            chunksCreated=chunks_created,
            pageCount=None,
            message=(
                "Document processed successfully."
            ),
        )