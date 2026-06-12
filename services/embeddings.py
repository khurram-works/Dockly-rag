from sentence_transformers import SentenceTransformer
from config import VECTOR_SIZE

model = SentenceTransformer("all-MiniLM-L6-v2")
print("Embedding model loaded successfully")

def generate_embedding(text: str) -> list[float]:
    embedding = model.encode(text)
    return embedding.tolist()

def generate_embeddings_batch(texts: list[str]) -> list[list[float]]:
    
    embeddings = model.encode(
        texts,
        batch_size = 32,
        show_progress_bar = True
    )

    return [embedding.tolist() for embedding in embeddings]


    
