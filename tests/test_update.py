"""
test_update.py — Tests for the PUT /todos/{id} endpoint.

Manual test cases covered:
  - TC-012 : Update all fields of an existing Todo
  - TC-013 : Partially update a Todo (status only)
  - TC-014 : Update a Todo with a non-existent ID
"""


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def create_todo(client, title="Initial Todo", description="Initial desc", status="pending"):
    payload = {"title": title, "description": description, "status": status}
    resp = client.post("/todos/", json=payload)
    assert resp.status_code == 200
    return resp.json()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_update_todo_all_fields(client):
    """TC-012 — PUT /todos/{id} with all fields updates the item correctly."""
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
    """TC-013 — PUT /todos/{id} with only `status` leaves other fields unchanged."""
    created = create_todo(client, title="Stable Title", description="Stable Desc")
    todo_id = created["id"]

    response = client.put(f"/todos/{todo_id}", json={"status": "done"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "done"
    assert data["title"] == "Stable Title"
    assert data["description"] == "Stable Desc"


def test_update_todo_not_found(client):
    """TC-014 — PUT /todos/9999 returns 404 when the ID does not exist."""
    response = client.put("/todos/9999", json={"title": "Ghost update"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}
