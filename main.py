from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from routes.documents import router
from services.qdrant import ensure_collection_exists
from config import FRONTEND_URL, NODE_BACKEND_URL


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting Dockly Python Service...")
    try:
        ensure_collection_exists()
        print("Python service ready and collection verified!")
    except Exception as e:
        print(f"Error during startup: {e}")
    
    yield
    
    print("Shutting down Dockly Python Service...")

app = FastAPI(
    title="Dockly Python Service",
    description="RAG pipeline for document processing and querying",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[NODE_BACKEND_URL, FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "dockly-python"}
