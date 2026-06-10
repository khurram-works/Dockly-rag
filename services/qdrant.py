# from qdrant_client import QdrantClient
# from qdrant_client.models import (
#     VectorParams,      # Defines vector size and distance metric
#     Distance,          # The math used to compare vectors
#     PointStruct,       # Represents one vector + its metadata
#     Filter,            # For filtering search results
#     FieldCondition,    # One condition in a filter
#     MatchValue         # The value to match in a filter
# )
# from config import QDRANT_URL, QDRANT_API_KEY, QDRANT_COLLECTION_NAME, VECTOR_SIZE
# import uuid
# # uuid generates random unique IDs
# # Qdrant requires integer or UUID IDs for each point


# # ─────────────────────────────────────────────
# # Create the Qdrant client — connects to your cloud cluster
# # This runs once when the file is imported
# # ─────────────────────────────────────────────
# qdrant = QdrantClient(
#     url=QDRANT_URL,
#     api_key=QDRANT_API_KEY
# )


# # ─────────────────────────────────────────────
# # ensure_collection_exists
# # Creates the Qdrant collection if it doesn't exist yet
# # Safe to call multiple times — won't crash if already exists
# # ─────────────────────────────────────────────
# def ensure_collection_exists():
#     # Get list of all existing collections
#     existing = qdrant.get_collections()
#     existing_names = [col.name for col in existing.collections]
#     # List comprehension: get just the name from each collection object

#     if QDRANT_COLLECTION_NAME not in existing_names:
#         # Collection doesn't exist yet — create it
#         qdrant.create_collection(
#             collection_name=QDRANT_COLLECTION_NAME,
#             vectors_config=VectorParams(
#                 size=VECTOR_SIZE,
#                 # Every vector in this collection has exactly 384 numbers
#                 # Qdrant rejects vectors of any other size

#                 distance=Distance.COSINE
#                 # COSINE = use cosine similarity to compare vectors
#                 # This is the best metric for text similarity
#                 # Values range from 0 (completely different) to 1 (identical)
#             )
#         )
#         print(f"Created Qdrant collection: {QDRANT_COLLECTION_NAME}")
#     else:
#         print(f"Qdrant collection already exists: {QDRANT_COLLECTION_NAME}")


# # ─────────────────────────────────────────────
# # store_chunks
# # Takes processed chunks and stores them in Qdrant
# # This is called after PDF processing is complete
# # ─────────────────────────────────────────────
# def store_chunks(
#     chunks: list[str],           # The text chunks
#     embeddings: list[list[float]], # The vectors for each chunk
#     company_id: str,
#     document_id: str,
#     filename: str
# ) -> int:
#     # Returns the number of chunks stored

#     points = []
#     # We'll build a list of PointStruct objects
#     # Each PointStruct = one vector + its metadata

#     for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
#         # zip(chunks, embeddings) pairs each chunk with its embedding
#         # enumerate() gives us the index i (0, 1, 2, 3...)
#         # This is like chunks.forEach((chunk, i) => ...) in JavaScript

#         point = PointStruct(
#             id=str(uuid.uuid4()),
#             # Each point needs a unique ID
#             # uuid4() generates a random UUID like "a3f2b1c4-..."

#             vector=embedding,
#             # The 384 numbers representing this chunk's meaning

#             payload={
#                 # Payload = metadata stored alongside the vector
#                 # This is what gets returned when we search
#                 "companyId": company_id,
#                 "documentId": document_id,
#                 "filename": filename,
#                 "text": chunk,
#                 # The actual text — we need this to send to Groq later
#                 "chunkIndex": i
#                 # Which chunk number this is (0, 1, 2, 3...)
#             }
#         )
#         points.append(point)

#     # Upload all points to Qdrant in one batch operation
#     # Much faster than uploading one by one
#     qdrant.upsert(
#         collection_name=QDRANT_COLLECTION_NAME,
#         points=points
#         # upsert = insert if new, update if ID already exists
#         # Safer than insert which would crash on duplicates
#     )

#     return len(points)
#     # Return how many chunks were stored


# # ─────────────────────────────────────────────
# # search_similar_chunks
# # Takes a question vector and finds the most
# # similar chunks for a specific company
# # ─────────────────────────────────────────────
# def search_similar_chunks(
#     query_embedding: list[float],  # The question converted to a vector
#     company_id: str,               # Only search THIS company's chunks
#     limit: int = 5                 # Return top 5 most similar chunks
# ) -> list[dict]:

