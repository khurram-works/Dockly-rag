from typing import Any, Dict, List
from qdrant_client import QdrantClient
from qdrant_client.models import FieldCondition, Filter, MatchValue


class VectorRetriever:
    def __init__(
        self,
        embedding_provider: Any,
        qdrant_client: QdrantClient,
        collection_name: str,
    ) -> None:
        self._embedding_provider = embedding_provider
        self._qdrant_client = qdrant_client
        self._collection_name = collection_name

   
    def retrieve(
    self,
    query: str,
    company_id: str,
    limit: int = 5,
) -> List[Dict[str, Any]]:

        query_embedding = self._embedding_provider.embed_query(query)
    

        if isinstance(query_embedding, tuple):
            query_embedding = query_embedding[0]

        if hasattr(query_embedding, "values"):
            vector = query_embedding.values
        else:
            vector = query_embedding
    

        if hasattr(vector, "tolist"):
            vector = vector.tolist()
        elif isinstance(vector, tuple):
            vector = list(vector)
    
        query_filter = Filter(
            must=[
                FieldCondition(
                    key="company_id",
                    match=MatchValue(value=company_id),
                )
            ]
        )

        

        response = self._qdrant_client.query_points(
            collection_name=self._collection_name,
            query=vector,  
            query_filter=query_filter,
            limit=limit,
            with_payload=True,
        )
    
        return [
            {
                "id": point.id,
                "score": point.score,
                "payload": point.payload,
            }
            for point in response.points
        ]
