def test_user_cannot_create_a_todo_with_an_empty_title(client):
    response = client.post("/todos/", json={"title": ""})
    assert response.status_code == 422


def test_user_can_filter_todos_by_status(client, create_todo):
    create_todo(title="Pending todo", status="pending")
    create_todo(title="Done todo", status="done")

    response = client.get("/todos/?status=pending")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["status"] == "pending"
    assert data[0]["title"] == "Pending todo"


def test_user_can_see_how_many_todos_exist(client, create_todo):
    create_todo(title="Todo 1")
    create_todo(title="Todo 2")
    create_todo(title="Todo 3")

    response = client.get("/todos/count")
    assert response.status_code == 200
    assert response.json() == {"count": 3}
