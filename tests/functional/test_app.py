import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session
from src.database import db_session


def test_app_ok(client):
    # test app
    response = client.get("/")
    assert response.status_code == 200


@pytest.mark.parametrize(
    "user_data",
    [
        {"username": "test_user_1", "password": "test_user_pw_1"},
        {"username": "test_user_2", "password": "test_user_pw_2"},
        {"username": "test_user_3", "password": "test_user_pw_3"},
    ],
)
def test_database_error_offline(client_offline_db, user_data):
    # test postgress service down with user endpoint
    response = client_offline_db.post("/user", json=user_data)
    print(response.json())
    assert response.status_code == 503
