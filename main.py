from fastapi import FastAPI
from contextlib import asynccontextmanager
from qdrant_client.models import Distance
from fastapi.middleware.cors import CORSMiddleware 

from api.routes.documents import router as document_router
from core.config.settings import settings
from infrastructure.qdrant.qdrant_client import create_qdrant_client
from infrastructure.qdrant.qdrant_collection_manager import QdrantCollectionManager
from domain.models.vector_collection_config import VectorCollectionConfig

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting Dockly RAG Service...")
    try:
        client = create_qdrant_client()
        collection_manager = QdrantCollectionManager(client=client)
        config = VectorCollectionConfig(
            collection_name=settings.qdrant_collection_name,
            vector_size=1024,
            distance=Distance.COSINE,
        )
        
        collection_manager.ensure_collection(config)
        print(f"Qdrant collection '{settings.qdrant_collection_name}' ready!")
    except Exception as e:
        print(f"Error during startup: {e}")
        raise
    
    yield
    print("Shutting down Dockly RAG Service...")

app = FastAPI(
    title="Dockly RAG Service",
    lifespan=lifespan,
)

app.include_router(document_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, settings.node_backend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}