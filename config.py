from dotenv import load_dotenv
import os

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
NODE_BACKEND_URL = os.getenv("NODE_BACKEND_URL")


QDRANT_COLLECTION_NAME = "dockly_documents"


VECTOR_SIZE = 384