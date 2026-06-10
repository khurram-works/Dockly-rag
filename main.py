# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from routes.documents import router
# from services.qdrant import ensure_collection_exists

# # Create the FastAPI app
# # This is like const app = express() in Node.js
# app = FastAPI(
#     title="Dockly Python Service",
#     description="RAG pipeline for document processing and querying",
#     version="1.0.0"
# )

# # CORS middleware — allows Node.js to call this Python server
# # Without this, requests from Node.js would be blocked
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5000", "http://localhost:3000"],
#     # Allow requests from your Node.js backend and Next.js frontend
#     allow_credentials=True,
#     allow_methods=["*"],   # Allow all HTTP methods
#     allow_headers=["*"],   # Allow all headers
# )

# # Register our router
# # prefix="/api" means all routes become /api/process-document and /api/query
# app.include_router(router, prefix="/api")
# # This is like app.use('/api', documentRoutes) in Express

# # Health check endpoint
# # Used to verify the server is running
# @app.get("/health")
# async def health_check():
#     return {"status": "healthy", "service": "dockly-python"}

# # Startup event — runs once when server starts
# @app.on_event("startup")
# async def startup_event():
#     print("Starting Dockly Python Service...")
#     ensure_collection_exists()
#     # Make sure Qdrant collection exists before accepting any requests
#     print("Python service ready!")


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




