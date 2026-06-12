from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.documents import router
from services.qdrant import ensure_collection_exists

app = FastAPI(
    title="Dockly Python Service",
    description="RAG pipeline for document processing and querying",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5000", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "dockly-python"}

@app.on_event("startup")
async def startup_event():
    print("Starting Dockly Python Service...")
    ensure_collection_exists()
    print("Python service ready!")




