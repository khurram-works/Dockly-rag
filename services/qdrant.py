from qdrant_client import QdrantClient
from qdrant_client.models import (Distance, VectorParams, Document, PointStruct, FieldCondition, MatchValue, Filter)
from config import QDRANT_API_KEY, QDRANT_COLLECTION_NAME, QDRANT_URL, VECTOR_SIZE
import uuid
from qdrant_client import models 

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

    qdrant.create_payload_index(
        collection_name=QDRANT_COLLECTION_NAME,
        field_name="companyId",
        field_schema=models.PayloadSchemaType.KEYWORD,
    )
    qdrant.create_payload_index(
        collection_name=QDRANT_COLLECTION_NAME,
        field_name="documentId",
        field_schema=models.PayloadSchemaType.KEYWORD,
    )

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

    results = qdrant.query_points(
        collection_name = QDRANT_COLLECTION_NAME,
        query = query_embedding,
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
            "documentId": result.payload["documentId"],
            "score": result.score,
            "chunkIndex": result.payload["chunkIndex"],
            "pageNumber": result.payload.get("pageNumber", 1)
        }
        for result in results.points
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
    

    




