from fastapi import Depends
from qdrant_client import QdrantClient
from qdrant_client.models import Distance

from api.controllers.document_controller import DocumentController
from api.services.document_processing_service import DocumentProcessingService
from core.config.settings import settings
from core.constants import EMBEDDING_MODEL_NAME, EMBEDDING_BATCH_SIZE

from processing.orchestration.document_processing_orchestrator import DocumentProcessingOrchestrator
from processing.planning.strategy_planner import StrategyPlanner
from processing.partitioning.document_partitioner import DocumentPartitioner
from processing.filtering.filter_pipeline import FilterPipeline
from processing.chunking.base_chunker import BaseChunker
from processing.validation.chunk_validator import ChunkValidator
from processing.embedding.embedding_service import EmbeddingService
from processing.indexing.indexing_service import IndexingService
from processing.indexing.vector_indexer import VectorIndexer
from processing.indexing.payload_builder import PayloadBuilder
from processing.inspection.document_inspector import DocumentInspector

from infrastructure.download.temporary_document import TemporaryDocument
from infrastructure.download.http_document_downloader import HttpDocumentDownloader
from infrastructure.qdrant.qdrant_vector_store import QdrantVectorStore
from infrastructure.qdrant.qdrant_collection_manager import QdrantCollectionManager

from providers.unstructured.provider import UnstructuredProvider
from providers.embeddings.sentence_transformer_provider import SentenceTransformerEmbeddingProvider

from domain.models.embedding_config import EmbeddingConfig
from domain.models.vector_collection_config import VectorCollectionConfig
from domain.models.document_chunking_strategy import DocumentChunkingStrategy
from domain.interfaces.embedding_provider import EmbeddingProvider 

from processing.chunking.unstructured_chunker import UnstructuredChunker
from processing.filtering.filters.empty_text_filter import EmptyTextFilter
from processing.filtering.filters.header_footer_filter import HeaderFooterFilter
from processing.filtering.filters.repeated_element_filter import RepeatedElementFilter


def get_qdrant_client() -> QdrantClient:
    return QdrantClient(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key,
        cloud_inference=True
    )

def get_collection_manager(
    client: QdrantClient = Depends(get_qdrant_client),
) -> QdrantCollectionManager:
    return QdrantCollectionManager(client=client)

def get_vector_collection_config() -> VectorCollectionConfig:
    return VectorCollectionConfig(
        collection_name=settings.qdrant_collection_name,
        vector_size=EMBEDDING_DIMENSION,
        distance=Distance.COSINE,
    )

def get_unstructured_provider() -> UnstructuredProvider:
    return UnstructuredProvider()

def get_strategy_planner() -> StrategyPlanner:
    return StrategyPlanner()

def get_partitioner() -> DocumentPartitioner:
    provider = get_unstructured_provider()
    return DocumentPartitioner(provider=provider)

def get_filter_pipeline() -> FilterPipeline:
    return FilterPipeline(
        filters=[
            EmptyTextFilter(),  
            HeaderFooterFilter(),
            RepeatedElementFilter(
                minimum_occurrences=2, 
                maximum_text_length=200,
            ),
        ]
    )

def get_chunker() -> BaseChunker:
    strategy = DocumentChunkingStrategy(
        max_characters=1500,
        new_after_n_chars=1000,
        combine_text_under_n_chars=1000,
        multipage_sections=True,
        include_orig_elements=True,
    )
    return UnstructuredChunker(strategy=strategy)

def get_embedding_service() -> EmbeddingService:
    config = EmbeddingConfig(
        model_name=EMBEDDING_MODEL_NAME,
        batch_size=EMBEDDING_BATCH_SIZE,
        normalize_embeddings=True,
    )
    provider = SentenceTransformerEmbeddingProvider(config=config)
    return EmbeddingService(provider=provider)


def get_embedding_provider(
    embedding_service: EmbeddingService = Depends(get_embedding_service)
) -> EmbeddingProvider:
    return embedding_service.provider

def get_payload_builder() -> PayloadBuilder:
    return PayloadBuilder()

def get_vector_indexer() -> VectorIndexer:
    payload_builder = get_payload_builder()
    return VectorIndexer(payload_builder=payload_builder)

def get_vector_store(
    client: QdrantClient = Depends(get_qdrant_client),
) -> QdrantVectorStore:
    return QdrantVectorStore(
        client=client,
        collection_name=settings.qdrant_collection_name,
    )

def get_indexing_service(
    vector_store: QdrantVectorStore = Depends(get_vector_store),
) -> IndexingService:
    indexer = get_vector_indexer()
    return IndexingService(indexer=indexer, vector_store=vector_store)

def get_document_orchestrator(
    indexing_service: IndexingService = Depends(get_indexing_service),
) -> DocumentProcessingOrchestrator:
    return DocumentProcessingOrchestrator(
        strategy_planner=get_strategy_planner(),
        partitioner=get_partitioner(),
        filter_pipeline=get_filter_pipeline(),
        chunker=get_chunker(),
        chunk_validator=ChunkValidator(),
        embedding_service=get_embedding_service(),
        indexing_service=indexing_service,
    )

def get_document_inspector() -> DocumentInspector:
    return DocumentInspector()
 

def get_document_processing_service(
    inspector: DocumentInspector = Depends(get_document_inspector),
    orchestrator: DocumentProcessingOrchestrator = Depends(get_document_orchestrator),
) -> DocumentProcessingService:
    temporary_document = TemporaryDocument(
        downloader=HttpDocumentDownloader()
    )
    return DocumentProcessingService(
        temporary_document=temporary_document,
        orchestrator=orchestrator,
        inspector=inspector, 
    )

def get_document_controller(
    processing_service: DocumentProcessingService = Depends(get_document_processing_service)
) -> DocumentController:
    return DocumentController(processing_service=processing_service)
