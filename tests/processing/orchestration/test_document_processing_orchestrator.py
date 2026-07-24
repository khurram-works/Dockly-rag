from pathlib import Path
from unittest.mock import Mock

from core.exceptions import ChunkValidationError

from domain.models.chunk_metadata import ChunkMetadata
from domain.models.document_chunk import DocumentChunk
from domain.models.document_profile import DocumentProfile
from domain.models.document_strategy import DocumentStrategy
from domain.models.embedded_chunk import EmbeddedChunk
from domain.models.embeddings import Embedding
from domain.models.parsed_document import ParsedDocument
from domain.models.vector_collection_config import (
    VectorCollectionConfig,
)

from processing.orchestration.document_processing_orchestrator import (
    DocumentProcessingOrchestrator,
)


def create_profile() -> DocumentProfile:

    return DocumentProfile(
        document_id="doc-123",
        company_id="company-456",
        filename="annual-report.pdf",
        extension=".pdf",
        mime_type="application/pdf",
        file_size=1024,
    )


def create_strategy() -> DocumentStrategy:

    return Mock(
        name="document-strategy",
    )


def create_parsed_document() -> ParsedDocument:

    return Mock(
        name="parsed-document",
    )


def create_filtered_document() -> ParsedDocument:

    return Mock(
        name="filtered-document",
    )


def create_chunk(
    index: int,
    text: str,
) -> DocumentChunk:

    return DocumentChunk(
        document_id="doc-123",
        filename="annual-report.pdf",
        company_id="company-456",
        chunk_index=index,
        text=text,
        metadata=ChunkMetadata(
            page_numbers=[1],
            languages=["eng"],
            coordinates=None,
            source_element_ids=[
                f"element-{index}",
            ],
            text_as_html=None,
        ),
    )


def create_embedded_chunk(
    chunk: DocumentChunk,
) -> EmbeddedChunk:

    return EmbeddedChunk(
        chunk=chunk,
        embedding=Embedding(
            values=(0.1, 0.2, 0.3),
        ),
    )


def create_collection_config() -> VectorCollectionConfig:

    return Mock(
        name="collection-config",
    )


def create_orchestrator():

    strategy_planner = Mock()

    partitioner = Mock()

    filter_pipeline = Mock()

    chunker = Mock()

    chunk_validator = Mock()

    embedding_service = Mock()

    collection_manager = Mock()

    indexing_service = Mock()

    orchestrator = DocumentProcessingOrchestrator(
        strategy_planner=strategy_planner,
        partitioner=partitioner,
        filter_pipeline=filter_pipeline,
        chunker=chunker,
        chunk_validator=chunk_validator,
        embedding_service=embedding_service,
        collection_manager=collection_manager,
        indexing_service=indexing_service,
    )

    return (
        orchestrator,
        strategy_planner,
        partitioner,
        filter_pipeline,
        chunker,
        chunk_validator,
        embedding_service,
        collection_manager,
        indexing_service,
    )


def test_orchestrator_processes_document_through_entire_pipeline():

    (
        orchestrator,
        strategy_planner,
        partitioner,
        filter_pipeline,
        chunker,
        chunk_validator,
        embedding_service,
        collection_manager,
        indexing_service,
    ) = create_orchestrator()

    file_path = Path(
        "documents/annual-report.pdf"
    )

    profile = create_profile()

    strategy = create_strategy()

    parsed_document = create_parsed_document()

    filtered_document = create_filtered_document()

    first_chunk = create_chunk(
        index=0,
        text="First chunk",
    )

    second_chunk = create_chunk(
        index=1,
        text="Second chunk",
    )

    chunks = [
        first_chunk,
        second_chunk,
    ]

    first_embedded_chunk = create_embedded_chunk(
        first_chunk
    )

    second_embedded_chunk = create_embedded_chunk(
        second_chunk
    )

    embedded_chunks = [
        first_embedded_chunk,
        second_embedded_chunk,
    ]

    collection_config = create_collection_config()

    strategy_planner.plan.return_value = strategy

    partitioner.partition.return_value = (
        parsed_document
    )

    filter_pipeline.apply.return_value = (
        filtered_document
    )

    chunker.chunk.return_value = chunks

    embedding_service.embed_chunks.return_value = (
        embedded_chunks
    )

    orchestrator.process(
        file_path=file_path,
        profile=profile,
        collection_config=collection_config,
    )

    strategy_planner.plan.assert_called_once_with(
        profile
    )

    partitioner.partition.assert_called_once_with(
        file_path=file_path,
        profile=profile,
        strategy=strategy,
    )

    filter_pipeline.apply.assert_called_once_with(
        parsed_document
    )

    chunker.chunk.assert_called_once_with(
        filtered_document
    )

    assert (
        chunk_validator.validate.call_count
        == 2
    )

    chunk_validator.validate.assert_any_call(
        first_chunk
    )

    chunk_validator.validate.assert_any_call(
        second_chunk
    )

    embedding_service.embed_chunks.assert_called_once_with(
        chunks
    )

    collection_manager.ensure_collection.assert_called_once_with(
        collection_config
    )

    indexing_service.index.assert_called_once_with(
        embedded_chunks
    )


