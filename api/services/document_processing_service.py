from pathlib import Path

from api.schemas.document_processing import (
    ProcessDocumentRequest,
)

from domain.models.document_profile import (
    DocumentProfile,
)

from infrastructure.download.temporary_document import (
    TemporaryDocument,
)

from processing.orchestration.document_processing_orchestrator import (
    DocumentProcessingOrchestrator,
)

from processing.inspection.document_inspector import DocumentInspector




class DocumentProcessingService:
    def __init__(
        self,
        temporary_document: TemporaryDocument,
        orchestrator: DocumentProcessingOrchestrator,
        inspector: DocumentInspector,
    ) -> None:
        self._temporary_document = temporary_document
        self._orchestrator = orchestrator
        self._inspector = inspector

    def process(
        self,
        request: ProcessDocumentRequest,
    ) -> tuple[int, int | None]:
        profile = self._inspector.inspect(
            document_id=request.document_id,
            company_id=request.company_id,
            filename=request.filename,
            file_size=request.file_size,
            mime_type=request.mime_type,
        )

        with self._temporary_document.open(
            file_url=request.file_url,
            filename=request.filename,
        ) as (file_path, download_file_size):
            chunks_created, page_count= self._orchestrator.process(
                file_path=file_path,
                profile=profile,
            )

        return chunks_created, page_count