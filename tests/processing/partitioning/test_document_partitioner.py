from pathlib import Path
from unittest.mock import Mock

from domain.models.document_profile import DocumentProfile
from domain.models.document_strategy import DocumentStrategy
from domain.models.parsed_document import ParsedDocument

from processing.partitioning.document_partitioner import (
    DocumentPartitioner,
)


def test_document_partitioner_delegates_to_provider():

    provider = Mock()

    expected_document = ParsedDocument(
        document_id="doc-123",
        company_id="company-456",
        filename="company.pdf",
        page_count=1,
        elements=[],
    )

    provider.partition.return_value = expected_document

    partitioner = DocumentPartitioner(
        provider=provider,
    )

    profile = DocumentProfile(
        document_id="doc-123",
        company_id="company-456",
        filename="company.pdf",
        extension=".pdf",
        mime_type="application/pdf",
        file_size=1024,
    )

    strategy = DocumentStrategy(
        parser="pdf",
        parsing_strategy="hi_res"
    )

    file_path = Path("company.pdf")

    result = partitioner.partition(
        file_path=file_path,
        profile=profile,
        strategy=strategy,
    )

    assert result is expected_document

    provider.partition.assert_called_once_with(
        file_path=file_path,
        profile=profile,
        strategy=strategy,
    )