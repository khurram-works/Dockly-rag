from unittest.mock import Mock

from qdrant_client import models

from domain.models.vector_collection_config import (
    VectorCollectionConfig,
)
from infrastructure.qdrant.qdrant_collection_manager import (
    QdrantCollectionManager,
)


def create_config() -> VectorCollectionConfig:

    return VectorCollectionConfig(
        collection_name="dockly_documents",
        vector_size=384,
        distance=models.Distance.COSINE,
    )


def test_collection_manager_does_not_create_existing_collection():

    client = Mock()

    client.collection_exists.return_value = True

    manager = QdrantCollectionManager(
        client=client,
    )

    config = create_config()

    manager.ensure_collection(
        config,
    )

    client.collection_exists.assert_called_once_with(
        collection_name="dockly_documents",
    )

    client.create_collection.assert_not_called()


def test_collection_manager_creates_missing_collection():

    client = Mock()

    client.collection_exists.return_value = False

    manager = QdrantCollectionManager(
        client=client,
    )

    config = create_config()

    manager.ensure_collection(
        config,
    )

    client.create_collection.assert_called_once()


def test_collection_manager_uses_configured_collection_name():

    client = Mock()

    client.collection_exists.return_value = False

    manager = QdrantCollectionManager(
        client=client,
    )

    config = create_config()

    manager.ensure_collection(
        config,
    )

    call_kwargs = (
        client.create_collection.call_args.kwargs
    )

    assert (
        call_kwargs["collection_name"]
        == "dockly_documents"
    )


def test_collection_manager_uses_configured_vector_size():

    client = Mock()

    client.collection_exists.return_value = False

    manager = QdrantCollectionManager(
        client=client,
    )

    config = create_config()

    manager.ensure_collection(
        config,
    )

    call_kwargs = (
        client.create_collection.call_args.kwargs
    )

    vector_config = (
        call_kwargs["vectors_config"]
    )

    assert vector_config.size == 384


def test_collection_manager_uses_configured_distance():

    client = Mock()

    client.collection_exists.return_value = False

    manager = QdrantCollectionManager(
        client=client,
    )

    config = create_config()

    manager.ensure_collection(
        config,
    )

    call_kwargs = (
        client.create_collection.call_args.kwargs
    )

    vector_config = (
        call_kwargs["vectors_config"]
    )

    assert (
        vector_config.distance
        == models.Distance.COSINE
    )


def test_collection_manager_creates_correct_vector_params():

    client = Mock()

    client.collection_exists.return_value = False

    manager = QdrantCollectionManager(
        client=client,
    )

    config = create_config()

    manager.ensure_collection(
        config,
    )

    call_kwargs = (
        client.create_collection.call_args.kwargs
    )

    vector_config = (
        call_kwargs["vectors_config"]
    )

    assert isinstance(
        vector_config,
        models.VectorParams,
    )