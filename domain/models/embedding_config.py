from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class EmbeddingConfig:

    model_name: str

    batch_size: int = 32

    normalize_embeddings: bool = True

    def __post_init__(self) -> None:

        if not self.model_name.strip():

            raise ValueError(
                "Embedding model name cannot be empty."
            )

        if self.batch_size <= 0:

            raise ValueError(
                "Embedding batch size must be greater than zero."
            )