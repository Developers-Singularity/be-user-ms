import pytest
from src.extensions import SecurityManager

from src.models.user_model import User

router_prefix = "/user"


@pytest.mark.parametrize(
    "user_data",
    [
        {"username": "test_user_1", "password": "test_user_pw_1"},
        {"username": "test_user_2", "password": "test_user_pw_2"},
        {"username": "test_user_3", "password": "test_user_pw_3"},
    ],
)
def test_post_user_ok(client, user_data, session):
    response = client.post(router_prefix, json=user_data)
    created = session.query(User).filter_by(username=user_data["username"]).first()
    assert response.status_code == 201
    assert user_data["username"] == created.username


# i need a test to test if values provided are empty
@pytest.mark.parametrize(
    "user_data",
    [
        {"username": "", "password": ""},
        {"username": "name", "password": ""},
        {"username": "", "password": "password"},
        {"username": "name", "password": "pas"},
        {"username": "name" * 6, "password": "password"},
        {"username": "name", "password": "password" * 6},
    ],
)
def test_post_user_bad_data(client, user_data, session):
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
def test_put_user_password_incorect(client, create_users, user_data, session):
    response = client.put(f"{router_prefix}/change-password", json=user_data)
    assert response.status_code == 422
    assert response.json()["detail"]== "Old password does not match with the current one."

@pytest.mark.parametrize(
    "user_data",
    [
        {"id": 1, "old_password": "test_user_pw_2"},
        {"old_password": "test_user_pw_2", "new_password": "test_user_pw_2"},
        {"id": 2, "old_password": "test_user_pw_3", "new_password": ""},
        {"id": 3, "old_password": "", "new_password": "test_user_pw_30"},
    ],
)
def test_put_user_password_bad_data(client, create_users, user_data, session):
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
def test_put_user_password_no_exist(client, create_users, user_data, session):
    response = client.put(f"{router_prefix}/change-password", json=user_data)
    assert response.status_code == 200