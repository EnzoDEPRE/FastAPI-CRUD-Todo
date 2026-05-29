def test_user_can_read_all_todos_when_the_list_is_not_empty(client, create_todo):
    create_todo(title="Todo A")
    response = client.get("/todos/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    for item in data:
        assert "id" in item
        assert "title" in item
        assert "status" in item


def test_user_gets_an_empty_list_when_no_todos_exist(client):
    response = client.get("/todos/")
    assert response.status_code == 200
    assert response.json() == []


def test_user_can_read_todos_with_pagination(client, create_todo):
    create_todo(title="Todo 1")
    create_todo(title="Todo 2")
    create_todo(title="Todo 3")

    response = client.get("/todos/?skip=1&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Todo 2"
    assert data[1]["title"] == "Todo 3"


def test_user_can_read_one_existing_todo(client, create_todo):
    created = create_todo(title="Single Todo", description="Test desc")
    todo_id = created["id"]

    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == todo_id
    assert data["title"] == "Single Todo"
    assert data["description"] == "Test desc"


def test_user_gets_404_when_reading_an_unknown_todo(client):
    response = client.get("/todos/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}


def test_user_gets_validation_error_when_todo_id_is_not_a_number(client):
    response = client.get("/todos/abc")
    assert response.status_code == 422
