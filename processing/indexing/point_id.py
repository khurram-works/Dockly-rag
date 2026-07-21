from uuid import NAMESPACE_URL, uuid5


def build_point_id(
    document_id: str,
    chunk_index: int,
) -> str:

    return str(
        uuid5(
            NAMESPACE_URL,
            f"{document_id}:{chunk_index}",
        )
    )