from fastapi import Depends
from qdrant_client import QdrantClient
from qdrant_client.models import Distance

from api.controllers.document_controller import (
    DocumentController,
)

from domain.models.embedding_config import (
    EmbeddingConfig,
)

from domain.models.vector_collection_config import (
    VectorCollectionConfig,
)

from providers.embeddings.sentence_transformer_provider import (
    SentenceTransformerEmbeddingProvider,
)

from processing.embedding.embedding_service import (
    EmbeddingService,
)

from processing.planning.strategy_planner import (
    StrategyPlanner,
)

from processing.partitioning.document_partitioner import (
    DocumentPartitioner,
)

from processing.filtering.filter_pipeline import (
    FilterPipeline,
)

from processing.chunking.unstructured_chunker import (
    UnstructuredChunker,
)

from processing.validation.chunk_validator import (
    ChunkValidator,
)

from processing.indexing.vector_indexer import (
    VectorIndexer,
)

from processing.indexing.payload_builder import (
    PayloadBuilder,
)

from processing.indexing.indexing_service import (
    IndexingService,
)

from infrastructure.qdrant.qdrant_vector_store import (
    QdrantVectorStore,
)

from infrastructure.qdrant.qdrant_collection_manager import (
    QdrantCollectionManager,
)

from processing.orchestration.document_processing_orchestrator import (
    DocumentProcessingOrchestrator,
)

from infrastructure.qdrant.qdrant_client import (
    create_qdrant_client,
)



def get_embedding_service() -> EmbeddingService:

    config = EmbeddingConfig(
        model_name="BAAI/bge-m3",
        batch_size=32,
        normalize_embeddings=True,
    )

    provider = SentenceTransformerEmbeddingProvider(
        config=config,
    )

    return EmbeddingService(
        provider=provider,
    )


def get_collection_config() -> VectorCollectionConfig:

    return VectorCollectionConfig(
        collection_name="dockly_documents",
        vector_size=1024,
        distance=Distance.COSINE,
    )


def get_qdrant_client() -> QdrantClient:

    return create_qdrant_client()


def get_indexing_service() -> IndexingService:

    payload_builder = PayloadBuilder()

    vector_indexer = VectorIndexer(
        payload_builder=payload_builder,
    )

    vector_store = get_vector_store()

    return IndexingService(
        indexer=vector_indexer,
        vector_store=vector_store,
    )


def get_document_orchestrator() -> (
    DocumentProcessingOrchestrator
):

    strategy_planner = StrategyPlanner()

    # Your actual Unstructured provider
    unstructured_provider = (
        get_unstructured_provider()
    )

    partitioner = DocumentPartitioner(
        provider=unstructured_provider,
    )

    filter_pipeline = FilterPipeline(
        filters=[]
    )

    chunker = DocumentChunker()

    chunk_validator = ChunkValidator()

    embedding_service = (
        get_embedding_service()
    )

    indexing_service = (
        get_indexing_service()
    )

    return DocumentProcessingOrchestrator(
        strategy_planner=strategy_planner,
        partitioner=partitioner,
        filter_pipeline=filter_pipeline,
        chunker=chunker,
        chunk_validator=chunk_validator,
        embedding_service=embedding_service,
        indexing_service=indexing_service,
    )


def get_document_controller() -> DocumentController:

    orchestrator = (
        get_document_orchestrator()
    )

    return DocumentController(
        orchestrator=orchestrator,
    )