def test_orchestrator_validates_every_chunk_before_embedding():

    (
        orchestrator,
        strategy_planner,
        partitioner,
        filter_pipeline,
        chunker,
        chunk_validator,
        embedding_service,
        collection_manager,
        indexing_service,
    ) = create_orchestrator()

    file_path = Path(
        "documents/annual-report.pdf"
    )

    profile = create_profile()

    strategy = create_strategy()

    parsed_document = create_parsed_document()

    filtered_document = create_filtered_document()

    first_chunk = create_chunk(
        index=0,
        text="First chunk",
    )

    second_chunk = create_chunk(
        index=1,
        text="Second chunk",
    )

    chunks = [
        first_chunk,
        second_chunk,
    ]

    embedded_chunks = [
        create_embedded_chunk(
            first_chunk
        ),
        create_embedded_chunk(
            second_chunk
        ),
    ]

    collection_config = create_collection_config()

    strategy_planner.plan.return_value = strategy

    partitioner.partition.return_value = (
        parsed_document
    )

    filter_pipeline.apply.return_value = (
        filtered_document
    )

    chunker.chunk.return_value = chunks

    embedding_service.embed_chunks.return_value = (
        embedded_chunks
    )

    orchestrator.process(
        file_path=file_path,
        profile=profile,
        collection_config=collection_config,
    )

    assert (
        chunk_validator.validate.call_count
        == len(chunks)
    )

    embedding_service.embed_chunks.assert_called_once_with(
        chunks
    )


def test_orchestrator_does_not_embed_or_index_invalid_chunk():

    (
        orchestrator,
        strategy_planner,
        partitioner,
        filter_pipeline,
        chunker,
        chunk_validator,
        embedding_service,
        collection_manager,
        indexing_service,
    ) = create_orchestrator()

    file_path = Path(
        "documents/annual-report.pdf"
    )

    profile = create_profile()

    strategy = create_strategy()

    parsed_document = create_parsed_document()

    filtered_document = create_filtered_document()

    valid_chunk = create_chunk(
        index=0,
        text="Valid chunk",
    )

    invalid_chunk = create_chunk(
        index=1,
        text="Invalid chunk",
    )

    chunks = [
        valid_chunk,
        invalid_chunk,
    ]

    strategy_planner.plan.return_value = strategy

    partitioner.partition.return_value = (
        parsed_document
    )

    filter_pipeline.apply.return_value = (
        filtered_document
    )

    chunker.chunk.return_value = chunks

    chunk_validator.validate.side_effect = [
        None,
        ChunkValidationError(
            "Chunk text cannot be empty."
        ),
    ]

    collection_config = create_collection_config()

    try:

        orchestrator.process(
            file_path=file_path,
            profile=profile,
            collection_config=collection_config,
        )

    except ChunkValidationError:

        pass

    else:

        raise AssertionError(
            "Expected ChunkValidationError"
        )

    embedding_service.embed_chunks.assert_not_called()

    collection_manager.ensure_collection.assert_not_called()

    indexing_service.index.assert_not_called()