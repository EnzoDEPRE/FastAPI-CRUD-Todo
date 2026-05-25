"""
test_delete.py — Tests for the DELETE /todos/{id} endpoint.

Manual test cases covered:
  - TC-015 : Delete an existing Todo
  - TC-016 : Verify Todo is deleted (read after delete)
  - TC-017 : Delete a Todo with a non-existent ID
"""


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def create_todo(client, title="Todo to delete"):
    resp = client.post("/todos/", json={"title": title})
    assert resp.status_code == 200
    return resp.json()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_delete_existing_todo(client):
    """TC-015 — DELETE /todos/{id} returns 200 and confirmation message."""
    created = create_todo(client)
    todo_id = created["id"]

    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json() == {"detail": "Todo deleted"}


def test_read_after_delete(client):
    """TC-016 — After deletion, GET /todos/{id} returns 404."""
    created = create_todo(client)
    todo_id = created["id"]

    del_response = client.delete(f"/todos/{todo_id}")
    assert del_response.status_code == 200

    get_response = client.get(f"/todos/{todo_id}")
    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "Todo not found"}


def test_delete_todo_not_found(client):
    """TC-017 — DELETE /todos/9999 returns 404 when the ID does not exist."""
    response = client.delete("/todos/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}
