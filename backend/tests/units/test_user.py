import pytest
from app.schemas.user import UserLoginSchema
from app.api.urls import UserURLS

register_url = UserURLS.register_url
login_url = UserURLS.login_url
user_data_url = UserURLS.user_data_url


@pytest.mark.asyncio
async def test_register(db, client, get_user_data):
    register_data = await get_user_data

    # Проверяем успешную регистрацию
    response = await client.post(register_url, json=register_data)
    assert response.status_code == 201

    # Проверяем неуспешную повторную регистрацию
    response = await client.post(register_url, json=register_data)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_login_and_get_user_data(db, client, get_user):
    user_data = await get_user
    login_data = UserLoginSchema(**user_data)
    login_data = login_data.dict()

    # Проверяем удачный логин
    response = await client.post(login_url, json=login_data)
    assert response.status_code == 200
    response_json = response.json()
    assert "token" in response_json and "type" in response_json

    headers = {"Authorization": f"{response_json.get('type')} {response_json.get('token')}"}
    response = await client.get(user_data_url, headers=headers)
    assert response.status_code == 200

    # Проверяем неуспешный логин
    login_data["password"] = "some_other_password"
    response = await client.post(login_url, json=login_data)
    assert response.status_code == 401
