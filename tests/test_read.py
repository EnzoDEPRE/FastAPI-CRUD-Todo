def create_todo(client, title="Test Todo", description=None, status="pending"):
    payload = {"title": title}
    if description:
        payload["description"] = description
    if status != "pending":
        payload["status"] = status
    resp = client.post("/todos/", json=payload)
    assert resp.status_code == 200
    return resp.json()


def test_read_all_todos_non_empty(client):
    create_todo(client, title="Todo A")
    response = client.get("/todos/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    for item in data:
        assert "id" in item
        assert "title" in item
        assert "status" in item


def test_read_all_todos_empty_database(client):
    response = client.get("/todos/")
    assert response.status_code == 200
    assert response.json() == []


def test_read_todos_with_pagination(client):
    create_todo(client, title="Todo 1")
    create_todo(client, title="Todo 2")
    create_todo(client, title="Todo 3")

    response = client.get("/todos/?skip=1&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Todo 2"
    assert data[1]["title"] == "Todo 3"


def test_read_single_todo_existing(client):
    created = create_todo(client, title="Single Todo", description="Test desc")
    todo_id = created["id"]

    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == todo_id
    assert data["title"] == "Single Todo"
    assert data["description"] == "Test desc"


def test_read_single_todo_not_found(client):
    response = client.get("/todos/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}


def test_read_single_todo_invalid_id(client):
    response = client.get("/todos/abc")
    assert response.status_code == 422
