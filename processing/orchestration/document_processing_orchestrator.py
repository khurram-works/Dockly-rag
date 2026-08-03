from pathlib import Path

from domain.models.document_profile import DocumentProfile

from processing.planning.strategy_planner import (
    StrategyPlanner,
)

from processing.partitioning.base_partitioner import (
    BasePartitioner,
)

from processing.filtering.filter_pipeline import (
    FilterPipeline,
)

from processing.chunking.base_chunker import (
    BaseChunker,
)

from processing.validation.chunk_validator import (
    ChunkValidator,
)

from processing.embedding.embedding_service import (
    EmbeddingService,
)

from processing.indexing.indexing_service import (
    IndexingService,
)

from core.logging import get_logger
 
logger = get_logger(__name__)

class DocumentProcessingOrchestrator:

    def __init__(
        self,
        strategy_planner: StrategyPlanner,
        partitioner: BasePartitioner,
        filter_pipeline: FilterPipeline,
        chunker: BaseChunker,
        chunk_validator: ChunkValidator,
        embedding_service: EmbeddingService,
        indexing_service: IndexingService,
    ) -> None:

        self._strategy_planner = strategy_planner
        self._partitioner = partitioner
        self._filter_pipeline = filter_pipeline
        self._chunker = chunker
        self._chunk_validator = chunk_validator
        self._embedding_service = embedding_service
        self._indexing_service = indexing_service

    def process(
        self,
        file_path: Path,
        profile: DocumentProfile,
    ) -> tuple[int, int | None ]:
        try:
            logger.info(
                "Starting document processing",
                document_id=profile.document_id,
                company_id=profile.company_id,
                filename=profile.filename,
            )

            strategy = self._strategy_planner.plan(profile)
            logger.info(
                "Strategy selected",
                parser=strategy.parser,
                parsing_strategy=strategy.parsing_strategy
            )

 
            parsed_document = self._partitioner.partition(
                file_path=file_path,
                profile=profile,
                strategy=strategy,
            )
            logger.info(
                "Document partitioned",
                elements_count=len(parsed_document.elements)
            )

            filtered_document = self._filter_pipeline.apply(parsed_document)
            logger.info(
                "Document filtering completed", 
                filtered_element_count=len(filtered_document.elements)
            )

            chunks = self._chunker.chunk(filtered_document)
            logger.info(
                "Chunks created", 
                chunks_count=len(chunks)
            )


            for chunk in chunks:
                self._chunk_validator.validate(chunk)


            embedded_chunks = self._embedding_service.embed_chunks(chunks)
            logger.info(
                "Embeddings generated", 
                embedded_count=len(embedded_chunks)
            )


            self._indexing_service.index(embedded_chunks)
            logger.info("Chunks indexed in vector database", indexed_count=len(embedded_chunks))

            logger.info(
                "Document processing completed",
                document_id=profile.document_id,
                chunks_created=len(chunks),
            )

            return len(chunks), parsed_document.page_count
            
        except Exception as e:
            logger.exception(
                "Processing failed document=%s company=%s file=%s",
                profile.document_id,
                profile.company_id,
                file_path,
            )
            raise