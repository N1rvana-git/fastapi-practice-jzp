import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_user_registration_and_get(async_client: AsyncClient):
    response_post = await async_client.post("/users/", json={
        "username": "new_user",
        "email": "new@example.com",
        "password": "Validpassword",
    })
    assert response_post.status_code == 200
    user_data = response_post.json()
    assert user_data["username"] == "new_user"
    assert user_data["email"] == "new@example.com"
    assert "id" in user_data

    user_id = user_data["id"]

    response_fail = await async_client.post("/users/", json={
        "username": "new_user",
        "email": "new@example.com",
        "password": "Validpassword"
    })
    assert response_fail.status_code == 400
    assert response_fail.json() == {"detail":"email already registered"}

    response_get = await async_client.get(f"/users/{user_id}")
    assert response_get.status_code == 200
    assert response_get.json()["username"] == "new_user"