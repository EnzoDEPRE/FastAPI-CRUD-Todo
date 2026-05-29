def test_creating_a_todo_returns_created_status(client):
    response = client.post("/todos/", json={"title": "Bug fix test"})
    assert response.status_code == 201


def test_empty_titles_are_still_rejected_when_creating_a_todo(client):
    response = client.post("/todos/", json={"title": ""})
    assert response.status_code == 422


def test_invalid_status_is_rejected_when_creating_a_todo(client):
    response = client.post("/todos/", json={"title": "Valid title", "status": "123"})
    assert response.status_code == 422


def test_invalid_status_is_rejected_when_updating_a_todo(client, create_todo):
    todo_id = create_todo(title="Test todo")["id"]
    response = client.put(f"/todos/{todo_id}", json={"status": "nimportequoi"})
    assert response.status_code == 422
