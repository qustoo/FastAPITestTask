import pytest


async def test_get_all_users(async_client):
    response = await async_client.get("/users/")
    json_response = response.json()
    assert len(json_response["users"])


@pytest.mark.parametrize(
    "user_id, name, surname, age, birthdate",
    [("65ab0bb40466bfd28747be84", "ivan", "ivanov", 18, "2024-01-19T23:54:16.413000")],
)
async def test_get_user_by_id(
    user_id, name, surname, age, birthdate, async_client
):
    response = await async_client.get(f"/users/{user_id}")
    json_response = response.json()
    assert response.status_code == 200
    assert json_response["id"] == user_id
    assert json_response["name"] == name
    assert json_response["surname"] == surname
    assert json_response["age"] == age
    assert json_response["birthdate"] == birthdate


@pytest.mark.parametrize("name, surname", [("", "")])
async def test_empty_filter_users_by_name_surname(name, surname, async_client):
    total_users = await async_client.get("/users/")
    total_len = len(total_users.json()["users"])
    filter_users = await async_client.get("/users/filter")
    len_empty_filter = len(filter_users.json()["users"])
    assert total_len == len_empty_filter


@pytest.mark.parametrize("name, surname", [("ivan", ""), ("", "ivanov"), ("yakov",""),("","strelkov")])
async def test_filter_users_by_name_surname_with_one_empty(name, surname, async_client):
    filter_users = await async_client.get("/users/filter",params = {"name":name,"surname":surname})
    json_response = filter_users.json()["users"]
    for user in json_response:
        for k, v in user.items():
            if name == "":
                assert user["surname"] == surname
            elif surname == "":
                assert user["name"] == name
