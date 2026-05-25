import pytest


@pytest.mark.xfail(strict=True, reason="DEFECT-001: POST returns 200 instead of 201")
def test_create_todo_should_return_201(client):
    response = client.post("/todos/", json={"title": "Defect test"})
    assert response.status_code == 201


def test_create_todo_empty_title_is_now_fixed(client):
    response = client.post("/todos/", json={"title": ""})
    assert response.status_code == 422


@pytest.mark.xfail(strict=True, reason="DEFECT-003: Invalid status value accepted on create")
def test_create_todo_invalid_status_should_be_rejected(client):
    response = client.post("/todos/", json={"title": "Valid title", "status": "123"})
    assert response.status_code == 422


@pytest.mark.xfail(strict=True, reason="DEFECT-003: Invalid status value accepted on update")
def test_update_todo_invalid_status_should_be_rejected(client):
    resp = client.post("/todos/", json={"title": "Test todo"})
    todo_id = resp.json()["id"]
    response = client.put(f"/todos/{todo_id}", json={"status": "nimportequoi"})
    assert response.status_code == 422
