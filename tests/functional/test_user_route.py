import pytest
from src.extensions import SecurityManager

from src.models.user_model import User

router_prefix = "/user"


@pytest.mark.parametrize(
    "user_data",
    [
        {
            "username": "test_user_1",
            "password": "test_user_pw_1",
            "name": "test_user_1",
            "surname": "test_user_1",
        },
        {
            "username": "test_user_2",
            "password": "test_user_pw_2",
            "name": "test_user_2",
            "surname": "test_user_2",
        },
        {
            "username": "test_user_3",
            "password": "test_user_pw_3",
            "name": "test_user_3",
            "surname": "test_user_3",
        },
    ],
)
def test_post_user_ok(client, user_data, session):
    # test user creation
    response = client.post(router_prefix, json=user_data)
    created = session.query(User).filter_by(username=user_data["username"]).first()
    assert response.status_code == 201
    assert user_data["username"] == created.username


@pytest.mark.parametrize(
    "user_data",
    [
        {"username": "", "password": ""},
        {"username": "name", "password": ""},
        {"username": "", "password": "password", "name": "name", "surname": "surname"},
        {"username": "name", "password": "pas", "name": "name", "surname": "surname"},
        {"username": "name" * 6, "password": "password"},
        {"username": "name", "password": "password" * 6},
    ],
)
def test_post_user_bad_data(client, user_data, session):
    # test user creation with bad data
    response = client.post(router_prefix, json=user_data)
    assert response.status_code == 422
    assert response.json()
    assert response.json()["detail"][0]["msg"]


@pytest.mark.parametrize(
    "user_data",
    [
        {"id": 1, "old_password": "test_user_pw_1", "new_password": "test_user_pw_10"},
        {"id": 2, "old_password": "test_user_pw_2", "new_password": "test_user_pw_20"},
        {"id": 3, "old_password": "test_user_pw_3", "new_password": "test_user_pw_30"},
    ],
)
def test_put_user_password_ok(client, create_users, user_data, session):
    # test user password change
    response = client.put(f"{router_prefix}/change-password", json=user_data)
    changed = session.query(User).filter_by(id=user_data["id"]).first()
    assert response.status_code == 200
    assert SecurityManager.compare_hash(changed.password, user_data["new_password"])


@pytest.mark.parametrize(
    "user_data",
    [
        {"id": 1, "old_password": "test_user_pw_2", "new_password": "test_user_pw_10"},
        {"id": 2, "old_password": "test_user_pw_3", "new_password": "test_user_pw_20"},
        {"id": 3, "old_password": "test_user_pw_4", "new_password": "test_user_pw_30"},
    ],
)
def test_put_user_password_incorect(client, create_users, user_data):
    # test user password change with incorrect old password
    response = client.put(f"{router_prefix}/change-password", json=user_data)
    assert response.status_code == 422
    assert (
        response.json()["detail"] == "Old password does not match with the current one."
    )


@pytest.mark.parametrize(
    "user_data",
    [
        {"id": 1, "old_password": "test_user_pw_2"},
        {"old_password": "test_user_pw_2", "new_password": "test_user_pw_2"},
        {"id": 2, "old_password": "test_user_pw_3", "new_password": ""},
        {"id": 3, "old_password": "", "new_password": "test_user_pw_30"},
    ],
)
def test_put_user_password_bad_data(client, create_users, user_data):
    # test user password change with bad data
    response = client.put(f"{router_prefix}/change-password", json=user_data)
    assert response.status_code == 422


@pytest.mark.parametrize(
    "user_data",
    [
        {"id": 10, "old_password": "test_user_pw_2", "new_password": "test_user_pw_10"},
        {"id": 20, "old_password": "test_user_pw_3", "new_password": "test_user_pw_20"},
        {"id": 30, "old_password": "test_user_pw_4", "new_password": "test_user_pw_30"},
    ],
)
def test_put_user_password_no_exist(client, create_users, user_data):
    # test user password change when user does not exist
    response = client.put(f"{router_prefix}/change-password", json=user_data)
    assert response.status_code == 200


@pytest.mark.parametrize("id", [1, 2, 3])
def test_get_user_by_id_ok(client, create_users, id):
    # test get user by id when data exists
    response = client.get(f"{router_prefix}/{id}")
    assert response.status_code == 200
    assert response.json()["id"] == id


@pytest.mark.parametrize("id", [10, 20, 30])
def test_get_user_by_id_no_exist(client, create_users, id):
    # test get user by id when data does not exist
    response = client.get(f"{router_prefix}/{id}")
    assert response.status_code == 200
    assert response.json()["detail"] == f"User with ID:{id} not found."


@pytest.mark.parametrize("id", ["a", "b", True])
def test_get_user_by_id_bad_data(client, create_users, id):
    # test get user by id when data is invalid
    response = client.get(f"{router_prefix}/{id}")
    assert response.status_code == 422


def test_get_all_users_ok(client, create_users):
    # test get user by id when data exists
    response = client.get(router_prefix)
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_get_all_users_no_exist(client):
    # test get user by id when data does not exist
    response = client.get(router_prefix)
    assert response.status_code == 200
    assert response.json() == []

@pytest.mark.parametrize(
    "user_data",
    [
        {"name": "test_user_1", "surname": "test_user_1"},
        {"name": "test_user_2", "surname": "test_user_2"},
        {"name": "test_user_3", "surname": "test_user_3"},
    ],
)
def test_put_user_ok(client,user_data,create_users):
    # test user update
    response = client.put(f"{router_prefix}/{user_data['name'][-1]}", json=user_data)
    assert response.status_code == 200
    assert response.json()["name"] == user_data["name"]
    assert response.json()["surname"] == user_data["surname"]