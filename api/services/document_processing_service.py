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


class DocumentProcessingService:

    def __init__(
        self,
        temporary_document: TemporaryDocument,
        orchestrator: DocumentProcessingOrchestrator,
    ) -> None:

        self._temporary_document = (
            temporary_document
        )

        self._orchestrator = orchestrator

    def process(
        self,
        request: ProcessDocumentRequest,
    ) -> int:

        extension = Path(
            request.filename
        ).suffix.lower()

        profile = DocumentProfile(
            document_id=request.documentId,
            company_id=request.companyId,
            filename=request.filename,
            extension=extension,
            mime_type=None,
            file_size=0,
        )

        with self._temporary_document.open(
            file_url=request.fileUrl,
            filename=request.filename,
        ) as file_path:

            chunks_created = (
                self._orchestrator.process(
                    file_path=file_path,
                    profile=profile,
                )
            )

        return chunks_created