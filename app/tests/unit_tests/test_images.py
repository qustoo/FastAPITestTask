import pytest


@pytest.mark.parametrize(
    "file_id, filename, length, uploadDate",
    [
        (
            "65ab0bb30466bfd28747be81",
            "2. WHERE EXISTS.mp4_snapshot_06.44_[2023.10.04_19.07.12].jpg",
            115659,
            "2024-01-19T23:54:28.032000",
        ),
    ],
)
async def test_get_file_information(
    file_id, filename, length, uploadDate, async_client
):
    response = await async_client.get(f"/files/information/{file_id}")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["_id"] == file_id
    assert json_response["filename"] == filename
    assert json_response["length"] == length
    assert json_response["uploadDate"] == uploadDate
