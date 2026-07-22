from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from core.exceptions import PartitioningError

from domain.enums.element_type import ElementType
from domain.enums.parser_strategy import ParsingStrategy
from domain.enums.parser_type import ParserType

from domain.models.document_profile import DocumentProfile
from domain.models.document_strategy import DocumentStrategy

from providers.unstructured.provider import (
    UnstructuredProvider,
)


def test_provider_routes_pdf_to_pdf_handler(
    tmp_path,
):

    file_path = tmp_path / "company.pdf"

    file_path.touch()

    provider = UnstructuredProvider()

    profile = DocumentProfile(
        document_id="doc-123",
        company_id="company-456",
        filename="company.pdf",
        extension=".pdf",
        mime_type="application/pdf",
        file_size=1024,
    )

    strategy = DocumentStrategy(
        parser=ParserType.PDF,
        parsing_strategy=ParsingStrategy.FAST,
    )

    expected_document = Mock()

    provider._partition_pdf = Mock(
        return_value=expected_document,
    )

    provider._handlers[ParserType.PDF] = (
        provider._partition_pdf
    )

    result = provider.partition(
        file_path=file_path,
        profile=profile,
        strategy=strategy,
    )

    assert result is expected_document

    provider._partition_pdf.assert_called_once_with(
        file_path=file_path,
        profile=profile,
        strategy=strategy,
    )


def test_provider_rejects_missing_file():

    provider = UnstructuredProvider()

    profile = DocumentProfile(
        document_id="doc-123",
        company_id="company-456",
        filename="company.pdf",
        extension=".pdf",
        mime_type="application/pdf",
        file_size=1024,
    )

    strategy = DocumentStrategy(
        parser=ParserType.PDF,
        parsing_strategy=ParsingStrategy.FAST,
    )

    with pytest.raises(PartitioningError):

        provider.partition(
            file_path=Path(
                "does-not-exist.pdf"
            ),
            profile=profile,
            strategy=strategy,
        )


def test_provider_rejects_unsupported_parser(
    tmp_path,
):

    file_path = tmp_path / "company.pdf"

    file_path.touch()

    provider = UnstructuredProvider()

    profile = DocumentProfile(
        document_id="doc-123",
        company_id="company-456",
        filename="company.pdf",
        extension=".pdf",
        mime_type="application/pdf",
        file_size=1024,
    )

    strategy = Mock()

    strategy.parser = "unsupported-parser"

    with pytest.raises(PartitioningError):

        provider.partition(
            file_path=file_path,
            profile=profile,
            strategy=strategy,
        )


def test_provider_converts_unstructured_elements_to_domain_elements(
    tmp_path,
):

    file_path = tmp_path / "company.pdf"

    file_path.touch()

    provider = UnstructuredProvider()

    profile = DocumentProfile(
        document_id="doc-123",
        company_id="company-456",
        filename="company.pdf",
        extension=".pdf",
        mime_type="application/pdf",
        file_size=1024,
    )

    strategy = DocumentStrategy(
        parser=ParserType.PDF,
        parsing_strategy=ParsingStrategy.FAST,
    )

    fake_element = Mock()

    fake_element.element_id = "element-123"

    fake_element.text = (
        "Our company builds software."
    )

    fake_element.category = "NarrativeText"

    fake_element.metadata = Mock()

    fake_element.metadata.page_number = 1

    fake_element.metadata.languages = [
        "eng"
    ]

    fake_element.metadata.coordinates = None

    fake_element.metadata.text_as_html = None

    with patch(
        "providers.unstructured.provider.partition_pdf",
        return_value=[
            fake_element
        ],
    ):

        result = provider.partition(
            file_path=file_path,
            profile=profile,
            strategy=strategy,
        )

    assert result.document_id == (
        "doc-123"
    )

    assert result.company_id == (
        "company-456"
    )

    assert result.filename == (
        "company.pdf"
    )

    assert result.page_count == 1

    assert len(result.elements) == 1

    element = result.elements[0]

    assert element.element_id == (
        "element-123"
    )

    assert element.text == (
        "Our company builds software."
    )

    assert element.element_type == (
        ElementType.NARRATIVE
    )

    assert element.metadata.page_number == 1

    assert element.metadata.languages == [
        "eng"
    ]


