import pytest

import app as app_module


@pytest.fixture
def client():
    app_module.tasks.clear()
    app_module.next_id = 1
    app_module.app.config["TESTING"] = True
    with app_module.app.test_client() as c:
        yield c


def test_home(client):
    res = client.get("/")
    assert res.status_code == 200
    assert "message" in res.get_json()


def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"


def test_add_and_list_task(client):
    res = client.post("/api/tasks", json={"title": "Pipeline banao"})
    assert res.status_code == 201
    assert res.get_json()["title"] == "Pipeline banao"

    res = client.get("/api/tasks")
    assert len(res.get_json()) == 1


def test_add_task_without_title(client):
    res = client.post("/api/tasks", json={})
    assert res.status_code == 400


def test_toggle_task(client):
    client.post("/api/tasks", json={"title": "Test"})
    res = client.put("/api/tasks/1")
    assert res.get_json()["done"] is True


def test_delete_task(client):
    client.post("/api/tasks", json={"title": "Test"})
    res = client.delete("/api/tasks/1")
    assert res.status_code == 200
    assert client.get("/api/tasks").get_json() == []


def test_missing_task(client):
    assert client.put("/api/tasks/99").status_code == 404
    assert client.delete("/api/tasks/99").status_code == 404
