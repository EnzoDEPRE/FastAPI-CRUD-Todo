def create_todo(client, title="Initial Todo", description="Initial desc", status="pending"):
    payload = {"title": title, "description": description, "status": status}
    resp = client.post("/todos/", json=payload)
    assert resp.status_code == 200
    return resp.json()


def test_update_todo_all_fields(client):
    created = create_todo(client)
    todo_id = created["id"]

    payload = {
        "title": "Buy groceries — UPDATED",
        "description": "Milk, eggs, bread, butter",
        "status": "in_progress"
    }
    response = client.put(f"/todos/{todo_id}", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == todo_id
    assert data["title"] == "Buy groceries — UPDATED"
    assert data["description"] == "Milk, eggs, bread, butter"
    assert data["status"] == "in_progress"


def test_update_todo_partial_status_only(client):
    created = create_todo(client, title="Stable Title", description="Stable Desc")
    todo_id = created["id"]

    response = client.put(f"/todos/{todo_id}", json={"status": "done"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "done"
    assert data["title"] == "Stable Title"
    assert data["description"] == "Stable Desc"


def test_update_todo_not_found(client):
    response = client.put("/todos/9999", json={"title": "Ghost update"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}
