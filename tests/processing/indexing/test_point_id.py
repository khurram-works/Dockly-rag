from uuid import UUID

from processing.indexing.point_id import build_point_id


def test_build_point_id_is_deterministic():

    first_id = build_point_id(
        document_id="doc-123",
        chunk_index=0,
    )

    second_id = build_point_id(
        document_id="doc-123",
        chunk_index=0,
    )

    assert first_id == second_id


def test_different_chunks_have_different_point_ids():

    first_id = build_point_id(
        document_id="doc-123",
        chunk_index=0,
    )

    second_id = build_point_id(
        document_id="doc-123",
        chunk_index=1,
    )

    assert first_id != second_id


def test_different_documents_have_different_point_ids():

    first_id = build_point_id(
        document_id="doc-123",
        chunk_index=0,
    )

    second_id = build_point_id(
        document_id="doc-456",
        chunk_index=0,
    )

    assert first_id != second_id





def test_build_point_id_returns_valid_uuid():

    point_id = build_point_id(
        document_id="doc-123",
        chunk_index=0,
    )

    parsed_uuid = UUID(point_id)

    assert str(parsed_uuid) == point_id