def test_provider_preserves_table_element(
    tmp_path,
):

    file_path = tmp_path / "company.pdf"

    file_path.touch()

    provider = UnstructuredProvider()

    profile = DocumentProfile(
        document_id="doc-123",
        company_id="company-456",
        filename="company.pdf",
        extension=".pdf",
        mime_type="application/pdf",
        file_size=1024,
    )

    strategy = DocumentStrategy(
        parser=ParserType.PDF,
        parsing_strategy=ParsingStrategy.FAST,
    )

    fake_table = Mock()

    fake_table.element_id = "table-123"

    fake_table.text = (
        "Product | Revenue"
    )

    fake_table.category = "Table"

    fake_table.metadata = Mock()

    fake_table.metadata.page_number = 2

    fake_table.metadata.languages = [
        "eng"
    ]

    fake_table.metadata.coordinates = None

    fake_table.metadata.text_as_html = (
        "<table>...</table>"
    )

    with patch(
        "providers.unstructured.provider.partition_pdf",
        return_value=[
            fake_table
        ],
    ):

        result = provider.partition(
            file_path=file_path,
            profile=profile,
            strategy=strategy,
        )

    element = result.elements[0]

    assert element.element_type == (
        ElementType.TABLE
    )

    assert element.metadata.text_as_html == (
        "<table>...</table>"
    )

    assert element.metadata.page_number == 2

def test_provider_maps_uncategorized_text(
    tmp_path,
):

    file_path = tmp_path / "company.pdf"

    file_path.touch()

    provider = UnstructuredProvider()

    profile = DocumentProfile(
        document_id="doc-123",
        company_id="company-456",
        filename="company.pdf",
        extension=".pdf",
        mime_type="application/pdf",
        file_size=1024,
    )

    strategy = DocumentStrategy(
        parser=ParserType.PDF,
        parsing_strategy=ParsingStrategy.FAST,
    )

    fake_element = Mock()

    fake_element.element_id = "element-123"

    fake_element.text = (
        "Uncategorized document text."
    )

    fake_element.category = (
        "UncategorizedText"
    )

    fake_element.metadata = Mock()

    fake_element.metadata.page_number = 1

    fake_element.metadata.languages = [
        "eng"
    ]

    fake_element.metadata.coordinates = None

    fake_element.metadata.text_as_html = None

    with patch(
        "providers.unstructured.provider.partition_pdf",
        return_value=[
            fake_element
        ],
    ):

        result = provider.partition(
            file_path=file_path,
            profile=profile,
            strategy=strategy,
        )

    element = result.elements[0]

    assert element.element_type == (
        ElementType.UNCATEGORIZED
    )


def test_provider_wraps_partitioning_failure(
    tmp_path,
):

    file_path = tmp_path / "company.pdf"

    file_path.touch()

    provider = UnstructuredProvider()

    profile = DocumentProfile(
        document_id="doc-123",
        company_id="company-456",
        filename="company.pdf",
        extension=".pdf",
        mime_type="application/pdf",
        file_size=1024,
    )

    strategy = DocumentStrategy(
        parser=ParserType.PDF,
        parsing_strategy=ParsingStrategy.FAST,
    )

    with patch(
        "providers.unstructured.provider.partition_pdf",
        side_effect=RuntimeError(
            "Underlying parser failed"
        ),
    ):

        with pytest.raises(
            PartitioningError,
            match="Failed to partition",
        ):

            provider.partition(
                file_path=file_path,
                profile=profile,
                strategy=strategy,
            )