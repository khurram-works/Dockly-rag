from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class EmbeddingConfig:
    model_name: str
    batch_size: int = 32
    normalize_embeddings: bool = True