import pytest
from app.api.urls import DeskURLS
from app.models.user import get_user_model


create_desk_url = DeskURLS.create_desk_url
get_desk_list_url = DeskURLS.get_desk_list_url
create_type_url = DeskURLS.create_type_url
get_task_type_list_url = DeskURLS.get_task_type_list_url
create_task_url = DeskURLS.create_task_url
get_task_list_url = DeskURLS.get_task_list_url


@pytest.mark.asyncio
async def test_desk(db, client, get_token):
    token = await get_token
    headers = {"Authorization": token}
    desk_data = {"title": "test desk title"}

    # Проверяем успешное создание доски
    response = await client.post(create_desk_url, json=desk_data, headers=headers)
    assert response.status_code == 201
    assert response.text not in (None, {})
    desk_id = response.json().get("id")

    # Проверяем успешное получение списка досок
    response = await client.get(get_desk_list_url, headers=headers)
    assert response.status_code == 200
    assert response.text not in (None, {})

    # db_user = get_user_model(username=user.get("username"), db=db)

    # Проверяем успешное создание типа задачи
    task_type_data = {
        "title": "test task type",
        "color": "ffffff"
    }
    response = await client.post(create_type_url, json=task_type_data, headers=headers)
    assert response.status_code == 201
    task_type_id = response.json().get("id")

    # Проверяем получение списка типов задач
    response = await client.get(get_task_list_url, headers=headers)
    assert response.status_code == 200
    assert response.text not in (None, {})

    # Проверяем создание задачи
    task_data = {
        "desk_id": desk_id,
        "type_id": task_type_id,
        "title": "test task",
        "description": "test task description",
        "date_to": "2023-12-02T16:11:52.281705+03:00"
    }
    response = await client.post(create_task_url, json=task_data, headers=headers)
    assert response.status_code == 201

    task_data.pop("type_id")
    response = await client.post(create_task_url, json=task_data, headers=headers)
    assert response.status_code == 201

    task_data.pop("description")
    response = await client.post(create_task_url, json=task_data, headers=headers)
    assert response.status_code == 201

    # Проверяем получение списка задач
    response = await client.get(get_task_list_url, headers=headers)
    assert response.status_code == 200
    assert response.text not in (None, {})

