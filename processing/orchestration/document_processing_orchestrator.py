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
    ) -> int:


        strategy = self._strategy_planner.plan(
            profile
        )

        parsed_document = self._partitioner.partition(
            file_path=file_path,
            profile=profile,
            strategy=strategy,
        )


        filtered_document = self._filter_pipeline.apply(
            parsed_document
        )


        chunks = self._chunker.chunk(
            filtered_document
        )



        for chunk in chunks:

            self._chunk_validator.validate(
                chunk
            )



        embedded_chunks = (
            self._embedding_service.embed_chunks(
                chunks
            )
        )



        self._indexing_service.index(
            embedded_chunks
        )

        return len(chunks)