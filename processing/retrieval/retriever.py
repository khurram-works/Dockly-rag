# from typing import Any, Dict, List
# from qdrant_client import QdrantClient
# from qdrant_client.models import FieldCondition, Filter, MatchValue


# class VectorRetriever:
#     def __init__(
#         self,
#         embedding_provider: Any,
#         qdrant_client: QdrantClient,
#         collection_name: str,

#     ) -> None:
#         self._embedding_provider = embedding_provider
#         self._qdrant_client = qdrant_client
#         self._collection_name = collection_name

#     def retrieve(
#         self,
#         query: str,
#         company_id: str,
#         limit: int = 5,
#     ) -> List[Dict[str, Any]]:
#         query_embedding = self._embedding_provider.embed_query(query)

#         query_filter = Filter(
#             must=[
#                 FieldCondition(
#                     key="company_id",
#                     match=MatchValue(value=company_id),
#                 )
#             ]
#         )

#         search_results = self._qdrant_client.query_points(
#             collection_name=self._collection_name,
#             query_vector=query_embedding.values,
#             query_filter=query_filter,
#             limit=limit,
#             with_payload=True,
#         )

#         return [
#             {
#                 "id": result.id,
#                 "score": result.score,
#                 "payload": result.payload,
#             }
#             for result in search_results
#         ]


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

    # def retrieve(
    #     self,
    #     query: str,
    #     company_id: str,
    #     limit: int = 5,
    # ) -> List[Dict[str, Any]]:
    #     # 1. Embed query
    #     query_embedding = self._embedding_provider.embed_query(query)
        
    #     # Ensure embedding vector is a flat list of floats
    #     vector = (
    #         query_embedding.values 
    #         if hasattr(query_embedding, "values") 
    #         else query_embedding
    #     )

    #     query_filter = Filter(
    #         must=[
    #             FieldCondition(
    #                 key="company_id",
    #                 match=MatchValue(value=company_id),
    #             )
    #         ]
    #     )

    #     # 2. Query Qdrant
    #     response = self._qdrant_client.query_points(
    #         collection_name=self._collection_name,
    #         query=vector,  # Changed from query_vector to query
    #         query_filter=query_filter,
    #         limit=limit,
    #         with_payload=True,
    #     )

    #     # 3. Extract points from QueryResponse
    #     return [
    #         {
    #             "id": point.id,
    #             "score": point.score,
    #             "payload": point.payload,
    #         }
    #         for point in response.points  # Extract from response.points
    #     ]
    def retrieve(
    self,
    query: str,
    company_id: str,
    limit: int = 5,
) -> List[Dict[str, Any]]:
    # 1. Get embedding from provider
        query_embedding = self._embedding_provider.embed_query(query)
    
        # If the provider returns a tuple, extract the vector (usually the 1st element)
        if isinstance(query_embedding, tuple):
            query_embedding = query_embedding[0]
    
        # Extract raw list if it's wrapped in an object attribute like .values
        if hasattr(query_embedding, "values"):
            vector = query_embedding.values
        else:
            vector = query_embedding
    
        # Final safety check: convert numpy array or tuple to standard list
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
    
        # 2. Pass clean vector list to Qdrant
        response = self._qdrant_client.query_points(
            collection_name=self._collection_name,
            query=vector,  # Must be List[float]
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
