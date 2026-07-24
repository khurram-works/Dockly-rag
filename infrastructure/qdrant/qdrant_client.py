from qdrant_client import QdrantClient

from core.config.setttings import settings

def create_qdrant_client() -> QdrantClient:

    return QdrantClient(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key,
    )