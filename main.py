# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from contextlib import asynccontextmanager
# from api.routes.documents import router
# from services.qdrant import ensure_collection_exists
# from config import FRONTEND_URL, NODE_BACKEND_URL


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     print("Starting Dockly Python Service...")
#     try:
#         ensure_collection_exists()
#         print("Python service ready and collection verified!")
#     except Exception as e:
#         print(f"Error during startup: {e}")
    
#     yield
    
#     print("Shutting down Dockly Python Service...")

# app = FastAPI(
#     title="Dockly Python Service",
#     description="RAG pipeline for document processing and querying",
#     version="1.0.0",
#     lifespan=lifespan
# )

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[NODE_BACKEND_URL, FRONTEND_URL],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.include_router(router, prefix="/api")

# @app.get("/health")
# async def health_check():
#     return {"status": "healthy", "service": "dockly-python"}


# main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from qdrant_client.models import Distance

from api.routes.documents import router as document_router
from core.config.setttings import settings
from infrastructure.qdrant.qdrant_client import create_qdrant_client
from infrastructure.qdrant.qdrant_collection_manager import QdrantCollectionManager
from domain.models.vector_collection_config import VectorCollectionConfig

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting Dockly RAG Service...")
    try:
        client = create_qdrant_client()
        collection_manager = QdrantCollectionManager(client=client)
        
        # Configure collection based on embedding model
        # BAAI/bge-m3 produces 1024-dimensional vectors
        config = VectorCollectionConfig(
            collection_name=settings.qdrant_collection_name,
            vector_size=1024,  # BAAI/bge-m3 dimension
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