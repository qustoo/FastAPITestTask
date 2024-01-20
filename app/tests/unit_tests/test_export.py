from httpx import AsyncClient
import pytest
import os


@pytest.mark.parametrize(
    "filename",
    [("test_filename.xlsx"), ("some_filename.xlsx"), ("bla_bla_filename.xlsx")],
)
async def test_export_data(async_client: AsyncClient, filename: str):
    response = await async_client.get("/export/", params={"filename": filename})
    assert response.status_code == 200
    assert os.path.exists(filename)
    os.remove(filename)
