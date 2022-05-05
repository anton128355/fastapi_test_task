import json
import pytest
from starlette.testclient import TestClient
import os
import sys
BASE_DIR= os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, '../app'))
from app.main import app
from app.api import crud


@pytest.fixture(scope="module")
def test_app():
    with TestClient(app) as client:
        yield client 


def test_create_user(test_app, monkeypatch):
    test_request_payload = {"username": "something0", "email": "something1@gmail.com", "password": "something2"}
    test_response_payload = {"username": "something0", "email": "something1@gmail.com", "password": "something2", "id": 1}

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(crud, "post", mock_post)

    response = test_app.post('/user', json=test_request_payload)

    assert response.status_code == 201
    assert response.json() == test_response_payload


def test_read_user(test_app, monkeypatch):
    test_data = {"id": 1, "username": "something0", "email": "something1@gmail.com", "password": "something2"}

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/user/1")
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_user_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/user/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"

    response = test_app.get("/user/0")
    assert response.status_code == 422


def test_read_all_users(test_app, monkeypatch):
    test_data = [
        {"id": 1, "username": "something0", "email": "something1@gmail.com", "password": "something2"},
        {"id": 2, "username": "something3", "email": "something4@gmail.com", "password": "something5"},
    ]

    async def mock_get_all():
        return test_data

    monkeypatch.setattr(crud, "get_all", mock_get_all)

    response = test_app.get("/user-list")
    assert response.status_code == 200
    assert response.json() == test_data


def test_put_user(test_app, monkeypatch):
    test_data1 = {"username": "something0", "email": "something1@gmail.com", "password": "something2", "id": 1}
    test_data2 = {}

    async def mock_get(id):
        return True

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_put(id, payload):
        return 1

    monkeypatch.setattr(crud, "put", mock_put)

    response1 = test_app.put("/user/1", data=json.dumps(test_data1))
    response2 = test_app.put("/user/2", data=json.dumps(test_data2))

    assert response1.status_code == 200
    assert response1.json() == test_data1

    assert response2.status_code == 200
    assert response2.json() == {"username": "random_str", "email": "random_str@gmail.com", "password": "random_str", "id": 1}


def test_patch_user(test_app, monkeypatch):
    test_data1 = {"username": "something0", "email": "something1@gmail.com", "password": "something2", "id": 1},
    test_data2 = {"username": "something3", "email": "something4@gmail.com", "password": "something2", "id": 2}

    async def mock_get(id):
        return True

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_put(id, payload):
        return 1

    monkeypatch.setattr(crud, "put", mock_put)

    response1 = test_app.put("/user/1", data=json.dumps(test_data1))
    response2 = test_app.put("/user/2", data=json.dumps(test_data2))


    async def mock_get(id):
        return True

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_patch(id, payload):
        return 1

    monkeypatch.setattr(crud, "patch", mock_patch)

    response1 = test_app.patch("/user/1", data=json.dumps({"username": "real_name", "password": "real_password"}))
    response2 = test_app.patch("/user/2", data=json.dumps({"email": "real_email@gmail.com"}))

    assert response1.status_code == 200
    assert response1.json() == {"username": "real_name", "email": "random_str@gmail.com", "password": "real_password", "id": 1}

    assert response2.status_code == 200
    assert response2.json() == {"username": "random_str", "email": "real_email@gmail.com", "password": "random_str", "id": 1}


def test_remove_user(test_app, monkeypatch):
    test_data = {"username": "something0", "email": "something1@gmail.com", "password": "something2", "id": 1}

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_delete(id):
        return id

    monkeypatch.setattr(crud, "delete", mock_delete)

    response = test_app.delete("/user/1")
    assert response.status_code == 200
    assert response.json() == test_data


def test_remove_user_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.delete("/user/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"

    response = test_app.delete("/user/0")
    assert response.status_code == 422