# from sentence_transformers import SentenceTransformer
# from config import VECTOR_SIZE

# # ─────────────────────────────────────────────
# # Load the model once at module level
# # ─────────────────────────────────────────────

# # This line runs ONCE when your Python server starts
# # The first time ever, it downloads ~80MB from the internet
# # Every time after, it loads from your local disk in ~2 seconds
# # It never runs again during the server's lifetime
# model = SentenceTransformer("all-MiniLM-L6-v2")

# print("Embedding model loaded successfully")
# # This print confirms the model loaded when you start the server


# # ─────────────────────────────────────────────
# # generate_embedding
# # Converts a single piece of text into a vector
# # Returns a list of 384 numbers
# # ─────────────────────────────────────────────
# def generate_embedding(text: str) -> list[float]:
#     # list[float] means a list of decimal numbers

#     embedding = model.encode(text)
#     # model.encode() is the magic function
#     # It takes a string and returns a numpy array of 384 numbers

#     return embedding.tolist()
#     # .tolist() converts numpy array to a regular Python list
#     # Qdrant needs a regular Python list, not a numpy array


# # ─────────────────────────────────────────────
# # generate_embeddings_batch
# # Converts MULTIPLE texts at once — much faster
# # than calling generate_embedding() in a loop
# # ─────────────────────────────────────────────
# def generate_embeddings_batch(texts: list[str]) -> list[list[float]]:
#     # list[list[float]] = a list of vectors
#     # Each vector is a list of 384 numbers

#     embeddings = model.encode(
#         texts,
#         # Pass all texts at once — the model processes them in parallel
#         # This is 5-10x faster than encoding one by one

#         batch_size=32,
#         # Process 32 texts at a time internally
#         # Good balance of speed and memory usage

#         show_progress_bar=True
#         # Shows a progress bar in the terminal while processing
#         # Useful for large documents with many chunks
#     )

#     return [embedding.tolist() for embedding in embeddings]
#     # List comprehension converting each numpy array to a Python list
#     # Same as: embeddings.map(e => Array.from(e)) in JavaScript

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


    
