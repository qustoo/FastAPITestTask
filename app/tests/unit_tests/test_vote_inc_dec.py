import pytest


@pytest.mark.parametrize("user_id", [("65ab0bb40466bfd28747be84")])
async def test_inc_vote_value(user_id, async_client):
    before_inc = (await async_client.get(f"/users/{user_id}")).json()["vote_value"]
    response = await async_client.post(f"/users/inc_vote/{user_id}")
    after_inc = response.json()["vote_value"]
    assert response.status_code == 200
    assert after_inc - before_inc == 1


@pytest.mark.parametrize("user_id", [("65ab0bb40466bfd28747be84")])
async def test_dec_vote_value(user_id, async_client):
    before_inc = (await async_client.get(f"/users/{user_id}")).json()["vote_value"]
    response = await async_client.post(f"/users/dec_vote/{user_id}")
    after_inc = response.json()["vote_value"]
    assert response.status_code == 200
    assert before_inc - after_inc == 1
