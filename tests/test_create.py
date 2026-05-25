"""
test_create.py — Tests for the POST /todos/ endpoint.

Manual test cases covered:
  - TC-002 : Create a Todo with all fields
  - TC-003 : Create a Todo with title only (optional fields use defaults)
  - TC-004 : Create a Todo without the required `title` field
  - TC-005 : Create a Todo with an empty title string
"""


def test_create_todo_all_fields(client):
    """TC-002 — POST /todos/ with all fields should return 200 and the created item."""
    payload = {
        "title": "Buy groceries",
        "description": "Milk, eggs, bread",
        "status": "pending"
    }
    response = client.post("/todos/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Buy groceries"
    assert data["description"] == "Milk, eggs, bread"
    assert data["status"] == "pending"
    assert isinstance(data["id"], int)
    assert data["id"] > 0


def test_create_todo_title_only(client):
    """TC-003 — POST /todos/ with title only should apply default values."""
    payload = {"title": "Call dentist"}
    response = client.post("/todos/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Call dentist"
    assert data["description"] is None
    assert data["status"] == "pending"
    assert isinstance(data["id"], int)


def test_create_todo_missing_title(client):
    """TC-004 — POST /todos/ without `title` should return 422 Unprocessable Entity."""
    payload = {"description": "No title provided"}
    response = client.post("/todos/", json=payload)
    assert response.status_code == 422
    errors = response.json()["detail"]
    fields = [e["loc"] for e in errors]
    assert any("title" in loc for loc in fields)


def test_create_todo_empty_title(client):
    """
    TC-005 — POST /todos/ with an empty title string should return 422.

    FIXED via TDD Feature 1: min_length=1 added to title field in schemas.py.
    The API now correctly rejects empty titles.
    """
    payload = {"title": ""}
    response = client.post("/todos/", json=payload)
    assert response.status_code == 422