#     results = qdrant.search(
#         collection_name=QDRANT_COLLECTION_NAME,

#         query_vector=query_embedding,
#         # The vector to compare against all stored vectors

#         query_filter=Filter(
#             must=[
#                 FieldCondition(
#                     key="companyId",
#                     # Look at the companyId field in each point's payload
#                     match=MatchValue(value=company_id)
#                     # Only return points where companyId equals this value
#                 )
#             ]
#             # must = ALL conditions must be true (like AND in SQL)
#         ),
#         # This filter is your multi-tenancy wall
#         # Nike's search NEVER touches Tesla's vectors

#         limit=limit,
#         # Return only the top N most similar results

#         with_payload=True
#         # Include the payload (metadata + text) in results
#         # Without this we'd only get IDs and scores
#     )

#     # Convert results to a simple list of dictionaries
#     return [
#         {
#             "text": result.payload["text"],
#             "filename": result.payload["filename"],
#             "score": result.score,
#             # score = how similar (0 to 1, higher is better)
#             "chunkIndex": result.payload["chunkIndex"]
#         }
#         for result in results
#     ]


# # ─────────────────────────────────────────────
# # delete_document_chunks
# # Removes all chunks for a specific document
# # Called when a company deletes a document
# # ─────────────────────────────────────────────
# def delete_document_chunks(document_id: str):
#     qdrant.delete(
#         collection_name=QDRANT_COLLECTION_NAME,
#         points_selector=Filter(
#             must=[
#                 FieldCondition(
#                     key="documentId",
#                     match=MatchValue(value=document_id)
#                 )
#             ]
#         )
#         # Delete ALL points where documentId matches
#         # This cleans up Qdrant when a document is deleted from PostgreSQL
#     )

from qdrant_client import QdrantClient
from qdrant_client.models import (Distance, VectorParams, Document, PointStruct, FieldCondition, MatchValue, Filter)
from config import QDRANT_API_KEY, QDRANT_COLLECTION_NAME, QDRANT_URL, VECTOR_SIZE
import uuid

qdrant = QdrantClient(
    url = QDRANT_URL,
    api_key= QDRANT_API_KEY,
    cloud_inference = True
)

def ensure_collection_exists():
    existing = qdrant.get_collections()
    existing_names = [col.name for col in existing.collections]
    if QDRANT_COLLECTION_NAME not in existing_names:
        qdrant.create_collection(
            collection_name = QDRANT_COLLECTION_NAME,
            vectors_config = VectorParams(size = VECTOR_SIZE, distance = Distance.COSINE)
        )
        print(f"Created Qdrant collection: {QDRANT_COLLECTION_NAME}")
    else:
        print(f"Qdrant collection already exists: {QDRANT_COLLECTION_NAME}")

def store_chunks(chunks: list[dict], embeddings: list[list[float]], company_id: str,document_id: str, filename: str) -> int:
    points = []
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        point = PointStruct(
            id = str(uuid.uuid4()),
            vector = embedding,
            payload = {
                "companyId": company_id,
                "documentId": document_id,
                "filename": filename,
                "text": chunk["text"],
                "chunkIndex": i,
                "pageNumber": chunk["pageNumber"], 
            }
        )

        points.append(point)

    qdrant.upsert(
        collection_name = QDRANT_COLLECTION_NAME,
        points = points,
    )

    return len(points)

def search_similar_chunks(query_embedding: list[float], company_id: str, limit: int=5) -> list[dict]:
    results = qdrant.search(
        collection_name = QDRANT_COLLECTION_NAME,
        query_vector = query_embedding,
        query_filter = Filter(
            must = [
                FieldCondition(
                    key="companyId",
                    match = MatchValue(value = company_id)
                )
            ]
            
        ),
        limit = limit,
        with_payload = True,
    )

    return [
        {
            "text": result.payload["text"],
            "filename": result.payload["filename"],
            "score": result.score,
            "chunkIndex": result.payload["chunkIndex"],
            "pageNumber": result.payload.get("pageNumber", 1)
        }
        for result in results
    ]

def delete_document_chunks(document_id: str):
    qdrant.delete(
        collection_name = QDRANT_COLLECTION_NAME,
        points_selector = Filter(
            must = [
                FieldCondition(
                    key = "documentId",
                    match = MatchValue(value=document_id)
                )
            ]
        )
    )
    

    




