import pytest

from core.exceptions import ChunkValidationError

from domain.models.chunk_metadata import ChunkMetadata
from domain.models.document_chunk import DocumentChunk

from processing.validation.chunk_validator import (
    ChunkValidator,
)


def create_valid_chunk() -> DocumentChunk:

    return DocumentChunk(
        document_id="doc-123",
        filename="company.pdf",
        company_id="company-456",
        chunk_index=0,
        text="ACME builds software products.",
        metadata=ChunkMetadata(
            page_numbers=[1],
            languages=["eng"],
            coordinates=None,
            source_element_ids=["element-123"],
            text_as_html=None,
        ),
    )


def test_valid_chunk_passes_validation():

    chunk = create_valid_chunk()

    validator = ChunkValidator()

    result = validator.validate(chunk)

    assert result is None


def test_empty_document_id_is_rejected():

    chunk = create_valid_chunk()

    chunk.document_id = ""

    validator = ChunkValidator()

    with pytest.raises(
        ChunkValidationError,
        match="document_id",
    ):

        validator.validate(chunk)


def test_whitespace_document_id_is_rejected():

    chunk = create_valid_chunk()

    chunk.document_id = "   "

    validator = ChunkValidator()

    with pytest.raises(
        ChunkValidationError,
        match="document_id",
    ):

        validator.validate(chunk)


def test_empty_company_id_is_rejected():

    chunk = create_valid_chunk()

    chunk.company_id = ""

    validator = ChunkValidator()

    with pytest.raises(
        ChunkValidationError,
        match="company_id",
    ):

        validator.validate(chunk)


def test_whitespace_company_id_is_rejected():

    chunk = create_valid_chunk()

    chunk.company_id = "   "

    validator = ChunkValidator()

    with pytest.raises(
        ChunkValidationError,
        match="company_id",
    ):

        validator.validate(chunk)


def test_empty_filename_is_rejected():

    chunk = create_valid_chunk()

    chunk.filename = ""

    validator = ChunkValidator()

    with pytest.raises(
        ChunkValidationError,
        match="filename",
    ):

        validator.validate(chunk)


def test_whitespace_filename_is_rejected():

    chunk = create_valid_chunk()

    chunk.filename = "   "

    validator = ChunkValidator()

    with pytest.raises(
        ChunkValidationError,
        match="filename",
    ):

        validator.validate(chunk)


def test_empty_text_is_rejected():

    chunk = create_valid_chunk()

    chunk.text = ""

    validator = ChunkValidator()

    with pytest.raises(
        ChunkValidationError,
        match="text",
    ):

        validator.validate(chunk)


def test_whitespace_only_text_is_rejected():

    chunk = create_valid_chunk()

    chunk.text = "   \n\t  "

    validator = ChunkValidator()

    with pytest.raises(
        ChunkValidationError,
        match="text",
    ):

        validator.validate(chunk)


def test_negative_chunk_index_is_rejected():

    chunk = create_valid_chunk()

    chunk.chunk_index = -1

    validator = ChunkValidator()

    with pytest.raises(
        ChunkValidationError,
        match="chunk_index",
    ):

        validator.validate(chunk)


def test_zero_chunk_index_is_valid():

    chunk = create_valid_chunk()

    chunk.chunk_index = 0

    validator = ChunkValidator()

    result = validator.validate(chunk)

    assert result is None


def test_positive_chunk_index_is_valid():

    chunk = create_valid_chunk()

    chunk.chunk_index = 10

    validator = ChunkValidator()

    result = validator.validate(chunk)

    assert result is None