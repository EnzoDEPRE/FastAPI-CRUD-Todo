def test_user_can_update_all_todo_fields(client, create_todo):
    created = create_todo(title="Initial Todo", description="Initial desc", status="pending")
    todo_id = created["id"]

    payload = {
        "title": "Buy groceries - updated",
        "description": "Milk, eggs, bread, butter",
        "status": "in_progress"
    }
    response = client.put(f"/todos/{todo_id}", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == todo_id
    assert data["title"] == "Buy groceries - updated"
    assert data["description"] == "Milk, eggs, bread, butter"
    assert data["status"] == "in_progress"


def test_user_can_update_only_the_todo_status(client, create_todo):
    created = create_todo(title="Stable Title", description="Stable Desc")
    todo_id = created["id"]

    response = client.put(f"/todos/{todo_id}", json={"status": "done"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "done"
    assert data["title"] == "Stable Title"
    assert data["description"] == "Stable Desc"


def test_user_gets_404_when_updating_an_unknown_todo(client):
    response = client.put("/todos/9999", json={"title": "Ghost update"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}


def test_user_cannot_update_a_todo_with_an_empty_title(client, create_todo):
    created = create_todo(title="Keep my title")

    response = client.put(f"/todos/{created['id']}", json={"title": ""})

    assert response.status_code == 422
