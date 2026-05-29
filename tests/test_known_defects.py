def test_create_todo_should_return_201(client):
    response = client.post("/todos/", json={"title": "Defect test"})
    assert response.status_code == 201


def test_create_todo_empty_title_is_now_fixed(client):
    response = client.post("/todos/", json={"title": ""})
    assert response.status_code == 422


def test_create_todo_invalid_status_should_be_rejected(client):
    response = client.post("/todos/", json={"title": "Valid title", "status": "123"})
    assert response.status_code == 422


def test_update_todo_invalid_status_should_be_rejected(client, create_todo):
    todo_id = create_todo(title="Test todo")["id"]
    response = client.put(f"/todos/{todo_id}", json={"status": "nimportequoi"})
    assert response.status_code == 422
