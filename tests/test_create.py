def test_user_can_create_todo_with_all_fields(client):
    payload = {
        "title": "Buy groceries",
        "description": "Milk, eggs, bread",
        "status": "pending"
    }
    response = client.post("/todos/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Buy groceries"
    assert data["description"] == "Milk, eggs, bread"
    assert data["status"] == "pending"
    assert isinstance(data["id"], int)
    assert data["id"] > 0


def test_user_can_create_todo_with_only_a_title(client):
    payload = {"title": "Call dentist"}
    response = client.post("/todos/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Call dentist"
    assert data["description"] is None
    assert data["status"] == "pending"
    assert isinstance(data["id"], int)


def test_user_cannot_create_todo_without_a_title(client):
    payload = {"description": "No title provided"}
    response = client.post("/todos/", json=payload)
    assert response.status_code == 422
    errors = response.json()["detail"]
    fields = [e["loc"] for e in errors]
    assert any("title" in loc for loc in fields)


def test_user_cannot_create_todo_with_an_empty_title(client):
    payload = {"title": ""}
    response = client.post("/todos/", json=payload)
    assert response.status_code == 422
