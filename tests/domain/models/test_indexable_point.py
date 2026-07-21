from domain.models.indexable_point import IndexablePoint


def test_indexable_point_stores_vector_and_payload():

    point = IndexablePoint(
        point_id="point-123",
        vector=(
            0.1,
            0.2,
            0.3,
        ),
        payload={
            "document_id": "doc-123",
            "company_id": "company-456",
        },
    )

    assert point.point_id == "point-123"

    assert point.vector == (
        0.1,
        0.2,
        0.3,
    )

    assert point.payload["document_id"] == "doc-123"
    assert point.payload["company_id"] == "company-456"