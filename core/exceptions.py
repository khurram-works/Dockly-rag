class RAGPipelineError(Exception):
    """Base exception for all RAG pipeline errors."""


class UnsupportedDocumentError(RAGPipelineError):
    """Raised when no parsing strategy exists for a document type."""


class DocumentDownloadError(RAGPipelineError):
    """Raised when a document cannot be downloaded."""


class PartitioningError(RAGPipelineError):
    """Raised when document partitioning fails."""


class EmbeddingError(RAGPipelineError):
    """Raised when embedding generation fails."""


class StorageError(RAGPipelineError):
    """Raised when indexing or storage fails."""


class RetrievalError(RAGPipelineError):
    """Raised when document retrieval fails."""

