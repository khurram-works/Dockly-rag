import numpy as np
from unittest.mock import Mock, patch

from domain.models.embedding_config import EmbeddingConfig
from providers.embeddings.sentence_transformer_provider import (
    SentenceTransformerEmbeddingProvider,
)



def test_embed_documents_returns_empty_list_for_empty_input():

    config = EmbeddingConfig(
        model_name="fake-model",
    )

    with patch(
        "providers.embeddings.sentence_transformer_provider.SentenceTransformer"
    ) as model_class:

        provider = SentenceTransformerEmbeddingProvider(
            config=config,
        )

        embeddings = provider.embed_documents([])

        assert embeddings == []

        model_class.return_value.encode_document.assert_not_called()


def test_embed_documents_preserves_input_count():

    config = EmbeddingConfig(
        model_name="fake-model",
    )

    fake_model = Mock()

    fake_model.encode_document.return_value = np.array([
        [0.1, 0.2, 0.3],
        [0.4, 0.5, 0.6],
    ])

    with patch(
        "providers.embeddings.sentence_transformer_provider.SentenceTransformer",
        return_value=fake_model,
    ):

        provider = SentenceTransformerEmbeddingProvider(
            config=config,
        )

        embeddings = provider.embed_documents([
            "first document",
            "second document",
        ])

        assert len(embeddings) == 2


def test_embed_documents_preserves_embedding_order():

    config = EmbeddingConfig(
        model_name="fake-model",
    )

    fake_model = Mock()

    fake_model.encode_document.return_value = np.array([
        [1.0, 2.0, 3.0],
        [4.0, 5.0, 6.0],
    ])

    with patch(
        "providers.embeddings.sentence_transformer_provider.SentenceTransformer",
        return_value=fake_model,
    ):

        provider = SentenceTransformerEmbeddingProvider(
            config=config,
        )

        embeddings = provider.embed_documents([
            "first document",
            "second document",
        ])

        assert embeddings[0].values == (
            1.0,
            2.0,
            3.0,
        )

        assert embeddings[1].values == (
            4.0,
            5.0,
            6.0,
        )



def test_embed_query_returns_embedding():

    config = EmbeddingConfig(
        model_name="fake-model",
    )

    fake_model = Mock()

    fake_model.encode_query.return_value = np.array([
        0.1,
        0.2,
        0.3,
    ])

    with patch(
        "providers.embeddings.sentence_transformer_provider.SentenceTransformer",
        return_value=fake_model,
    ):

        provider = SentenceTransformerEmbeddingProvider(
            config=config,
        )

        embedding = provider.embed_query(
            "What does the company do?"
        )

        assert embedding.values == (
            0.1,
            0.2,
            0.3,
        )

        assert embedding.dimension == 3


def test_provider_passes_configuration_to_model():

    config = EmbeddingConfig(
        model_name="my-model",
    )

    with patch(
        "providers.embeddings.sentence_transformer_provider.SentenceTransformer"
    ) as model_class:

        SentenceTransformerEmbeddingProvider(
            config=config,
        )

        model_class.assert_called_once_with(
            "my-model"
        )

def test_embed_documents_passes_embedding_configuration():

    config = EmbeddingConfig(
        model_name="fake-model",
        batch_size=16,
        normalize_embeddings=False,
    )

    fake_model = Mock()

    fake_model.encode_document.return_value = np.array([
        [0.1, 0.2, 0.3],
    ])

    with patch(
        "providers.embeddings.sentence_transformer_provider.SentenceTransformer",
        return_value=fake_model,
    ):

        provider = SentenceTransformerEmbeddingProvider(
            config=config,
        )

        provider.embed_documents([
            "first document",
        ])

        fake_model.encode_document.assert_called_once_with(
          ["first document"],
          batch_size=16,
          normalize_embeddings=False,
          convert_to_numpy=True,
        )


def test_embed_query_passes_normalization_configuration():

    config = EmbeddingConfig(
        model_name="fake-model",
        normalize_embeddings=False,
    )

    fake_model = Mock()

    fake_model.encode_query.return_value = np.array([
        0.1,
        0.2,
        0.3,
    ])

    with patch(
        "providers.embeddings.sentence_transformer_provider.SentenceTransformer",
        return_value=fake_model,
    ):

        provider = SentenceTransformerEmbeddingProvider(
            config=config,
        )

        provider.embed_query(
            "What does the company do?"
        )

        fake_model.encode_query.assert_called_once_with(
          "What does the company do?",
          normalize_embeddings=False,
          convert_to_numpy=True,
        )